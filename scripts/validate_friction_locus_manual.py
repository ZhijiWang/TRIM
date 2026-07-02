"""Validate the friction_locus manual v0.1 repair draft artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
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
EXPECTED_STATUS = "DRAFT_INCOMPLETE"
EXPECTED_SYNTHESIS_IDS = {
    "SYN_V0_1_DECISION_CANDIDATES",
    "SYN_V0_1_DOMINANCE_RESOLUTION",
    "SYN_V0_1_TIE_HANDLING",
    "SYN_V0_1_CONFLICTING_TESTS",
    "SYN_V0_1_REVIEW_POLICY",
    "SYN_V0_1_PROPOSED_FINAL_SEPARATION",
    "SYN_V0_1_SPEAKER_BOUNDARY_SPLIT",
    "SYN_V0_1_OPERATION_ATTRIBUTION_TWO_CF",
    "SYN_V0_1_CONTEXT_POSITIVE_EVIDENCE",
    "SYN_V0_1_WORKED_EXAMPLES",
    "SYN_V0_1_MANIFEST_FREEZE",
    "SYN_V0_1_SCHEMA_CONSTRAINTS",
}
PR18_SELECTED_IDS = [
    "L1_AUSTEN_PNP_001",
    "L1_SHELLEY_FRANK_001",
    "L1_DICKENS_GE_001",
    "L1_BRONTE_JE_001",
    "L1_WILDE_DG_001",
    "L1_JAMES_TS_001",
    "L1_STEVENSON_JH_001",
    "L1_POE_TELLTALE_001",
    "L1_HAWTHORNE_SL_001",
    "L1_CHOPIN_AWAKENING_001",
    "L1_HARDY_TESS_001",
    "L1_MELVILLE_BARTLEBY_001",
    "L1_WHARTON_MIRTH_001",
    "L1_COLLINS_MOONSTONE_001",
    "L1_CONRAD_SECRET_001",
    "L2_HOMER_ODYSSEY_001",
    "L2_SOPHOCLES_ANTIGONE_001",
    "L2_HERODOTUS_SCYTHIAN_001",
    "L2_BIBLE_GENESIS_001",
    "L2_BIBLE_SAMUEL_001",
    "L2_AESOP_001",
    "L2_OVID_DAPHNE_001",
    "L2_MALORY_MORTE_001",
    "L2_BEOWULF_DRAGON_001",
    "L2_ARABIAN_NIGHTS_001",
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


def resolve_for_test(candidate_set: list[str], conflict: bool = False) -> tuple[str, bool]:
    """Tiny validator model for the documented dominance rules."""
    if conflict:
        return "unresolved", True
    unique = list(dict.fromkeys(candidate_set))
    if not unique:
        return "unresolved", True
    if len(unique) == 1:
        return unique[0], False
    if len(unique) == 2:
        return "requires_pairwise_resolution", False
    return "unresolved", True


def validate() -> list[str]:
    errors: list[str] = []
    manifest = load_json(MANUAL_DIR / "friction_locus_manual_manifest.json")
    manual = load_json(MANUAL_DIR / "friction_locus_manual_v0_1.json")
    markdown = (MANUAL_DIR / "friction_locus_manual_v0_1.md").read_text(encoding="utf-8")
    contamination = (MANUAL_DIR / "friction_locus_sample_contamination_audit.md").read_text(encoding="utf-8")
    schema_audit = (MANUAL_DIR / "friction_locus_schema_compatibility_audit.md").read_text(encoding="utf-8")
    schema = load_json(ROOT / "schemas" / "human_llm_coder_output.schema.json")
    predicted_rows = read_csv(ROOT / "docs" / "studies" / "predicted_confusions.csv")
    provenance_rows = read_csv(MANUAL_DIR / "friction_locus_provenance_matrix.csv")

    require(manifest["manual_status"] == EXPECTED_STATUS, "manifest manual status must be DRAFT_INCOMPLETE", errors)
    require(manual["manual_status"] == EXPECTED_STATUS, "JSON manual status must be DRAFT_INCOMPLETE", errors)
    require("Status: `DRAFT_INCOMPLETE`" in markdown, "Markdown manual status must be DRAFT_INCOMPLETE", errors)
    require(manual["category_order"] == EXPECTED_CATEGORIES, "category order mismatch", errors)
    require(set(manual["categories"]) == set(EXPECTED_CATEGORIES), "category set mismatch", errors)

    schema_values = set(schema["$defs"]["friction_locus"]["enum"])
    for category in EXPECTED_CATEGORIES:
        require(category in schema_values, f"schema does not accept {category}", errors)
    require("unresolved" in schema_values, "schema does not accept unresolved", errors)

    governance_fields = manual["governance_model"]["fields"]
    for field in [
        "proposed_locus",
        "operational_status",
        "final_operational_label",
        "escalation_required",
        "review_policy",
        "original_record_preserved",
    ]:
        require(field in governance_fields, f"governance model missing {field}", errors)
    for phrase in [
        "Human proposal, model proposal, and post-review decision are distinct events.",
        "A model proposal never autonomously approves a review-required value.",
        "unresolved as final_operational_label is distinct from a substantive proposed_locus.",
    ]:
        require(phrase in manual["governance_model"]["rules"], f"governance rule missing: {phrase}", errors)

    required_category_fields = [
        "definition",
        "analytic_question",
        "use_when",
        "do_not_use_when",
        "use_another_value_when",
        "positive_indicators",
        "exclusion_indicators",
        "candidate_detection",
        "primary_counterfactual",
        "counterfactual_tests",
        "escalation_condition",
        "review_policy",
        "provenance_note",
    ]
    all_test_ids: list[str] = []
    review_statuses: dict[str, str] = {}
    for category in EXPECTED_CATEGORIES:
        require(f"### `{category}`" in markdown, f"markdown missing section for {category}", errors)
        payload = manual["categories"][category]
        for field in required_category_fields:
            require(bool(payload.get(field)), f"{category}: blank required field {field}", errors)
        for field in ["use_when", "do_not_use_when", "use_another_value_when", "positive_indicators", "exclusion_indicators"]:
            require(all(item for item in payload[field]), f"{category}: blank item in {field}", errors)
        detection = payload["candidate_detection"]
        require(detection["states"] == ["candidate_supported", "candidate_not_supported", "insufficient_evidence", "not_applicable"], f"{category}: candidate states mismatch", errors)
        require(detection["order_priority"] == "none", f"{category}: candidate detection implies priority", errors)
        review_policy = payload["review_policy"]
        review_statuses[category] = review_policy["status"]
        for key in [
            "status",
            "trigger",
            "human_proposal_allowed",
            "model_proposal_allowed",
            "requires_human_review_for_model",
            "final_label_before_review",
            "source_basis",
        ]:
            require(key in review_policy, f"{category}: review policy missing {key}", errors)
        require(review_policy["status"] in {"standard", "review_sensitive", "reserved"}, f"{category}: invalid review status", errors)
        for test in payload["counterfactual_tests"]:
            all_test_ids.append(test["test_id"])
            for field in ["test_id", "question", "answer_states", "evidence_required", "confidence_required", "effect_on_decision_required"]:
                require(field in test and test[field] not in ["", []], f"{category}: test missing {field}", errors)
    require(len(all_test_ids) == len(set(all_test_ids)), "duplicate counterfactual test IDs", errors)
    require(review_statuses["cue_function"] == "reserved", "cue_function must be reserved", errors)
    require(review_statuses["boundary_setting"] == "review_sensitive", "boundary_setting must be review-sensitive", errors)
    require(review_statuses["context_inference"] == "review_sensitive", "context_inference must be review-sensitive", errors)
    standard = {k for k, v in review_statuses.items() if v == "standard"}
    require(standard == {"warrant_attribution", "warrant_relation", "operation_function", "temporal_layering", "perspective_assignment"}, f"unexpected standard categories: {standard}", errors)

    context_rules = manual["categories"]["context_inference"]["valid_proposal_requirements"]
    require(context_rules["exact_contextual_bridge_required"] is True, "context bridge must be required", errors)
    require(context_rules["selection_by_elimination_allowed"] is False, "context_inference cannot be by elimination", errors)
    for field in [
        "bridge_name",
        "bridge_type",
        "where_bridge_is_documented",
        "why_local_evidence_is_insufficient_without_it",
        "why_bridge_is_context_rather_than_new_warrant",
        "inside_or_outside_packet",
        "protocol_permission",
        "confidence",
    ]:
        require(field in context_rules["must_record"], f"context_inference missing requirement {field}", errors)

    decision = manual["decision_process"]
    require(decision["stage_A_candidate_detection"]["order_independence"] is True, "candidate detection must be order-independent", errors)
    detected_categories = {item["category"] for item in decision["stage_A_candidate_detection"]["checks"]}
    require(detected_categories == set(EXPECTED_CATEGORIES), "candidate detection must cover all categories", errors)
    require(decision["stage_A_candidate_detection"]["insufficient_evidence_terminal"] == "ESCALATE_INSUFFICIENT_EVIDENCE", "insufficient evidence terminal mismatch", errors)
    rules = decision["stage_B_dominance_resolution"]["rules"]
    cases = {rule["case"] for rule in rules}
    for case in [
        "no_supported_candidate",
        "one_supported_candidate",
        "two_supported_candidates",
        "more_than_two_supported_candidates",
        "review_sensitive_or_reserved_proposal",
        "conflicting_counterfactual_tests",
    ]:
        require(case in cases, f"dominance resolution missing {case}", errors)
    require(resolve_for_test(["operation_function", "warrant_attribution"])[0] == resolve_for_test(["warrant_attribution", "operation_function"])[0], "category order changes pairwise outcome", errors)
    require(resolve_for_test([]) == ("unresolved", True), "no-candidate path must unresolved/escalate", errors)
    require(resolve_for_test(["warrant_relation"]) == ("warrant_relation", False), "one-candidate path mismatch", errors)
    require(resolve_for_test(["a", "b"])[0] == "requires_pairwise_resolution", "two-candidate path must require pairwise resolution", errors)
    require(resolve_for_test(["a", "b", "c"]) == ("unresolved", True), "multi-candidate unresolved path mismatch", errors)
    require(resolve_for_test(["operation_function"], conflict=True) == ("unresolved", True), "conflicting tests must unresolved/escalate", errors)

    manual_pairs = {item["pair"]: item for item in manual["pairwise_disambiguation"]}
    for row in predicted_rows:
        require(row["category pair"] in manual_pairs, f"predicted pair missing: {row['category pair']}", errors)
    for required_pair in [
        "boundary_setting -> perspective_assignment",
        "perspective_assignment -> warrant_attribution",
        "perspective_assignment -> warrant_relation",
        "warrant_attribution -> operation_function",
        "operation_function -> temporal_layering",
        "boundary_setting -> context_inference",
        "context_inference -> warrant_relation",
    ]:
        require(required_pair in manual_pairs, f"required pairwise distinction missing: {required_pair}", errors)
    for pair, item in manual_pairs.items():
        left, _, right = pair.partition(" -> ")
        require(left in EXPECTED_CATEGORIES and right in EXPECTED_CATEGORIES, f"invalid pair categories: {pair}", errors)
        for field in [
            "why_confusion_expected",
            "distinction",
            "question",
            "counterfactual_manipulation",
            "pattern",
            "directional_error_risk",
            "unresolved_condition",
        ]:
            require(bool(item.get(field)), f"{pair}: blank pairwise field {field}", errors)
    require("Remove warranting standing" in manual_pairs["warrant_attribution -> operation_function"]["question"] or "remove warranting standing" in manual_pairs["warrant_attribution -> operation_function"]["question"], "operation/attribution lacks first manipulation", errors)
    require("remove the operation" in manual_pairs["warrant_attribution -> operation_function"]["question"].lower(), "operation/attribution lacks second manipulation", errors)

    examples = manual["worked_examples"]
    example_types = {item["example_type"] for item in examples}
    for kind in ["resolved", "pairwise", "review_required", "unresolved", "conflicting_tests"]:
        require(kind in example_types, f"missing worked example type {kind}", errors)
    for example in examples:
        for field in [
            "example_id",
            "training_manual_status",
            "actor_event_type",
            "selected_evidence",
            "focal_interpretive_decision",
            "proposed_primary_interpretation",
            "candidate_loci",
            "alternative_pathway",
            "primary_counterfactual_test",
            "primary_test_answer",
            "cited_evidence",
            "pairwise_counterfactual_test",
            "pairwise_test_answer",
            "confidence",
            "effect_on_decision",
            "proposed_locus",
            "operational_status",
            "final_operational_label",
            "uncertainty",
            "escalation_required",
            "review_policy_applied",
            "original_record_preserved",
            "decision_path",
            "provenance",
        ]:
            require(field in example and example[field] not in ["", []], f"{example['example_id']}: blank required example field {field}", errors)
        require(example["training_manual_status"] == "training_manual_example_ineligible_for_held_out_testing", f"{example['example_id']}: wrong training status", errors)
    review_example = next(item for item in examples if item["example_type"] == "review_required")
    require(review_example["actor_event_type"] == "model_proposal", "review-required example must be model proposal", errors)
    require(review_example["proposed_locus"] == "cue_function", "review-required example must preserve substantive proposed locus", errors)
    require(review_example["operational_status"] == "requires_human_review", "review-required example must require review", errors)
    require(review_example["final_operational_label"] == "unresolved", "review-required final label must be unresolved", errors)
    require(review_example["escalation_required"] is True, "review-required example must escalate", errors)

    synthesis_ids = [item["synthesis_id"] for item in manual["synthesis_records"]]
    require(set(synthesis_ids) == EXPECTED_SYNTHESIS_IDS, f"synthesis IDs mismatch: {set(synthesis_ids)}", errors)
    require(len(synthesis_ids) == len(set(synthesis_ids)), "duplicate synthesis IDs", errors)
    provenance_synthesis_ids = {row["synthesis_id"] for row in provenance_rows if row.get("synthesis_id")}
    require(EXPECTED_SYNTHESIS_IDS.issubset(provenance_synthesis_ids), "provenance missing synthesis IDs", errors)
    for row in provenance_rows:
        for field in [
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
        ]:
            require(row.get(field, "") != "", f"blank provenance field {field}", errors)

    require("private passage-level textual overlap check: not performed" in contamination.lower(), "contamination audit must state private text check not performed", errors)
    require("semantic correspondence check against private source packets: not performed" in contamination.lower(), "contamination audit must state semantic check not performed", errors)
    require("No selected study identifiers or source-packet paths were found" in contamination, "contamination conclusion must be limited", errors)
    forbidden_claims = [
        "zero copied selected passages",
        "no renamed selected examples",
        "passage-level contamination count zero",
        "passage-level textual overlap check performed",
    ]
    for claim in forbidden_claims:
        require(claim not in contamination.lower(), f"contamination audit overclaims: {claim}", errors)

    authoritative_text = markdown + "\n" + json.dumps(manual, ensure_ascii=False)
    for case_id in PR18_SELECTED_IDS:
        require(case_id not in authoritative_text, f"selected PR #18 ID appears in manual: {case_id}", errors)
    require(not re.search(r"\bL[12]_[A-Z0-9_]+", authoritative_text), "L1_/L2_ case-like ID appears in manual", errors)
    require("data/studies/human_llm_pilot/source_packets" not in authoritative_text, "study source packet path appears in manual", errors)

    require(manifest["manual_content_commit"] is None, "manual_content_commit must remain null pre-merge", errors)
    require(manifest["review_commit"] is None, "review_commit must remain null pre-review", errors)
    require(manifest["merge_commit"] is None, "merge_commit must remain null pre-merge", errors)
    require("TO_BE_" not in json.dumps(manifest), "manifest contains circular placeholder", errors)
    for path_key, hash_key in [
        ("markdown_path", "markdown_hash"),
        ("json_path", "json_hash"),
        ("source_inventory_path", "source_inventory_hash"),
        ("provenance_matrix_path", "provenance_matrix_hash"),
        ("predicted_confusion_audit_path", "predicted_confusion_audit_hash"),
        ("contamination_audit_path", "contamination_audit_hash"),
    ]:
        require(normalized_sha256(ROOT / manifest[path_key]) == manifest[hash_key], f"manifest hash mismatch for {path_key}", errors)
    require(manifest["schema_compatibility_status"] == "compatible_with_documented_protocol_constraint", "schema status must be constrained compatibility", errors)
    for phrase in [
        "candidate_set",
        "review_policy",
        "original_record_id",
        "compatible_with_documented_protocol_constraint",
    ]:
        require(phrase in schema_audit, f"schema audit missing evidence/gap: {phrase}", errors)

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
