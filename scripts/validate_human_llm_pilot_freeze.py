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

EXPECTED_MAIN_SHA = "6998175eeca5d349072bf31012c69f2d568f28ec"
EXPECTED_SAMPLE_SIZE = 25
EXPECTED_LAYER_COUNTS = {"Layer 1": 15, "Layer 2": 10}
EXPECTED_TERMINAL_COUNTS = {
    "selected": 25,
    "eligible_not_selected": 1,
    "ineligible": 4,
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
    source_rows = read_csv(DATA_DIR / "source_manifest.csv")
    rights_rows = read_csv(DATA_DIR / "source_rights_manifest.csv")
    substantive_rows = read_csv(DATA_DIR / "source_packet_substantive_audit.csv")
    familiarity_rows = read_csv(DATA_DIR / "researcher_familiarity_audit.csv")
    selection_rows = read_csv(DOCS_DIR / "human_llm_sample_selection_log.csv")

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
    require(
        sample["selection_log_hash"] == normalized_file_sha(DOCS_DIR / "human_llm_sample_selection_log.csv"),
        "selection-log hash mismatch",
        errors,
    )
    require(
        sample["source_manifest_hash"] == normalized_file_sha(DATA_DIR / "source_manifest.csv"),
        "source-manifest hash mismatch",
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
        require(
            packet["canonical_text_publication_status"] == "not_in_public_repository",
            f"{case_id}: canonical text publication status not redacted",
            errors,
        )
        require(
            packet["public_redistribution_status"] == "not_confirmed_pending_rights_review",
            f"{case_id}: redistribution status is overstated",
            errors,
        )
        require(
            packet["repository_publication_status"] == "metadata_only_text_redacted",
            f"{case_id}: repository publication status is not metadata-only",
            errors,
        )
        require(
            packet["controlled_storage_reference"].startswith("controlled_private_study_storage/"),
            f"{case_id}: controlled storage reference missing or unsafe",
            errors,
        )
        require(
            packet["text_layer_visibility"]["researcher_and_model_identical"] is True,
            f"{case_id}: researcher/model text layers differ",
            errors,
        )
        require(
            packet["text_layer_visibility"]["secondary_scholarship_visible"] is False,
            f"{case_id}: secondary scholarship is visible",
            errors,
        )
        require(
            packet["text_layer_visibility"]["model_facing_instructions_included"] is False,
            f"{case_id}: packet contains model-facing instructions",
            errors,
        )
        require(
            all(segment.get("text_status") == "redacted_from_public_pr_pending_rights_review" for segment in packet["segments"]),
            f"{case_id}: segment text is not redacted",
            errors,
        )
        require(
            rights_row["public_redistribution_status"] == "not_confirmed_pending_rights_review",
            f"{case_id}: rights row overstates redistribution clearance",
            errors,
        )
        require(
            rights_row["repository_publication_status"] == "metadata_only_text_redacted",
            f"{case_id}: rights row does not preserve public redaction",
            errors,
        )
        require(
            substantive_row["failure"] == "none_public_execution_blocked_by_rights_redaction",
            f"{case_id}: substantive audit failure: {substantive_row['failure']}",
            errors,
        )
        if packet["inclusion_layer"] == "Layer 1":
            log_row = selected_log_rows[case_id]
            require(log_row["prior_demo_use"] == "no", f"{case_id}: held-out case has demo use", errors)
            require(log_row["prior_manual_use"] == "no", f"{case_id}: held-out case has manual use", errors)
            require(
                log_row["manual_development_influence"] != "direct",
                f"{case_id}: held-out case directly influenced manual",
                errors,
            )
        require(
            "no friction_locus labels inferred or used"
            in selected_log_rows[case_id]["label_information_visible_at_selection"],
            f"{case_id}: selection log exposes label information",
            errors,
        )

    familiarity_levels = {row["researcher_familiarity_level"] for row in familiarity_rows}
    require(len(familiarity_levels) >= 3, "familiarity audit still uses a blanket value", errors)
    require("casual_familiarity" not in familiarity_levels, "old blanket familiarity value remains", errors)

    require(manual["repository_commit"] == EXPECTED_MAIN_SHA, "manual commit mismatch", errors)
    require(manual["manual_path"] is None, "manual path should be unresolved", errors)
    require(manual["manual_file_hash"] is None, "manual hash should be unresolved", errors)
    require(
        manual["manual_freeze_status"] == "BLOCKED_INCOMPLETE_AUTHORITATIVE_MANUAL",
        "manual status must be blocked",
        errors,
    )
    for key in ["predicted_confusions", "category_definitions", "schema"]:
        require(
            normalized_file_sha(ROOT / manual[f"{key}_path"]) == manual[f"{key}_hash"],
            f"{key} hash mismatch",
            errors,
        )

    schema = load_json(ROOT / manual["schema_path"])
    schema_categories = set(schema["$defs"]["friction_locus"]["enum"])
    lineage_rows = read_csv(ROOT / manual["category_definitions_path"])
    lineage_categories = {row["TRIM category"] for row in lineage_rows}
    predicted_rows = read_csv(ROOT / manual["predicted_confusions_path"])
    substantive_categories = {item for item in schema_categories if item not in {"unresolved", None}}
    require(len(substantive_categories) == 8, "schema must retain eight substantive friction_locus values", errors)
    for row in predicted_rows:
        pair = row["category pair"]
        left, sep, right = pair.partition(" -> ")
        require(bool(sep), f"malformed predicted-confusion pair: {pair}", errors)
        require(left in schema_categories, f"predicted-confusion category missing from schema: {left}", errors)
        require(right in schema_categories, f"predicted-confusion category missing from schema: {right}", errors)
        require(left in lineage_categories, f"predicted-confusion category missing from lineage table: {left}", errors)
        require(right in lineage_categories, f"predicted-confusion category missing from lineage table: {right}", errors)

    for key in [
        "system_prompt",
        "user_prompt_template",
        "condition_A",
        "condition_B",
        "condition_C",
        "output_schema",
    ]:
        path_key = f"{key}_path"
        hash_key = f"{key}_hash"
        require(
            normalized_file_sha(ROOT / prompts[path_key]) == prompts[hash_key],
            f"{key} hash mismatch",
            errors,
        )
    require(prompts["prompt_bundle_status"] == "BLOCKED_NOT_EXECUTION_READY", "prompt bundle must be blocked", errors)
    require(prompts["condition_C_status"] == "BLOCKED_INCOMPLETE_AUTHORITATIVE_MANUAL", "Condition C must be blocked", errors)
    require(prompts["browsing_status"] == "disabled", "browsing must be disabled", errors)
    require(prompts["tool_status"] == "disabled", "tools must be disabled", errors)
    require(prompt_audit["audit_status"] == "BLOCKED", "prompt audit must be blocked", errors)
    for prompt_name in ["condition_A.txt", "condition_B.txt", "condition_C.txt"]:
        text = (PROMPTS_DIR / prompt_name).read_text(encoding="utf-8")
        require("BLOCKED_NOT_EXECUTION_READY" in text, f"{prompt_name} lacks blocked status", errors)
    require("{{SOURCE_PACKET}}" in (PROMPTS_DIR / "user_prompt_template.txt").read_text(encoding="utf-8"), "source packet placeholder missing", errors)
    require("{{OUTPUT_SCHEMA}}" in (PROMPTS_DIR / "user_prompt_template.txt").read_text(encoding="utf-8"), "output schema placeholder missing", errors)

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
    require(
        allocation["sample_manifest_hash"] == sample["sample_manifest_hash"],
        "allocation references wrong sample hash",
        errors,
    )
    require(allocation["second_human_component"] == "not_in_current_protocol", "second human component added", errors)
    require(allocation["planned_model_run_counts"]["primary_condition_C_runs"] == 25, "primary run count mismatch", errors)
    require(allocation["planned_model_run_counts"]["stability_runs_additional_beyond_primary"] == 75, "stability run count mismatch", errors)
    require(allocation["planned_model_run_counts"]["ablation_condition_runs"] == 18, "ablation run count mismatch", errors)
    require(allocation["planned_model_run_counts"]["total_planned_model_runs_after_human_lock"] == 118, "allocation total mismatch", errors)
    require(allocation["planned_model_run_counts"]["primary_run_double_counted_in_stability_runs"] is False, "primary run double-counted", errors)
    require("before human lock" in allocation["condition_assignment"]["visibility_constraints"], "allocation must prohibit model execution before human lock", errors)

    require(governance["protocol_design"] == "Design B", "governance protocol design mismatch", errors)
    require(governance["external_human_recruitment"] == "prohibited", "external recruitment not prohibited", errors)
    require(governance["participant_data_collection"] == "none", "participant data collection unexpectedly present", errors)
    require(governance["formal_ethics_exemption_claimed"] is False, "formal ethics exemption is claimed", errors)
    require(governance["overall_execution_readiness"] == "BLOCKED", "governance readiness must be blocked", errors)

    require(freeze_status["overall_execution_readiness"] == "BLOCKED", "overall readiness must be blocked", errors)
    require(freeze_status["manual_freeze_status"] == "BLOCKED_INCOMPLETE_AUTHORITATIVE_MANUAL", "manual freeze status mismatch", errors)
    require(freeze_status["rights_freeze_status"] == "BLOCKED_RIGHTS_REVIEW_REQUIRED", "rights freeze status mismatch", errors)
    require(freeze_status["model_freeze_status"].startswith("BLOCKED"), "model freeze status mismatch", errors)
    require(freeze_status["human_coding_occurred"] is False, "human coding occurred", errors)
    require(freeze_status["model_called"] is False, "model called", errors)
    require(freeze_status["results_generated"] is False, "results generated", errors)

    freeze_report = (DOCS_DIR / "human_llm_pilot_freeze_report.md").read_text(encoding="utf-8")
    for phrase in [
        "overall_execution_readiness: `BLOCKED`",
        "Manual status: `BLOCKED_INCOMPLETE_AUTHORITATIVE_MANUAL`",
        "Public source packets now contain metadata only.",
        "Model called: no.",
        "Released walkthrough artifacts modified: no.",
    ]:
        require(phrase in freeze_report, f"freeze report missing boundary: {phrase}", errors)

    checklist = (DOCS_DIR / "human_llm_protocol_freeze_checklist.md").read_text(encoding="utf-8")
    for incomplete in [
        "- [ ] Authoritative current Design B friction_locus manual frozen.",
        "- [ ] Prompts A/B/C frozen as executable.",
        "- [ ] Account-verified model and decoding parameters frozen.",
        "- [ ] Researcher records completed.",
        "- [ ] Run manifests populated.",
        "- [ ] Raw-output hashes computed immediately after receipt.",
        "- [ ] Stability-run completion recorded.",
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
