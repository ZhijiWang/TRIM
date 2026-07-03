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
    freeze_pkg = load_json(DATA_DIR / "freeze_package_manifest.json")
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
    require(prompts["prompt_compatibility_status"] == "PASSED_SCHEMA_AND_MANUAL_COMPATIBILITY_EXECUTION_BLOCKED", "prompt compatibility status mismatch", errors)
    require(prompts["condition_C_status"].startswith("CONDITION_C_REBUILT_COMPATIBLE"), "Condition C status mismatch", errors)
    require(prompts["browsing_status"] == "disabled", "browsing must be disabled", errors)
    require(prompts["tool_status"] == "disabled", "tools must be disabled", errors)

    prompt_a_text = (PROMPTS_DIR / "condition_A.txt").read_text(encoding="utf-8")
    prompt_b_text = (PROMPTS_DIR / "condition_B.txt").read_text(encoding="utf-8")
    prompt_c_text = (PROMPTS_DIR / "condition_C.txt").read_text(encoding="utf-8")
    system_text = (PROMPTS_DIR / "system_prompt.txt").read_text(encoding="utf-8")
    user_text = (PROMPTS_DIR / "user_prompt_template.txt").read_text(encoding="utf-8")
    all_prompt_text = "\n".join([prompt_a_text, prompt_b_text, prompt_c_text, system_text, user_text, (PROMPTS_DIR / "human_researcher_instructions.txt").read_text(encoding="utf-8")])
    for phrase in [
        "candidate_loci",
        "review_policy_applied",
        "review_of_record_id",
        "review_of_record_hash",
        "final_operational_label",
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
    ]:
        require(phrase in prompt_c_text, f"Condition C missing requirement: {phrase}", errors)
    require("{{SOURCE_PACKET}}" in user_text, "source packet placeholder missing", errors)
    require("{{OUTPUT_SCHEMA}}" in user_text, "output schema placeholder missing", errors)
    require(prompt_audit["audit_status"] == "PASSED_MANUAL_COMPATIBILITY_EXECUTION_BLOCKED", "prompt audit status mismatch", errors)

    parity = (DOCS_DIR / "pr18_prompt_parity_audit.md").read_text(encoding="utf-8")
    require("Unresolved substantive asymmetries: none" in parity, "prompt parity unresolved asymmetry remains", errors)
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
    require(freeze_pkg["pr18_head_before_update"] == EXPECTED_PR18_START_SHA, "freeze package starting PR18 head mismatch", errors)
    require(freeze_pkg["manual_merge_commit"] == EXPECTED_MAIN_SHA, "freeze package manual merge mismatch", errors)
    require(freeze_pkg["manual_markdown_hash"] == EXPECTED_MANUAL["manual_markdown_sha256"], "freeze package markdown hash mismatch", errors)
    require(freeze_pkg["manual_json_hash"] == EXPECTED_MANUAL["manual_json_sha256"], "freeze package json hash mismatch", errors)
    require(freeze_pkg["manual_manifest_hash"] == EXPECTED_MANUAL["manual_manifest_sha256"], "freeze package manifest hash mismatch", errors)
    require(freeze_pkg["coder_schema_hash"] == EXPECTED_MANUAL["coder_schema_sha256"], "freeze package schema hash mismatch", errors)
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
    require(freeze_status["prompt_compatibility_status"] == "PASSED_SCHEMA_AND_MANUAL_COMPATIBILITY_EXECUTION_BLOCKED", "prompt status mismatch", errors)
    require(freeze_status["rights_freeze_status"] == "BLOCKED_RIGHTS_REVIEW_REQUIRED", "rights freeze status mismatch", errors)
    require(freeze_status["private_packet_status"].startswith("BLOCKED"), "private packet status mismatch", errors)
    require(freeze_status["model_account_status"].startswith("BLOCKED"), "model account status mismatch", errors)
    require(freeze_status["execution_authorization_status"].startswith("BLOCKED"), "execution authorization should be blocked", errors)
    require(freeze_status["human_coding_occurred"] is False, "human coding occurred", errors)
    require(freeze_status["model_called"] is False, "model called", errors)
    require(freeze_status["results_generated"] is False, "results generated", errors)

    freeze_report = (DOCS_DIR / "human_llm_pilot_freeze_report.md").read_text(encoding="utf-8")
    for phrase in [
        "overall_execution_readiness: `BLOCKED_PENDING_RIGHTS_PRIVATE_PACKETS_MODEL_ACCOUNT_AND_FINAL_EXECUTION_AUTHORIZATION`",
        "Manual status: `AUTHORITATIVE_FOR_PROTOCOL_REVIEW`",
        "Manual compatibility: passed.",
        "Prompt/schema compatibility: passed.",
        "Private packets inspected in this task: no.",
        "Released walkthrough artifacts modified: no.",
    ]:
        require(phrase in freeze_report, f"freeze report missing boundary: {phrase}", errors)

    checklist = (DOCS_DIR / "human_llm_protocol_freeze_checklist.md").read_text(encoding="utf-8")
    for complete in [
        "- [x] Authoritative current Design B friction_locus manual referenced for protocol review.",
        "- [x] Prompt bundle rebuilt for manual/schema compatibility.",
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
