"""Validate the authoritative friction_locus manual v0.1 artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANUAL_DIR = ROOT / "docs" / "manuals"
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


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def pr18_selected_ids() -> list[str]:
    raw = subprocess.check_output(
        [
            "git",
            "show",
            "origin/research/human-llm-pilot-freeze:data/studies/human_llm_pilot/sample_manifest.json",
        ],
        cwd=ROOT,
        text=True,
    )
    return load_json_from_text(raw)["selected_case_ids"]


def load_json_from_text(text: str) -> dict[str, Any]:
    return json.loads(text)


def validate() -> list[str]:
    errors: list[str] = []
    manifest = load_json(MANUAL_DIR / "friction_locus_manual_manifest.json")
    manual_json = load_json(MANUAL_DIR / "friction_locus_manual_v0_1.json")
    markdown = (MANUAL_DIR / "friction_locus_manual_v0_1.md").read_text(encoding="utf-8")
    schema = load_json(ROOT / "schemas" / "human_llm_coder_output.schema.json")
    predicted_rows = read_csv(ROOT / "docs" / "studies" / "predicted_confusions.csv")
    provenance_rows = read_csv(MANUAL_DIR / "friction_locus_provenance_matrix.csv")

    require(manual_json["manual_status"] == "AUTHORITATIVE_FOR_PROTOCOL_REVIEW", "manual status mismatch", errors)
    require(manual_json["category_order"] == EXPECTED_CATEGORIES, "category order mismatch", errors)
    require(set(manual_json["categories"]) == set(EXPECTED_CATEGORIES), "category set mismatch", errors)

    required_category_fields = [
        "definition",
        "analytic_question",
        "use_when",
        "do_not_use_when",
        "use_another_value_when",
        "positive_indicators",
        "exclusion_indicators",
        "confusable_with",
        "counterfactual_tests",
        "decision_consequence",
        "escalation_condition",
        "examples",
        "provenance_note",
    ]
    all_test_ids: list[str] = []
    for category in EXPECTED_CATEGORIES:
        require(f"### `{category}`" in markdown, f"markdown missing section for {category}", errors)
        payload = manual_json["categories"][category]
        for field in required_category_fields:
            require(bool(payload.get(field)), f"{category}: blank required field {field}", errors)
        require(payload["use_when"], f"{category}: missing use_when", errors)
        require(payload["use_another_value_when"], f"{category}: missing use_another_value_when", errors)
        require(payload["counterfactual_tests"], f"{category}: missing counterfactual test", errors)
        require(payload["examples"]["positive"]["provenance"] == "artificial_minimal_example_not_study_sample", f"{category}: positive example provenance invalid", errors)
        require(payload["examples"]["near_miss"]["provenance"] == "artificial_minimal_example_not_study_sample", f"{category}: near-miss example provenance invalid", errors)
        for other in payload["confusable_with"]:
            require(other in EXPECTED_CATEGORIES, f"{category}: invalid confusable category {other}", errors)
        for test in payload["counterfactual_tests"]:
            all_test_ids.append(test["test_id"])
            for field in ["test_id", "question", "answer_states"]:
                require(bool(test.get(field)), f"{category}: blank test field {field}", errors)
    require(len(all_test_ids) == len(set(all_test_ids)), "duplicate test IDs", errors)

    schema_values = set(schema["$defs"]["friction_locus"]["enum"])
    for category in EXPECTED_CATEGORIES:
        require(category in schema_values, f"schema does not accept {category}", errors)
    require("unresolved" in schema_values, "schema does not accept unresolved", errors)
    require(
        "requires_human_review"
        in schema["$defs"]["shared_record"]["properties"]["friction_locus_operational_status"]["enum"],
        "schema lacks requires_human_review",
        errors,
    )
    require("alternative_pathways" in schema["$defs"]["shared_record"]["properties"], "schema lacks alternative_pathways", errors)
    require("counterfactual_tests" in schema["$defs"]["shared_record"]["properties"], "schema lacks counterfactual_tests", errors)

    reachable = set()
    for node in manual_json["decision_tree"]["nodes"]:
        for edge in ["yes", "no", "terminal"]:
            target = node.get(edge)
            if target in EXPECTED_CATEGORIES or target == "unresolved":
                reachable.add(target)
    require(set(EXPECTED_CATEGORIES).issubset(reachable), f"decision tree does not reach all categories: {reachable}", errors)
    require("unresolved" in reachable, "decision tree lacks unresolved path", errors)

    manual_pairs = {item["pair"] for item in manual_json["pairwise_disambiguation"]}
    for row in predicted_rows:
        require(row["category pair"] in manual_pairs, f"predicted pair missing from manual: {row['category pair']}", errors)
    for item in manual_json["pairwise_disambiguation"]:
        left, _, right = item["pair"].partition(" -> ")
        require(left in EXPECTED_CATEGORIES and right in EXPECTED_CATEGORIES, f"invalid manual pair: {item['pair']}", errors)
        require(item["test"], f"missing pairwise test: {item['pair']}", errors)

    required_provenance_fields = [
        "manual_component",
        "category",
        "source_path",
        "source_commit",
        "source_status",
        "inherited_wording",
        "revised_wording",
        "revision_reason",
        "unresolved_conflict",
        "authority_decision",
    ]
    require(provenance_rows, "empty provenance matrix", errors)
    for row in provenance_rows:
        for field in required_provenance_fields:
            require(row.get(field, "") != "", f"blank provenance field {field}", errors)
    provenance_categories = {row["category"] for row in provenance_rows}
    require(set(EXPECTED_CATEGORIES).issubset(provenance_categories), "provenance missing category rows", errors)

    for key in [
        ("markdown_path", "markdown_hash"),
        ("json_path", "json_hash"),
        ("source_inventory_path", "source_inventory_hash"),
        ("provenance_matrix_path", "provenance_matrix_hash"),
        ("predicted_confusion_audit_path", "predicted_confusion_audit_hash"),
        ("contamination_audit_path", "contamination_audit_hash"),
    ]:
        path = ROOT / manifest[key[0]]
        require(normalized_sha256(path) == manifest[key[1]], f"manifest hash mismatch for {path}", errors)

    ids = pr18_selected_ids()
    authoritative_text = markdown + "\n" + json.dumps(manual_json, ensure_ascii=False)
    for case_id in ids:
        require(case_id not in authoritative_text, f"selected PR #18 case ID appears in manual: {case_id}", errors)
    require(not re.search(r"\bL[12]_[A-Z0-9_]+", authoritative_text), "L1_/L2_ case-like ID appears in manual", errors)
    require("data/studies/human_llm_pilot/source_packets" not in authoritative_text, "study source packet path appears in manual", errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("friction_locus_manual_validation: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
