"""Validate the blocked Design B human-LLM pilot preparation materials."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "studies" / "human_llm_pilot"
DOCS_DIR = ROOT / "docs" / "studies"
PROMPTS_DIR = ROOT / "prompts" / "human_llm_pilot"

EXPECTED_MAIN_SHA = "6364add9a89f3fe6d26043727b9d44cb21a76db0"
EXPECTED_PR18_START_SHA = "d22c5879eed4a1f5b751fecdf1dfbbe1a27d860b"
EXPECTED_SAMPLE_SIZE = 25
EXPECTED_LAYER_COUNTS = {"Layer 1": 15, "Layer 2": 10}
EXPECTED_TERMINAL_COUNTS = {
    "selected": 25,
    "eligible_not_selected": 1,
    "ineligible": 4,
}
EXPECTED_CATEGORIES = [
    "cue_function",
    "warrant_attribution",
    "warrant_relation",
    "operation_function",
    "boundary_setting",
    "temporal_layering",
    "perspective_assignment",
    "context_inference",
]
EXPECTED_MANUAL = {
    "manual_version": "friction_locus_manual_v0_1",
    "manual_status": "AUTHORITATIVE_FOR_PROTOCOL_REVIEW",
    "manual_merge_commit": EXPECTED_MAIN_SHA,
    "manual_markdown_path": "docs/manuals/friction_locus_manual_v0_1.md",
    "manual_markdown_sha256": "f26f5de05819c4fd36c0d88e7d86320d7374c27185c36575b18b584fc5d9b426",
    "manual_json_path": "docs/manuals/friction_locus_manual_v0_1.json",
    "manual_json_sha256": "797d79fcdb29fc32850c3778c6afb029ac0768207ea33f66d714fe8fa8cb591a",
    "manual_manifest_path": "docs/manuals/friction_locus_manual_manifest.json",
    "manual_manifest_sha256": "1b80c0931a0ed8159aaeeb6e7b348331beb33130776469f223ae2a8cfe89d8de",
    "coder_schema_path": "schemas/human_llm_coder_output.schema.json",
    "coder_schema_sha256": "2abdf5f5690aada67f1694f8d83dfe95236fbcba46c1bbcfca169567dbda7b12",
    "schema_compatibility": "compatible",
}
FORBIDDEN_PACKET_FIELDS = {
    "canonical_text",
    "expected_label",
    "friction_locus",
    "manual_hint",
    "model_facing_instruction",
    "model_output",
    "primary_label",
    "researcher_interpretation",
    "secondary_scholarship",
    "translation_or_gloss",
}
FORBIDDEN_FREEZE_FILE_TOKENS = {
    "agreement",
    "human_annotation",
    "human_record",
    "model_output",
    "parsed_model",
    "raw_output",
    "result",
    "run_result",
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_file_sha(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return sha_bytes(data)


def canonical_json_hash(payload: dict[str, Any], hash_field: str) -> str:
    def scrub(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: scrub(item)
                for key, item in sorted(value.items())
                if key != hash_field
            }
        if isinstance(value, list):
            return [scrub(item) for item in value]
        return value

    encoded = json.dumps(
        scrub(payload),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha_bytes(encoded)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalized_text(path: Path) -> str:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n").decode("utf-8")


def condition_payload(condition: str) -> str:
    base = normalized_text(PROMPTS_DIR / f"condition_{condition}.txt")
    if condition == "C":
        manual = normalized_text(ROOT / EXPECTED_MANUAL["manual_json_path"])
        return base.rstrip("\n") + "\nBEGIN_FULL_MANUAL_JSON\n" + manual.rstrip("\n") + "\nEND_FULL_MANUAL_JSON\n"
    return base if base.endswith("\n") else base + "\n"


def assembled_prompt_template(condition: str) -> str:
    components = [
        normalized_text(PROMPTS_DIR / "system_prompt.txt"),
        condition_payload(condition),
        normalized_text(PROMPTS_DIR / "source_packet_envelope.txt"),
        normalized_text(ROOT / "schemas" / "human_llm_model_response.schema.json"),
        normalized_text(PROMPTS_DIR / "case_and_run_context.txt"),
    ]
    return "\n\n".join(component.rstrip("\n") for component in components) + "\n"


def assembled_prompt_instance(condition: str, **substitutions: str) -> str:
    text = assembled_prompt_template(condition)
    for key, value in substitutions.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def validate_model_response_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "selected_evidence",
        "primary_label",
        "friction_locus_proposed",
        "rationale_mechanism",
        "uncertainty",
        "alternative_pathways",
        "counterfactual_tests",
        "candidate_loci",
        "decision_path",
        "review_policy_applied",
        "escalation_required",
        "escalation_reason",
        "free_text_rationale",
        "unresolved_ambiguity",
    }
    forbidden_runtime = {
        "record_type",
        "actor_type",
        "record_id",
        "timestamp",
        "record_hash",
        "run_id",
        "provider",
        "model",
        "model_version_if_known",
        "prompt_version",
        "instruction_condition",
        "source_packet_hash",
        "raw_output_hash",
        "parse_status",
        "retry_count",
        "technical_failure_status",
        "review_of_record_id",
        "review_of_record_hash",
    }
    extra = set(payload) - required
    missing = required - set(payload)
    errors.extend(f"model response extra field: {field}" for field in sorted(extra))
    errors.extend(f"model response missing field: {field}" for field in sorted(missing))
    if forbidden_runtime & set(payload):
        errors.append("model response contains runtime metadata")
    candidate_loci = payload.get("candidate_loci", [])
    if isinstance(candidate_loci, list):
        categories = [item.get("category") for item in candidate_loci if isinstance(item, dict)]
        if set(categories) != set(EXPECTED_CATEGORIES) or len(categories) != len(EXPECTED_CATEGORIES):
            errors.append("model response candidate_loci category set mismatch")
        for item in candidate_loci:
            if not isinstance(item, dict):
                errors.append("model response candidate_loci entry is not object")
                continue
            for key in ["category", "state", "cited_evidence", "rationale", "confidence"]:
                if key not in item:
                    errors.append(f"model response candidate_loci missing {key}")
            if item.get("state") == "candidate_supported" and not item.get("cited_evidence"):
                errors.append(f"supported candidate lacks cited evidence: {item.get('category')}")
    else:
        errors.append("model response candidate_loci is not a list")
    return errors


def enrich_model_payload(payload: dict[str, Any]) -> dict[str, Any]:
    enriched = {
        "record_type": "model_coder_record",
        "actor_type": "model",
        "case_id": "TEST_CASE",
        "record_id": "MODEL_TEST_RECORD_001",
        "timestamp": "2026-07-03T00:00:00Z",
        "manual_version": "friction_locus_manual_v0_1",
        **payload,
        "friction_locus_operational_status": "requires_human_review",
        "final_operational_label": "unresolved",
        "review_of_record_id": None,
        "review_of_record_hash": None,
        "run_id": "RUN_TEST_001",
        "provider": "OpenAI",
        "model": "UNRESOLVED_PENDING_OFFICIAL_VERIFICATION",
        "model_version_if_known": None,
        "prompt_version": "human_llm_pilot_prompts_v0_3_2026_07_03_prompt_assembly_enrichment_blocked",
        "instruction_condition": "C_full_manual",
        "source_packet_hash": "0" * 64,
        "raw_output_hash": "1" * 64,
        "parse_status": "valid_json",
        "retry_count": 0,
        "technical_failure_status": "none",
    }
    record_hash_payload = json.dumps(
        {k: v for k, v in sorted(enriched.items()) if k != "record_hash"},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    enriched["record_hash"] = sha_bytes(record_hash_payload)
    return enriched


def validate_enriched_model_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in [
        "record_type",
        "actor_type",
        "case_id",
        "record_id",
        "timestamp",
        "manual_version",
        "record_hash",
        "run_id",
        "provider",
        "model",
        "prompt_version",
        "instruction_condition",
        "source_packet_hash",
        "raw_output_hash",
        "parse_status",
        "retry_count",
        "technical_failure_status",
    ]:
        if key not in record:
            errors.append(f"enriched model record missing {key}")
    if record.get("record_type") != "model_coder_record":
        errors.append("enriched model record_type mismatch")
    if record.get("review_of_record_id") is not None or record.get("review_of_record_hash") is not None:
        errors.append("original model proposal review linkage must be null")
    if not isinstance(record.get("record_hash"), str) or len(record["record_hash"]) != 64:
        errors.append("enriched model record hash invalid")
    errors.extend(validate_model_response_payload({k: record[k] for k in load_json(ROOT / "schemas" / "human_llm_model_response.schema.json")["required"] if k in record}))
    return errors


def schema_contains_exact_categories(schema: dict[str, Any], path: str) -> bool:
    candidate_schema = schema
    for key in path.split("."):
        candidate_schema = candidate_schema[key]
    all_of = candidate_schema.get("allOf", [])
    found: dict[str, tuple[int, int]] = {}
    for item in all_of:
        category = (
            item.get("contains", {})
            .get("properties", {})
            .get("category", {})
            .get("const")
        )
        if category:
            found[category] = (item.get("minContains"), item.get("maxContains"))
    return found == {category: (1, 1) for category in EXPECTED_CATEGORIES}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_manual_reference(errors: list[str]) -> dict[str, Any]:
    ref = load_json(DATA_DIR / "authoritative_manual_reference.json")
    for key, expected in EXPECTED_MANUAL.items():
        require(ref.get(key) == expected, f"manual reference mismatch for {key}", errors)
    require(
        ref["claim_boundary"]
        == "Authoritative for protocol review only; not empirical validation, coder-reliability validation, ontology validation, or execution authorization.",
        "manual claim boundary mismatch",
        errors,
    )
    for path_key, hash_key in [
        ("manual_markdown_path", "manual_markdown_sha256"),
        ("manual_json_path", "manual_json_sha256"),
        ("manual_manifest_path", "manual_manifest_sha256"),
        ("coder_schema_path", "coder_schema_sha256"),
    ]:
        require(
            normalized_file_sha(ROOT / ref[path_key]) == ref[hash_key],
            f"authoritative hash mismatch for {path_key}",
            errors,
        )
    manual = load_json(ROOT / ref["manual_json_path"])
    require(manual["manual_status"] == ref["manual_status"], "manual JSON status mismatch", errors)
    require(manual["category_order"] == EXPECTED_CATEGORIES, "manual category set mismatch", errors)
    return ref


def validate() -> list[str]:
    errors: list[str] = []

    sample = load_json(DATA_DIR / "sample_manifest.json")
    allocation = load_json(DATA_DIR / "allocation_manifest.json")
    manual = load_json(DATA_DIR / "manual_freeze_manifest.json")
    prompts = load_json(DATA_DIR / "prompt_bundle_manifest.json")
    model_spec = load_json(DATA_DIR / "model_execution_spec.json")
    cost = load_json(DATA_DIR / "cost_ceiling.json")
    governance = load_json(DATA_DIR / "governance_status.json")
    freeze_status = load_json(DATA_DIR / "freeze_status.json")
    reconciliation = load_json(DATA_DIR / "candidate_count_reconciliation.json")
    prompt_audit = load_json(DATA_DIR / "prompt_condition_difference_audit.json")
    assembly = load_json(DATA_DIR / "prompt_assembly_manifest.json")
    freeze_pkg = load_json(DATA_DIR / "freeze_package_manifest.json")
    model_response_template = load_json(ROOT / "templates" / "model_response_payload.json")
    source_rows = read_csv(DATA_DIR / "source_manifest.csv")
    rights_rows = read_csv(DATA_DIR / "source_rights_manifest.csv")
    substantive_rows = read_csv(DATA_DIR / "source_packet_substantive_audit.csv")
    familiarity_rows = read_csv(DATA_DIR / "researcher_familiarity_audit.csv")
    selection_rows = read_csv(DOCS_DIR / "human_llm_sample_selection_log.csv")

    manual_ref = validate_manual_reference(errors)

    selected_ids = sample["selected_case_ids"]
    require(len(selected_ids) == EXPECTED_SAMPLE_SIZE, "unexpected sample size", errors)
    require(len(selected_ids) == len(set(selected_ids)), "duplicate selected case IDs", errors)
    layer_counts: dict[str, int] = {}
    for layer in sample["layer_assignments"].values():
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
    require(layer_counts == EXPECTED_LAYER_COUNTS, f"unexpected layer counts: {layer_counts}", errors)
    require(
        sample["sample_manifest_hash"] == canonical_json_hash(sample, "sample_manifest_hash"),
        "sample manifest hash mismatch",
        errors,
    )

    require(reconciliation["screened_count"] == 30, "screened count mismatch", errors)
    require(reconciliation["eligible_count"] == 26, "eligible count mismatch", errors)
    require(reconciliation["ineligible_count"] == 4, "ineligible count mismatch", errors)
    require(reconciliation["eligible_not_selected_count"] == 1, "eligible-not-selected count mismatch", errors)
    require(reconciliation["selected_count"] == EXPECTED_SAMPLE_SIZE, "selected count mismatch", errors)
    require(reconciliation["arithmetic_result"] is True, "candidate arithmetic is not reconciled", errors)

    terminal_counts: dict[str, int] = {}
    for row in selection_rows:
        terminal_counts[row["terminal_category"]] = terminal_counts.get(row["terminal_category"], 0) + 1
        if row["terminal_category"] == "eligible_not_selected":
            require(not row["exclusion_reason_code"], "eligible non-selected row still uses EXCL code", errors)
            require(row["non_selection_reason_code"].startswith("NOT_SELECTED_"), "missing non-selection reason", errors)
        if row["terminal_category"] == "ineligible":
            require(row["eligibility_exclusion_reason_code"].startswith("EXCL_"), "ineligible row lacks EXCL code", errors)
    require(terminal_counts == EXPECTED_TERMINAL_COUNTS, f"terminal counts mismatch: {terminal_counts}", errors)

    source_by_case = {row["case_id"]: row for row in source_rows}
    rights_by_case = {row["case_id"]: row for row in rights_rows}
    substantive_by_case = {row["case_id"]: row for row in substantive_rows}
    familiarity_by_case = {row["case_id"]: row for row in familiarity_rows}
    require(set(source_by_case) == set(selected_ids), "source manifest and sample disagree", errors)
    require(set(rights_by_case) == set(selected_ids), "rights manifest and sample disagree", errors)
    require(set(substantive_by_case) == set(selected_ids), "substantive audit and sample disagree", errors)
    require(set(familiarity_by_case) == set(selected_ids), "familiarity audit and sample disagree", errors)

    selected_log_rows = {
        row["candidate_id"]: row
        for row in selection_rows
        if row["inclusion_status"] == "selected"
    }
    require(set(selected_log_rows) == set(selected_ids), "selection log and sample disagree", errors)

    for case_id in selected_ids:
        packet_path = ROOT / source_by_case[case_id]["source_packet_path"]
        packet = load_json(packet_path)
        manifest_row = source_by_case[case_id]
        rights_row = rights_by_case[case_id]
        substantive_row = substantive_by_case[case_id]
        require(packet["case_id"] == case_id, f"{case_id}: packet case ID mismatch", errors)
        require(
            normalized_file_sha(packet_path) == manifest_row["source_packet_sha256"],
            f"{case_id}: packet file SHA mismatch",
            errors,
        )
        require(
            packet["source_packet_hash"]
            == canonical_json_hash(packet, "source_packet_hash")
            == manifest_row["source_packet_hash"],
            f"{case_id}: source packet hash mismatch",
            errors,
        )
        require(
            not (FORBIDDEN_PACKET_FIELDS & set(packet)),
            f"{case_id}: public packet contains text or interpretive fields",
            errors,
        )
        require(packet["canonical_text_publication_status"] == "not_in_public_repository", f"{case_id}: text not redacted", errors)
        require(packet["public_redistribution_status"] == "not_confirmed_pending_rights_review", f"{case_id}: redistribution overstated", errors)
        require(packet["repository_publication_status"] == "metadata_only_text_redacted", f"{case_id}: publication status not metadata-only", errors)
        require(packet["text_layer_visibility"]["researcher_and_model_identical"] is True, f"{case_id}: researcher/model layers differ", errors)
        require(all(segment.get("text_status") == "redacted_from_public_pr_pending_rights_review" for segment in packet["segments"]), f"{case_id}: segment text not redacted", errors)
        require(rights_row["public_redistribution_status"] == "not_confirmed_pending_rights_review", f"{case_id}: rights overstate clearance", errors)
        require(substantive_row["failure"] == "none_public_execution_blocked_by_rights_redaction", f"{case_id}: substantive audit failure", errors)
        require(
            "no friction_locus labels inferred or used"
            in selected_log_rows[case_id]["label_information_visible_at_selection"],
            f"{case_id}: selection log exposes label information",
            errors,
        )

    familiarity_levels = {row["researcher_familiarity_level"] for row in familiarity_rows}
    require(len(familiarity_levels) >= 3, "familiarity audit still uses a blanket value", errors)
    require("casual_familiarity" not in familiarity_levels, "old blanket familiarity value remains", errors)

    require(manual["repository_commit"] == EXPECTED_MAIN_SHA, "manual merge commit mismatch", errors)
    require(manual["manual_freeze_status"] == "MANUAL_COMPATIBILITY_PASSED_AUTHORITATIVE_FOR_PROTOCOL_REVIEW", "manual freeze status mismatch", errors)
    require(manual["manual_path"] == manual_ref["manual_markdown_path"], "manual path mismatch", errors)
    require(manual["manual_file_hash"] == manual_ref["manual_markdown_sha256"], "manual file hash mismatch", errors)
    require(manual["manual_json_hash"] == manual_ref["manual_json_sha256"], "manual JSON hash mismatch", errors)
    require(manual["manual_manifest_hash"] == manual_ref["manual_manifest_sha256"], "manual manifest hash mismatch", errors)
    require(manual["schema_hash"] == manual_ref["coder_schema_sha256"], "schema hash mismatch", errors)
    require(manual["schema_compatibility"] == "compatible", "schema compatibility mismatch", errors)
    require(manual["required_operational_components_missing"] == [], "manual still lists missing operational components", errors)

    schema = load_json(ROOT / manual["schema_path"])
    schema_categories = set(schema["$defs"]["substantive_friction_locus"]["enum"])
    require(schema_categories == set(EXPECTED_CATEGORIES), "schema substantive categories mismatch", errors)
    require(schema["$defs"]["candidate_loci"]["minItems"] == 8, "candidate_loci minItems mismatch", errors)
    require(schema["$defs"]["candidate_loci"]["maxItems"] == 8, "candidate_loci maxItems mismatch", errors)
    require("review_policy_applied" in schema["$defs"], "review_policy_applied missing from schema", errors)
    require("review_of_record_id" in schema["$defs"]["shared_record"]["properties"], "review_of_record_id missing", errors)
    require("review_of_record_hash" in schema["$defs"]["shared_record"]["properties"], "review_of_record_hash missing", errors)

    for key in [
        "system_prompt",
        "user_prompt_template",
        "condition_A",
        "condition_B",
        "condition_C",
        "human_researcher_instructions",
        "output_schema",
        "model_response_schema",
        "model_response_template",
        "source_packet_envelope",
    ]:
        path_key = f"{key}_path"
        hash_key = f"{key}_hash"
        require(
            normalized_file_sha(ROOT / prompts[path_key]) == prompts[hash_key],
            f"{key} hash mismatch",
            errors,
        )
    require(prompts["prompt_bundle_status"] == "BLOCKED_NOT_EXECUTION_READY", "prompt bundle must remain blocked", errors)
    require(prompts["manual_compatibility_status"] == "PASSED_AUTHORITATIVE_MANUAL_REFERENCE_VERIFIED", "manual compatibility status mismatch", errors)
    require(prompts["static_prompt_schema_status"] == "PASSED_MODEL_RESPONSE_SCHEMA_COMPATIBILITY_EXECUTION_BLOCKED", "static prompt/schema status mismatch", errors)
    require(prompts["prompt_assembly_status"] == "PASSED_PROMPT_ASSEMBLY_SPECIFIED_EXECUTION_BLOCKED", "prompt assembly status mismatch", errors)
    require(prompts["model_response_enrichment_status"] == "PASSED_CONTRACT_SPECIFIED_EXECUTION_BLOCKED", "enrichment status mismatch", errors)
    require(prompts["human_model_content_comparability_status"] == "PASSED_IDENTICAL_SOURCE_AND_MANUAL_CONTENT_WITH_DOCUMENTED_ACCESS_AFFORDANCE_ASYMMETRIES_EXECUTION_BLOCKED", "human/model content comparability status mismatch", errors)
    require(prompts["condition_manipulation_status"] == "PASSED_SHARED_BASELINE_WITH_DECLARED_INSTRUCTION_DEPTH_INCREMENTS_EXECUTION_BLOCKED", "condition manipulation status mismatch", errors)
    require(prompts["prompt_compatibility_status"].startswith("BLOCKED"), "prompt compatibility should remain blocked until execution gates pass", errors)
    require(prompts["condition_C_status"] == "CONDITION_C_FULL_JSON_MANUAL_INJECTION_SPECIFIED_EXECUTION_BLOCKED", "Condition C status mismatch", errors)
    require(prompts["browsing_status"] == "disabled", "browsing must be disabled", errors)
    require(prompts["tool_status"] == "disabled", "tools must be disabled", errors)

    require(assembly["assembly_order"] == ["SYSTEM_PROMPT", "CONDITION_PAYLOAD", "SOURCE_PACKET_ENVELOPE", "MODEL_RESPONSE_SCHEMA", "CASE_AND_RUN_CONTEXT"], "prompt assembly order mismatch", errors)
    require(assembly["component_joiner"] == "\\n\\n", "component joiner mismatch", errors)
    require(assembly["component_trailing_newline_rule"] == "include exactly one final trailing LF after CASE_AND_RUN_CONTEXT", "trailing newline rule mismatch", errors)
    require(assembly["component_normalization_rule"].startswith("UTF-8 text with CRLF and CR normalized to LF"), "normalization rule mismatch", errors)
    require(assembly["model_visible_context_fields"] == ["case_id", "instruction_condition", "prompt_bundle_version"], "model-visible context fields mismatch", errors)
    for field in ["assembled_prompt_hash", "source_packet_hash", "provider", "model", "run_id", "runtime_settings", "retry_metadata", "pricing_metadata"]:
        require(field in assembly["harness_only_context_fields"], f"harness-only field missing from manifest: {field}", errors)
    require(assembly["condition_C_manual_injection"]["repository_or_tool_access_required_by_model"] is False, "Condition C requires repository/tool access", errors)
    require(assembly["condition_C_manual_injection"]["source_sha256"] == EXPECTED_MANUAL["manual_json_sha256"], "Condition C manual injection hash mismatch", errors)
    for condition in ["A", "B", "C"]:
        require(
            sha_bytes(condition_payload(condition).encode("utf-8")) == assembly["condition_payload_hashes"][condition],
            f"condition payload hash mismatch for {condition}",
            errors,
        )
        require(
            sha_bytes(assembled_prompt_template(condition).encode("utf-8")) == assembly["assembled_prompt_template_hashes"][condition],
            f"assembled prompt template hash mismatch for {condition}",
            errors,
        )
    assembled_c = assembled_prompt_template("C")
    for forbidden in [
        "assembled_prompt_hash",
        "{{ASSEMBLED_PROMPT_HASH}}",
        "run_id:",
        "{{RUN_ID}}",
        "source_packet_hash:",
        "{{SOURCE_PACKET_HASH}}",
        "provider:",
        "model:",
        "runtime_settings",
        "retry_metadata",
        "pricing_metadata",
    ]:
        require(forbidden not in assembled_c, f"harness-only field appears in model-visible prompt: {forbidden}", errors)
    instance_c = assembled_prompt_instance(
        "C",
        CONTROLLED_SOURCE_PACKET_JSON='{"case_id":"TEST","segments":[]}',
        CASE_ID="TEST_CASE",
        INSTRUCTION_CONDITION="C_full_manual",
        PROMPT_BUNDLE_VERSION=prompts["prompt_bundle_version"],
    )
    changed_instance_c = assembled_prompt_instance(
        "C",
        CONTROLLED_SOURCE_PACKET_JSON='{"case_id":"TEST","segments":[{"id":"E1"}]}',
        CASE_ID="TEST_CASE",
        INSTRUCTION_CONDITION="C_full_manual",
        PROMPT_BUNDLE_VERSION=prompts["prompt_bundle_version"],
    )
    require(sha_bytes(instance_c.encode("utf-8")) != assembly["assembled_prompt_template_hashes"]["C"], "instance hash should differ from template hash after substitution", errors)
    require(sha_bytes(instance_c.encode("utf-8")) != sha_bytes(changed_instance_c.encode("utf-8")), "changing model-visible byte does not change instance hash", errors)
    require("BEGIN_FULL_MANUAL_JSON" in condition_payload("C"), "Condition C assembled payload lacks manual begin delimiter", errors)
    require("END_FULL_MANUAL_JSON" in condition_payload("C"), "Condition C assembled payload lacks manual end delimiter", errors)
    require(EXPECTED_MANUAL["manual_json_sha256"] == normalized_file_sha(ROOT / assembly["condition_C_manual_injection"]["source_path"]), "injected manual file hash mismatch", errors)

    response_schema = load_json(ROOT / prompts["model_response_schema_path"])
    forbidden_model_response_fields = {
        "record_type",
        "actor_type",
        "record_id",
        "timestamp",
        "record_hash",
        "run_id",
        "provider",
        "model",
        "model_version_if_known",
        "prompt_version",
        "instruction_condition",
        "source_packet_hash",
        "raw_output_hash",
        "parse_status",
        "retry_count",
        "technical_failure_status",
        "review_of_record_id",
        "review_of_record_hash",
    }
    require(response_schema["additionalProperties"] is False, "model response schema must reject additional properties", errors)
    require(not (forbidden_model_response_fields & set(response_schema["properties"])), "model response schema includes runtime metadata fields", errors)
    require(schema_contains_exact_categories(response_schema, "$defs.candidate_loci"), "model response schema lacks exact category coverage", errors)
    require(schema_contains_exact_categories(schema, "$defs.candidate_loci"), "final coder schema lacks exact category coverage", errors)
    require(response_schema["$defs"]["substantive_friction_locus"]["enum"] == schema["$defs"]["substantive_friction_locus"]["enum"], "model/final schema category set diverges", errors)
    require(response_schema["$defs"]["candidate_locus_state"]["enum"] == schema["$defs"]["candidate_locus_state"]["enum"], "model/final schema candidate states diverge", errors)
    require(response_schema["$defs"]["candidate_locus"]["properties"]["confidence"]["enum"] == schema["$defs"]["candidate_locus"]["properties"]["confidence"]["enum"], "model/final schema confidence enum diverges", errors)
    errors.extend(validate_model_response_payload(model_response_template))
    bad_payload = dict(model_response_template)
    bad_payload["raw_output_hash"] = "0" * 64
    require(validate_model_response_payload(bad_payload), "runtime metadata in model response was not rejected", errors)
    enriched = enrich_model_payload(model_response_template)
    errors.extend(validate_enriched_model_record(enriched))
    require("record_hash" not in model_response_template, "model response template has pre-enrichment record_hash", errors)
    require("record_hash" in enriched, "enriched model record lacks record_hash", errors)

    prompt_a_text = (PROMPTS_DIR / "condition_A.txt").read_text(encoding="utf-8")
    prompt_b_text = (PROMPTS_DIR / "condition_B.txt").read_text(encoding="utf-8")
    prompt_c_text = (PROMPTS_DIR / "condition_C.txt").read_text(encoding="utf-8")
    system_text = (PROMPTS_DIR / "system_prompt.txt").read_text(encoding="utf-8")
    user_text = (PROMPTS_DIR / "user_prompt_template.txt").read_text(encoding="utf-8")
    all_prompt_text = "\n".join([prompt_a_text, prompt_b_text, prompt_c_text, system_text, user_text, (PROMPTS_DIR / "human_researcher_instructions.txt").read_text(encoding="utf-8")])
    for phrase in [
        "candidate_loci",
        "review_policy_applied",
        "model-authored annotation payload",
        "not execution authorization",
    ]:
        require(phrase in all_prompt_text, f"prompt bundle missing required phrase: {phrase}", errors)
    for category in EXPECTED_CATEGORIES:
        require(category in prompt_c_text, f"Condition C missing category {category}", errors)
    for phrase in [
        "exactly eight structured candidate_loci entries",
        "cue_function is reserved",
        "boundary_setting and context_inference are review-sensitive",
        "context_inference requires a named, documented, protocol-permitted contextual bridge",
        "cue_function requires positive cue-family substitution evidence",
        "cannot be selected because all other categories failed",
        "BEGIN_FULL_MANUAL_JSON",
    ]:
        require(phrase in prompt_c_text, f"Condition C missing requirement: {phrase}", errors)
    require("{{SOURCE_PACKET}}" in user_text, "source packet placeholder missing", errors)
    require("{{MODEL_RESPONSE_SCHEMA}}" in user_text, "model response schema placeholder missing", errors)
    require(prompt_audit["audit_status"] == "PASSED_STATIC_PROMPT_SCHEMA_AND_ASSEMBLY_COMPATIBILITY_EXECUTION_BLOCKED", "prompt audit status mismatch", errors)

    parity = (DOCS_DIR / "pr18_prompt_parity_audit.md").read_text(encoding="utf-8")
    require("Unresolved substantive content asymmetries: none" in parity, "prompt parity unresolved asymmetry remains", errors)
    require("full authoritative JSON manual" in parity, "prompt parity does not specify human/model manual content", errors)
    manipulation = (DOCS_DIR / "pr18_condition_manipulation_audit.md").read_text(encoding="utf-8")
    require("shared structured annotation baseline with increasing levels of interpretive guidance" in manipulation, "condition manipulation name missing", errors)
    require("Condition B does not contain the full manual" in manipulation, "condition B full-manual exclusion missing", errors)
    require("Condition C receives the declared full guidance" in manipulation, "condition C full-guidance check missing", errors)
    contamination = (DOCS_DIR / "pr18_prompt_contamination_audit.md").read_text(encoding="utf-8")
    require("passage-level contamination comparison: not performed" in contamination, "contamination audit overclaims passage check", errors)
    require("semantic contamination comparison: not performed" in contamination, "contamination audit overclaims semantic check", errors)
    require("selected case IDs found in prompts: []" in contamination, "selected case IDs found in prompts", errors)
    require("manual example IDs found in prompts: []" in contamination, "manual example IDs found in prompts", errors)
    require("study source-packet paths found in prompts: False" in contamination, "source packet paths found in prompts", errors)

    for case_id in selected_ids:
        require(case_id not in all_prompt_text, f"selected case ID appears in prompts: {case_id}", errors)
    require("data/studies/human_llm_pilot/source_packets" not in all_prompt_text, "source-packet path appears in prompts", errors)
    for example_id in [
        "WEX_RESOLVED_WARRANT_ATTRIBUTION",
        "WEX_PAIR_OPERATION_ATTRIBUTION",
        "WEX_REVIEW_REQUIRED_CUE_FUNCTION_MODEL",
        "WEX_UNRESOLVED_NO_CANDIDATE",
        "WEX_CONFLICTING_OPERATION_TEMPORAL",
        "WEX_REVIEW_RECORD_FOR_CUE_FUNCTION",
    ]:
        require(example_id not in all_prompt_text, f"manual example ID appears in prompts: {example_id}", errors)

    require(freeze_pkg["base_main_commit"] == EXPECTED_MAIN_SHA, "freeze package base main mismatch", errors)
    require(freeze_pkg["pr18_head_before_update"] == "95bdabc07e0223e6836253c17982db4efcf7b6e8", "freeze package starting PR18 head mismatch", errors)
    require(freeze_pkg["manual_merge_commit"] == EXPECTED_MAIN_SHA, "freeze package manual merge mismatch", errors)
    require(freeze_pkg["manual_markdown_hash"] == EXPECTED_MANUAL["manual_markdown_sha256"], "freeze package markdown hash mismatch", errors)
    require(freeze_pkg["manual_json_hash"] == EXPECTED_MANUAL["manual_json_sha256"], "freeze package json hash mismatch", errors)
    require(freeze_pkg["manual_manifest_hash"] == EXPECTED_MANUAL["manual_manifest_sha256"], "freeze package manifest hash mismatch", errors)
    require(freeze_pkg["coder_schema_hash"] == EXPECTED_MANUAL["coder_schema_sha256"], "freeze package schema hash mismatch", errors)
    for path_key, hash_key in [
        ("prompt_assembly_spec_path", "prompt_assembly_spec_hash"),
        ("prompt_assembly_manifest_path", "prompt_assembly_manifest_hash"),
        ("model_response_schema_path", "model_response_schema_hash"),
        ("model_record_enrichment_contract_path", "model_record_enrichment_contract_hash"),
        ("human_access_spec_path", "human_access_spec_hash"),
        ("prompt_condition_manipulation_audit_path", "prompt_condition_manipulation_audit_hash"),
        ("prompt_contamination_audit_path", "prompt_contamination_audit_hash"),
        ("prompt_parity_audit_path", "prompt_parity_audit_hash"),
        ("runtime_spec_path", "runtime_spec_hash"),
        ("prompt_bundle_manifest_path", "prompt_bundle_manifest_hash"),
    ]:
        require(normalized_file_sha(ROOT / freeze_pkg[path_key]) == freeze_pkg[hash_key], f"freeze package hash mismatch for {path_key}", errors)
    require(freeze_pkg["static_prompt_schema_status"] == "PASSED_MODEL_RESPONSE_SCHEMA_COMPATIBILITY_EXECUTION_BLOCKED", "freeze package static schema status mismatch", errors)
    require(freeze_pkg["prompt_assembly_status"] == "PASSED_PROMPT_ASSEMBLY_SPECIFIED_EXECUTION_BLOCKED", "freeze package assembly status mismatch", errors)
    require(freeze_pkg["model_response_enrichment_status"] == "PASSED_CONTRACT_SPECIFIED_EXECUTION_BLOCKED", "freeze package enrichment status mismatch", errors)
    require(freeze_pkg["human_model_content_comparability_status"] == "PASSED_IDENTICAL_SOURCE_AND_MANUAL_CONTENT_WITH_DOCUMENTED_ACCESS_AFFORDANCE_ASYMMETRIES_EXECUTION_BLOCKED", "freeze package comparability status mismatch", errors)
    require(freeze_pkg["condition_manipulation_status"] == "PASSED_SHARED_BASELINE_WITH_DECLARED_INSTRUCTION_DEPTH_INCREMENTS_EXECUTION_BLOCKED", "freeze package manipulation status mismatch", errors)
    require(freeze_pkg["runtime_settings_status"] == "BLOCKED_PENDING_PROVIDER_ACCOUNT_VERIFICATION", "freeze package runtime status mismatch", errors)
    require(freeze_pkg["pricing_status"] == "BLOCKED_PENDING_PROVIDER_ACCOUNT_PRICING_RECHECK", "freeze package pricing status mismatch", errors)
    require(freeze_pkg["freeze_package_manifest_hash"] == canonical_json_hash(freeze_pkg, "freeze_package_manifest_hash"), "freeze package manifest hash mismatch", errors)
    require(freeze_pkg["execution_authorization_status"].startswith("BLOCKED"), "execution authorization is not blocked", errors)

    require(model_spec["provider"] == "OpenAI", "provider changed", errors)
    require(model_spec["original_unverified_model_id"] == "gpt-5.4-mini", "original model ID not recorded", errors)
    require(model_spec["model"] == "UNRESOLVED_PENDING_OFFICIAL_VERIFICATION", "model must remain unresolved", errors)
    require(model_spec["model_freeze_status"] == "BLOCKED", "model status must be blocked", errors)
    require(model_spec["account_availability_verified"] is False, "account availability is overstated", errors)
    require(model_spec["model_called"] is False, "model call recorded during freeze", errors)
    require(model_spec["browsing"] == "disabled", "model browsing not disabled", errors)
    require(model_spec["tools"] == "disabled", "model tools not disabled", errors)
    require(model_spec["response_format"].startswith("structured JSON required by schemas/human_llm_model_response.schema.json"), "model response schema not used in execution spec", errors)
    require(model_spec["raw_response_preservation"].startswith("exact raw response"), "raw response preservation missing", errors)
    require(model_spec["runtime_settings_status"] == "BLOCKED_PENDING_PROVIDER_ACCOUNT_VERIFICATION", "runtime settings status mismatch", errors)
    require(cost["estimated_upper_bound_cost_status"] == "not_final", "cost estimate must remain non-final", errors)
    require(cost["estimated_upper_bound_cost_usd"] is None, "cost estimate should not be final", errors)
    require(cost["total_planned_model_runs_after_human_lock"] == 118, "total planned run count mismatch", errors)

    require(
        allocation["allocation_hash"] == canonical_json_hash(allocation, "allocation_hash"),
        "allocation hash mismatch",
        errors,
    )
    require(allocation["second_human_component"] == "not_in_current_protocol", "second human component added", errors)
    require(allocation["planned_model_run_counts"]["total_planned_model_runs_after_human_lock"] == 118, "allocation total mismatch", errors)
    require(allocation["planned_model_run_counts"]["primary_run_double_counted_in_stability_runs"] is False, "primary run double-counted", errors)

    require(governance["protocol_design"] == "Design B", "governance protocol design mismatch", errors)
    require(governance["external_human_recruitment"] == "prohibited", "external recruitment not prohibited", errors)
    require(governance["participant_data_collection"] == "none", "participant data collection unexpectedly present", errors)
    require(governance["formal_ethics_exemption_claimed"] is False, "formal ethics exemption is claimed", errors)
    require(governance["overall_execution_readiness"] == "BLOCKED", "governance readiness must be blocked", errors)

    require(freeze_status["overall_execution_readiness"].startswith("BLOCKED"), "overall readiness must be blocked", errors)
    require(freeze_status["manual_compatibility_status"] == "PASSED_AUTHORITATIVE_MANUAL_REFERENCE_VERIFIED", "manual status mismatch", errors)
    require(freeze_status["static_prompt_schema_status"] == "PASSED_MODEL_RESPONSE_SCHEMA_COMPATIBILITY_EXECUTION_BLOCKED", "static prompt/schema status mismatch", errors)
    require(freeze_status["prompt_assembly_status"] == "PASSED_PROMPT_ASSEMBLY_SPECIFIED_EXECUTION_BLOCKED", "prompt assembly status mismatch", errors)
    require(freeze_status["model_response_enrichment_status"] == "PASSED_CONTRACT_SPECIFIED_EXECUTION_BLOCKED", "model response enrichment status mismatch", errors)
    require(freeze_status["human_model_content_comparability_status"] == "PASSED_IDENTICAL_SOURCE_AND_MANUAL_CONTENT_WITH_DOCUMENTED_ACCESS_AFFORDANCE_ASYMMETRIES_EXECUTION_BLOCKED", "human/model content comparability status mismatch", errors)
    require(freeze_status["condition_manipulation_status"] == "PASSED_SHARED_BASELINE_WITH_DECLARED_INSTRUCTION_DEPTH_INCREMENTS_EXECUTION_BLOCKED", "condition manipulation status mismatch", errors)
    require(freeze_status["prompt_compatibility_status"].startswith("BLOCKED"), "prompt status should remain blocked", errors)
    require(freeze_status["rights_freeze_status"] == "BLOCKED_RIGHTS_REVIEW_REQUIRED", "rights freeze status mismatch", errors)
    require(freeze_status["private_packet_status"].startswith("BLOCKED"), "private packet status mismatch", errors)
    require(freeze_status["model_account_status"].startswith("BLOCKED"), "model account status mismatch", errors)
    require(freeze_status["runtime_settings_status"] == "BLOCKED_PENDING_PROVIDER_ACCOUNT_VERIFICATION", "runtime settings status should be blocked", errors)
    require(freeze_status["pricing_status"] == "BLOCKED_PENDING_PROVIDER_ACCOUNT_PRICING_RECHECK", "pricing status should be blocked", errors)
    require(freeze_status["execution_authorization_status"].startswith("BLOCKED"), "execution authorization should be blocked", errors)
    require(freeze_status["human_coding_occurred"] is False, "human coding occurred", errors)
    require(freeze_status["model_called"] is False, "model called", errors)
    require(freeze_status["results_generated"] is False, "results generated", errors)

    freeze_report = (DOCS_DIR / "human_llm_pilot_freeze_report.md").read_text(encoding="utf-8")
    for phrase in [
        "overall_execution_readiness: `BLOCKED_PENDING_RIGHTS_PRIVATE_PACKETS_MODEL_ACCOUNT_RUNTIME_SETTINGS_PRICING_AND_FINAL_EXECUTION_AUTHORIZATION`",
        "Manual status: `AUTHORITATIVE_FOR_PROTOCOL_REVIEW`",
        "Manual compatibility: passed.",
        "Static prompt/schema compatibility: passed for the model-authored response schema.",
        "Prompt assembly: specified, hashable, and non-self-referential; execution still blocked.",
        "Assembled prompt hash: harness-only metadata, not model-visible.",
        "Model response candidate coverage: exact eight-category set enforced.",
        "Model response enrichment contract: specified.",
        "Private packets inspected in this task: no.",
        "Released walkthrough artifacts modified: no.",
    ]:
        require(phrase in freeze_report, f"freeze report missing boundary: {phrase}", errors)

    checklist = (DOCS_DIR / "human_llm_protocol_freeze_checklist.md").read_text(encoding="utf-8")
    for complete in [
        "- [x] Authoritative current Design B friction_locus manual referenced for protocol review.",
        "- [x] Prompt bundle rebuilt for static schema compatibility and deterministic assembly.",
        "- [x] Deterministic prompt assembly specified.",
        "- [x] Model-authored payload separated from harness metadata.",
        "- [x] Human manual access specified.",
        "- [x] A/B/C manipulation boundary renamed and frozen.",
    ]:
        require(complete in checklist, f"checklist missing completed item: {complete}", errors)
    for incomplete in [
        "- [ ] Prompts A/B/C frozen as executable.",
        "- [ ] Account-verified model and decoding parameters frozen.",
        "- [ ] Researcher records completed.",
        "- [ ] Run manifests populated.",
        "- [ ] Raw-output hashes computed immediately after receipt.",
    ]:
        require(incomplete in checklist, f"checklist incorrectly marks item complete: {incomplete}", errors)

    for path in DATA_DIR.rglob("*"):
        if path.is_file():
            lowered = path.name.lower()
            require(
                not any(token in lowered for token in FORBIDDEN_FREEZE_FILE_TOKENS),
                f"empirical/result-shaped file found in freeze data: {path.relative_to(ROOT)}",
                errors,
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("human_llm_pilot_freeze_validation: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
