"""Validate the frozen Design B human-LLM pilot preparation materials."""

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
FORBIDDEN_PACKET_FIELDS = {
    "expected_label",
    "friction_locus",
    "manual_hint",
    "model_facing_instruction",
    "model_output",
    "primary_label",
    "researcher_interpretation",
    "secondary_scholarship",
}
FORBIDDEN_FREEZE_FILE_TOKENS = {
    "agreement",
    "findings",
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


def text_sha(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return sha_bytes(normalized)


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
    source_rows = read_csv(DATA_DIR / "source_manifest.csv")
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
        allocation["allocation_hash"] == canonical_json_hash(allocation, "allocation_hash"),
        "allocation hash mismatch",
        errors,
    )
    require(
        allocation["sample_manifest_hash"] == sample["sample_manifest_hash"],
        "allocation references wrong sample hash",
        errors,
    )
    require(
        allocation["second_human_component"] == "not_in_current_protocol",
        "allocation unexpectedly includes second human component",
        errors,
    )
    require(
        "before human lock" in allocation["condition_assignment"]["visibility_constraints"],
        "allocation must prohibit model execution before human lock",
        errors,
    )

    source_by_case = {row["case_id"]: row for row in source_rows}
    require(set(source_by_case) == set(selected_ids), "source manifest and sample disagree", errors)
    selected_log_rows = {
        row["candidate_id"]: row
        for row in selection_rows
        if row["inclusion_status"] == "selected"
    }
    excluded_log_ids = {
        row["candidate_id"]
        for row in selection_rows
        if row["inclusion_status"] != "selected"
    }
    require(set(selected_log_rows) == set(selected_ids), "selection log and sample disagree", errors)
    require(not (excluded_log_ids & set(selected_ids)), "excluded case appears in final sample", errors)

    for case_id in selected_ids:
        packet_path = ROOT / source_by_case[case_id]["source_packet_path"]
        packet = load_json(packet_path)
        manifest_row = source_by_case[case_id]
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
            text_sha(packet["canonical_text"]) == manifest_row["canonical_text_sha256"],
            f"{case_id}: canonical text hash mismatch",
            errors,
        )
        if packet["translation_or_gloss"]:
            require(
                text_sha(packet["translation_or_gloss"]) == manifest_row["translation_gloss_sha256"],
                f"{case_id}: translation/gloss hash mismatch",
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
            "unclear" not in packet["rights_status"],
            f"{case_id}: rights status remains unclear",
            errors,
        )
        require(
            not (FORBIDDEN_PACKET_FIELDS & set(packet)),
            f"{case_id}: empirical or interpretive fields appear in packet",
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

    require(
        normalized_file_sha(ROOT / manual["manual_path"]) == manual["manual_file_hash"],
        "manual file hash mismatch",
        errors,
    )
    require(manual["repository_commit"] == EXPECTED_MAIN_SHA, "manual commit mismatch", errors)
    require(
        normalized_file_sha(ROOT / manual["predicted_confusions_path"])
        == manual["predicted_confusions_hash"],
        "predicted-confusions hash mismatch",
        errors,
    )
    require(
        normalized_file_sha(ROOT / manual["schema_path"]) == manual["schema_hash"],
        "manual schema hash mismatch",
        errors,
    )
    require(
        normalized_file_sha(ROOT / manual["category_definitions_path"])
        == manual["category_definitions_hash"],
        "category-definition hash mismatch",
        errors,
    )
    schema = load_json(ROOT / manual["schema_path"])
    schema_categories = set(schema["$defs"]["friction_locus"]["enum"])
    lineage_rows = read_csv(ROOT / manual["category_definitions_path"])
    lineage_categories = {row["TRIM category"] for row in lineage_rows}
    predicted_rows = read_csv(ROOT / manual["predicted_confusions_path"])
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
    require(prompts["browsing_status"] == "disabled", "browsing must be disabled", errors)
    require(prompts["tool_status"] == "disabled", "tools must be disabled", errors)
    require("{{SOURCE_PACKET}}" in (PROMPTS_DIR / "user_prompt_template.txt").read_text(encoding="utf-8"), "source packet placeholder missing", errors)
    require("{{OUTPUT_SCHEMA}}" in (PROMPTS_DIR / "user_prompt_template.txt").read_text(encoding="utf-8"), "output schema placeholder missing", errors)

    require(model_spec["provider"] == "OpenAI", "provider is unresolved", errors)
    require(model_spec["model"], "model is unresolved", errors)
    require(model_spec["browsing"] == "disabled", "model browsing not disabled", errors)
    require(model_spec["tools"] == "disabled", "model tools not disabled", errors)
    require(cost["hard_spending_ceiling_usd"] >= cost["estimated_upper_bound_cost_usd"], "cost ceiling below estimate", errors)
    require(
        governance["protocol_design"] == "Design B",
        "governance protocol design mismatch",
        errors,
    )
    require(
        governance["external_human_recruitment"] == "prohibited",
        "external recruitment not prohibited",
        errors,
    )
    require(
        governance["participant_data_collection"] == "none",
        "participant data collection unexpectedly present",
        errors,
    )
    require(
        governance["formal_ethics_exemption_claimed"] is False,
        "formal ethics exemption is claimed",
        errors,
    )

    freeze_report = (DOCS_DIR / "human_llm_pilot_freeze_report.md").read_text(encoding="utf-8")
    for phrase in [
        "Human coding occurred: no.",
        "Model called: no.",
        "Model outputs created: no.",
        "Findings generated: no.",
        "Released walkthrough artifacts modified: no.",
    ]:
        require(phrase in freeze_report, f"freeze report missing boundary: {phrase}", errors)

    checklist = (DOCS_DIR / "human_llm_protocol_freeze_checklist.md").read_text(encoding="utf-8")
    for incomplete in [
        "- [ ] Researcher records completed.",
        "- [ ] Human record hashes computed and verified.",
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
