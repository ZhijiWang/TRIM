"""Validate the friction_locus manual v0.1 protocol-review artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from copy import deepcopy
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
EXPECTED_STATUS = "AUTHORITATIVE_FOR_PROTOCOL_REVIEW"
EXPECTED_STATES = {
    "candidate_supported",
    "candidate_not_supported",
    "insufficient_evidence",
    "not_applicable",
}
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
    "SYN_V0_1_CANDIDATE_SCHEMA",
    "SYN_V0_1_REVIEW_POLICY_SCHEMA",
    "SYN_V0_1_REVIEW_LINKAGE",
    "SYN_V0_1_CUE_POSITIVE_CRITERION",
    "SYN_V0_1_OPERATION_ATTRIBUTION_EXAMPLE",
    "SYN_V0_1_CROSS_FIELD_VALIDATION",
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


def review_status_for(category: str | None) -> str:
    if category == "cue_function":
        return "reserved"
    if category in {"boundary_setting", "context_inference"}:
        return "review_sensitive"
    if category in EXPECTED_CATEGORIES:
        return "standard"
    return "not_applicable"


def expected_policy_requires_review(record: dict[str, Any]) -> bool:
    return (
        record.get("actor_type") == "model"
        and review_status_for(record.get("friction_locus_proposed") or record.get("proposed_locus"))
        in {"reserved", "review_sensitive"}
    )


def candidate_set(record: dict[str, Any]) -> set[str]:
    return {
        item["category"]
        for item in record["candidate_loci"]
        if item["state"] == "candidate_supported"
    }


def validate_candidate_loci(record: dict[str, Any], label: str, errors: list[str]) -> None:
    entries = record.get("candidate_loci")
    require(isinstance(entries, list), f"{label}: candidate_loci must be a list", errors)
    if not isinstance(entries, list):
        return
    require(len(entries) == 8, f"{label}: candidate_loci must have exactly eight entries", errors)
    categories = [item.get("category") for item in entries if isinstance(item, dict)]
    require(set(categories) == set(EXPECTED_CATEGORIES), f"{label}: candidate category set mismatch", errors)
    require(len(categories) == len(set(categories)), f"{label}: duplicate candidate category", errors)
    require("unresolved" not in categories, f"{label}: unresolved cannot be a candidate category", errors)
    for item in entries:
        if not isinstance(item, dict):
            errors.append(f"{label}: candidate entry must be object")
            continue
        category = item.get("category")
        state = item.get("state")
        require(category in EXPECTED_CATEGORIES, f"{label}: invalid candidate category {category}", errors)
        require(state in EXPECTED_STATES, f"{label}: invalid candidate state {state}", errors)
        require(isinstance(item.get("rationale"), str) and bool(item["rationale"].strip()), f"{label}: candidate rationale required for {category}", errors)
        require(item.get("confidence") in {"low", "medium", "high", "not_applicable"}, f"{label}: invalid confidence for {category}", errors)
        evidence = item.get("cited_evidence")
        require(isinstance(evidence, list), f"{label}: cited_evidence must be list for {category}", errors)
        if state == "candidate_supported":
            require(bool(evidence), f"{label}: supported candidate requires cited evidence for {category}", errors)
        else:
            require(
                item.get("rationale", "").strip(),
                f"{label}: unsupported candidate still needs rationale for {category}",
                errors,
            )


def validate_review_policy(record: dict[str, Any], label: str, errors: list[str]) -> None:
    proposed = record.get("friction_locus_proposed", record.get("proposed_locus"))
    operational_status = record.get("friction_locus_operational_status", record.get("operational_status"))
    final_label = record.get("final_operational_label")
    policy = record.get("review_policy_applied")
    require(isinstance(policy, dict), f"{label}: review_policy_applied must be object", errors)
    if not isinstance(policy, dict):
        return
    expected_status = review_status_for(proposed)
    if proposed in EXPECTED_CATEGORIES:
        require(policy.get("category") == proposed, f"{label}: review policy category must match proposed locus", errors)
    else:
        require(policy.get("status") == "not_applicable", f"{label}: unresolved proposal should use not_applicable policy", errors)
    require(policy.get("status") == expected_status, f"{label}: review policy status mismatch for {proposed}", errors)
    require(isinstance(policy.get("trigger"), list), f"{label}: review policy trigger must be list", errors)
    require(isinstance(policy.get("requires_human_review"), bool), f"{label}: requires_human_review must be boolean", errors)
    if expected_status == "standard":
        require(policy.get("final_label_before_review") is None, f"{label}: standard final_label_before_review must be null", errors)
    if expected_policy_requires_review(record):
        require(policy.get("requires_human_review") is True, f"{label}: model reserved/review-sensitive proposal must require review", errors)
        require(operational_status == "requires_human_review", f"{label}: model reserved/review-sensitive proposal must require operational review", errors)
        require(final_label == "unresolved", f"{label}: model reserved/review-sensitive proposal final label must be unresolved", errors)
        require(record.get("escalation_required") is True, f"{label}: model reserved/review-sensitive proposal must escalate", errors)


def validate_review_linkage(record: dict[str, Any], label: str, errors: list[str]) -> None:
    role = record.get("analyst_role")
    rec_id = record.get("record_id")
    rec_hash = record.get("record_hash")
    review_id = record.get("review_of_record_id")
    review_hash = record.get("review_of_record_hash")
    if role == "adjudicator_separate_record":
        require(isinstance(review_id, str) and bool(review_id), f"{label}: adjudicator review requires review_of_record_id", errors)
        require(isinstance(review_hash, str) and bool(re.fullmatch(r"sha256:[a-f0-9]{64}", review_hash)), f"{label}: adjudicator review requires valid review_of_record_hash", errors)
        require(review_id != rec_id, f"{label}: review record ID must differ from original ID", errors)
        require(review_hash != f"sha256:{rec_hash}", f"{label}: review record hash must differ from original reviewed hash", errors)
        require(record.get("original_record_preserved") is True, f"{label}: review must preserve original record", errors)
    elif role is not None:
        require(review_id is None, f"{label}: non-review record must not claim review_of_record_id", errors)
        require(review_hash is None, f"{label}: non-review record must not claim review_of_record_hash", errors)


def validate_record(record: dict[str, Any], label: str, errors: list[str]) -> None:
    validate_candidate_loci(record, label, errors)
    validate_review_policy(record, label, errors)
    validate_review_linkage(record, label, errors)
    supported = candidate_set(record)
    proposed = record.get("friction_locus_proposed", record.get("proposed_locus"))
    if proposed in EXPECTED_CATEGORIES and record.get("operational_status", record.get("friction_locus_operational_status")) == "accepted_for_analysis":
        require(proposed in supported, f"{label}: accepted proposed locus must be in candidate set", errors)


def resolve_for_test(candidate_loci: list[dict[str, Any]], conflict: bool = False) -> tuple[str, bool]:
    supported = sorted(candidate_set({"candidate_loci": candidate_loci}))
    if conflict:
        return "unresolved", True
    if not supported:
        return "unresolved", True
    if len(supported) == 1:
        return supported[0], False
    if len(supported) == 2:
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
    human_template = load_json(ROOT / "templates" / "human_coder_record.json")
    model_template = load_json(ROOT / "templates" / "model_coder_record.json")

    require(manifest["manual_status"] == EXPECTED_STATUS, "manifest manual status mismatch", errors)
    require(manual["manual_status"] == EXPECTED_STATUS, "JSON manual status mismatch", errors)
    require(f"Status: `{EXPECTED_STATUS}`" in markdown, "Markdown manual status mismatch", errors)
    require(manual["category_order"] == EXPECTED_CATEGORIES, "category order mismatch", errors)
    require(set(manual["categories"]) == set(EXPECTED_CATEGORIES), "category set mismatch", errors)

    schema_defs = schema["$defs"]
    require("candidate_loci" in schema_defs, "schema missing candidate_loci definition", errors)
    require("review_policy_applied" in schema_defs, "schema missing review_policy_applied definition", errors)
    require("review_record_hash" in schema_defs, "schema missing review_record_hash definition", errors)
    shared_required = set(schema_defs["shared_record"]["required"])
    for field in ["candidate_loci", "review_policy_applied", "review_of_record_id", "review_of_record_hash"]:
        require(field in shared_required, f"shared record does not require {field}", errors)
    candidate_schema = schema_defs["candidate_loci"]
    require(candidate_schema.get("minItems") == 8 and candidate_schema.get("maxItems") == 8, "schema must require exactly eight candidates", errors)
    require(len(candidate_schema.get("allOf", [])) == 8, "schema must contain one exact category contains rule per category", errors)
    state_enum = set(schema_defs["candidate_locus_state"]["enum"])
    require(state_enum == EXPECTED_STATES, "candidate state enum mismatch", errors)

    governance_fields = manual["governance_model"]["fields"]
    for field in [
        "proposed_locus",
        "candidate_loci",
        "operational_status",
        "final_operational_label",
        "review_policy_applied",
        "review_of_record_id",
        "review_of_record_hash",
        "original_record_preserved",
    ]:
        require(field in governance_fields, f"governance model missing {field}", errors)
    require("candidate_loci is the authoritative structured record" in " ".join(manual["governance_model"]["rules"]), "candidate_loci authority rule missing", errors)

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
        detection = payload["candidate_detection"]
        require(set(detection["states"]) == EXPECTED_STATES, f"{category}: candidate states mismatch", errors)
        require(detection["order_priority"] == "none", f"{category}: candidate detection implies priority", errors)
        review_policy = payload["review_policy"]
        review_statuses[category] = review_policy["status"]
        require(review_policy["status"] == review_status_for(category), f"{category}: review status mismatch", errors)
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

    cue_blob = json.dumps(manual["categories"]["cue_function"], ensure_ascii=False).lower()
    forbidden_cue = [
        "after more specific",
        "after all more specific",
        "no more specific candidate",
        "more specific loci have been tested and excluded",
        "after excluding more specific",
    ]
    for phrase in forbidden_cue:
        require(phrase not in cue_blob, f"cue_function residual wording remains: {phrase}", errors)
    for phrase in ["cue-family substitution", "holding the other procedural variables stable", "not the mere presence of a cue word"]:
        require(phrase in cue_blob, f"cue_function lacks positive criterion phrase: {phrase}", errors)

    context_rules = manual["categories"]["context_inference"]["valid_proposal_requirements"]
    require(context_rules["exact_contextual_bridge_required"] is True, "context bridge must be required", errors)
    require(context_rules["selection_by_elimination_allowed"] is False, "context_inference cannot be by elimination", errors)

    decision = manual["decision_process"]
    stage_a = decision["stage_A_candidate_detection"]
    require(stage_a["structured_storage"] == "candidate_loci", "Stage A must store candidate_loci", errors)
    require(stage_a["order_independence"] is True, "candidate detection must be order-independent", errors)
    detected_categories = {item["category"] for item in stage_a["checks"]}
    require(detected_categories == set(EXPECTED_CATEGORIES), "candidate detection must cover all categories", errors)
    require(stage_a["candidate_set_rule"].startswith("candidate_set ="), "candidate set rule missing", errors)
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
    op_attr_question = manual_pairs["warrant_attribution -> operation_function"]["question"].lower()
    require("remove warranting standing" in op_attr_question, "operation/attribution lacks standing-removal manipulation", errors)
    require("remove the operation" in op_attr_question, "operation/attribution lacks operation-removal manipulation", errors)

    examples = manual["worked_examples"]
    example_types = {item["example_type"] for item in examples}
    for kind in ["resolved", "pairwise", "review_required", "unresolved", "conflicting_tests", "linked_review_record"]:
        require(kind in example_types, f"missing worked example type {kind}", errors)
    proposal_examples = [item for item in examples if item["example_type"] != "linked_review_record"]
    linked_reviews = [item for item in examples if item["example_type"] == "linked_review_record"]
    require(len(proposal_examples) == 5, "expected five worked proposal records", errors)
    require(len(linked_reviews) == 1, "expected one linked review record", errors)
    for example in examples:
        validate_record(example, example["example_id"], errors)
        for field in [
            "example_id",
            "record_id",
            "record_hash",
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
            "review_of_record_id",
            "review_of_record_hash",
            "original_record_preserved",
            "decision_path",
            "provenance",
        ]:
            require(field in example, f"{example['example_id']}: missing example field {field}", errors)
        require(example["training_manual_status"] == "training_manual_example_ineligible_for_held_out_testing", f"{example['example_id']}: wrong training status", errors)
    review_example = next(item for item in examples if item["example_id"] == "WEX_REVIEW_REQUIRED_CUE_FUNCTION_MODEL")
    require(review_example["actor_event_type"] == "model_proposal", "review-required example must be model proposal", errors)
    require(review_example["review_of_record_id"] is None and review_example["review_of_record_hash"] is None, "original model proposal must not have review linkage", errors)
    linked = linked_reviews[0]
    require(linked["review_of_record_id"] == review_example["record_id"], "linked review must cite original record id", errors)
    require(linked["review_of_record_hash"] == "sha256:" + review_example["record_hash"], "linked review must cite original hash", errors)
    require(linked["record_id"] != review_example["record_id"], "linked review record ID must be distinct", errors)
    require(linked["record_hash"] != review_example["record_hash"], "linked review hash must be distinct", errors)
    require(linked["original_proposed_locus_preserved"] == review_example["proposed_locus"], "review must preserve original proposed locus history", errors)

    op_example = next(item for item in examples if item["example_id"] == "WEX_PAIR_OPERATION_ATTRIBUTION")
    require({"operation_function", "warrant_attribution"}.issubset(candidate_set(op_example)), "operation/attribution example must support both candidates", errors)
    for phrase in [
        "already officially admitted",
        "no special authority",
        "any equally authorized reader",
        "standing is a prerequisite",
        "operation performs the actual evidence-to-interpretation conversion",
    ]:
        require(phrase in json.dumps(op_example).lower(), f"operation/attribution example missing: {phrase}", errors)
    require(op_example["standing_removal_result"], "operation/attribution example missing standing-removal result", errors)
    require(op_example["operation_removal_result"], "operation/attribution example missing operation-removal result", errors)

    # Candidate order independence: reversed array still validates and resolves the same.
    reversed_example = deepcopy(op_example)
    reversed_example["candidate_loci"] = list(reversed(reversed_example["candidate_loci"]))
    before = resolve_for_test(op_example["candidate_loci"])
    after = resolve_for_test(reversed_example["candidate_loci"])
    require(before == after, "candidate array order changes validator outcome", errors)
    duplicate_example = deepcopy(op_example)
    duplicate_example["candidate_loci"][0]["category"] = duplicate_example["candidate_loci"][1]["category"]
    dup_errors: list[str] = []
    validate_candidate_loci(duplicate_example, "duplicate_example", dup_errors)
    require(any("mismatch" in item or "duplicate" in item for item in dup_errors), "duplicate candidate categories were not rejected", errors)
    cue_only_bad = deepcopy(review_example)
    for item in cue_only_bad["candidate_loci"]:
        item["state"] = "candidate_not_supported"
        item["cited_evidence"] = []
        item["rationale"] = "No other candidate supported."
    cue_only_bad["candidate_loci"][0]["state"] = "candidate_supported"
    cue_only_bad["candidate_loci"][0]["rationale"] = "Supported only because no other candidate is supported."
    require("cue-family substitution" not in cue_only_bad["candidate_loci"][0]["rationale"], "bad cue fixture unexpectedly contains positive criterion", errors)
    require("no other candidate" in cue_only_bad["candidate_loci"][0]["rationale"], "bad cue fixture missing elimination-only wording", errors)

    for template, name in [(human_template, "human template"), (model_template, "model template")]:
        validate_record(template, name, errors)
        require(template["review_of_record_id"] is None, f"{name}: proposal template review_of_record_id must be null", errors)
        require(template["review_of_record_hash"] is None, f"{name}: proposal template review_of_record_hash must be null", errors)

    synthesis_ids = {item["synthesis_id"] for item in manual["synthesis_records"]}
    require(synthesis_ids == EXPECTED_SYNTHESIS_IDS, f"synthesis IDs mismatch: {synthesis_ids}", errors)
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
        require(row.get("unresolved_conflict") == "none", "provenance contains unresolved conflict", errors)

    lower_contamination = contamination.lower()
    require("private passage-level textual overlap check: not performed" in lower_contamination, "contamination audit must state private text check not performed", errors)
    require("semantic correspondence check against private source packets: not performed" in lower_contamination, "contamination audit must state semantic check not performed", errors)
    require("No selected study identifiers or source-packet paths were found" in contamination, "contamination conclusion must be limited", errors)
    for claim in [
        "zero copied selected passages",
        "passage-level contamination count zero",
        "passage-level textual overlap check performed",
    ]:
        require(claim not in lower_contamination, f"contamination audit overclaims: {claim}", errors)

    authoritative_text = markdown + "\n" + json.dumps(manual, ensure_ascii=False)
    for case_id in PR18_SELECTED_IDS:
        require(case_id not in authoritative_text, f"selected PR #18 ID appears in manual: {case_id}", errors)
    require(not re.search(r"\bL[12]_[A-Z0-9_]+", authoritative_text), "L1_/L2_ case-like ID appears in manual", errors)
    require("data/studies/human_llm_pilot/source_packets" not in authoritative_text, "study source packet path appears in manual", errors)

    for key in ["manual_content_commit", "review_commit", "merge_commit"]:
        require(manifest[key] is None, f"{key} must remain null pre-merge/review", errors)
    require("TO_BE_" not in json.dumps(manifest), "manifest contains circular placeholder", errors)
    for path_key, hash_key in [
        ("markdown_path", "markdown_hash"),
        ("json_path", "json_hash"),
        ("source_inventory_path", "source_inventory_hash"),
        ("provenance_matrix_path", "provenance_matrix_hash"),
        ("predicted_confusion_audit_path", "predicted_confusion_audit_hash"),
        ("contamination_audit_path", "contamination_audit_hash"),
        ("schema_compatibility_audit_path", "schema_compatibility_audit_hash"),
        ("schema_path", "schema_hash"),
    ]:
        require(normalized_sha256(ROOT / manifest[path_key]) == manifest[hash_key], f"manifest hash mismatch for {path_key}", errors)
    require(manifest["schema_compatibility_status"] == "compatible", "schema status must be compatible", errors)
    for phrase in [
        "candidate_loci[]",
        "review_policy_applied",
        "review_of_record_id",
        "review_of_record_hash",
        "No manual-required algorithmic state exists only in unstructured prose.",
        "JSON Schema-enforced",
        "Validator-enforced",
        "Protocol-enforced",
    ]:
        require(phrase in schema_audit, f"schema audit missing: {phrase}", errors)

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
