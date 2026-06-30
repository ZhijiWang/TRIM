import pandas as pd

from trim.ai_execution import (
    SubmissionAvailability,
    alternative_signature_frequency,
    case_comparison,
    classify_pathway,
    evidence_overlap,
    field_agreement,
    jaccard,
    model_pattern_summary,
    primary_context_role_reversal,
    uncertainty_distribution,
)


def _left_record(**overrides):
    record = {
        "case_id": "case-1",
        "function_label": "immediate_stabilization",
        "friction_locus": "operation_function",
        "rationale_mechanism": "stabilizes",
        "epistemic_support": "textual_anchor",
        "discourse_level": "dramatic_present",
        "temporal_orientation": "immediate",
        "uncertainty_flag": "low",
        "primary_evidence_segment_ids": "S1|S2",
        "context_segment_ids": "S3",
        "alternative_signature": "",
        "rationale_note": "short rationale",
    }
    record.update(overrides)
    return record


def _right_record(**overrides):
    record = _left_record(
        rationale_mechanism="stabilizes+narrows",
        primary_evidence_segment_ids="S2|S3",
        context_segment_ids="S1",
        uncertainty_flag="medium",
        alternative_signature=(
            "warrant_relation / narrows / textual_anchor / dramatic_present / "
            "immediate / medium"
        ),
    )
    record.update(overrides)
    return record


def test_submission_availability_requires_all_locked_files():
    complete = SubmissionAvailability(True, True, True, True, True)
    missing_codex = SubmissionAvailability(True, False, False, False, False)

    assert complete.complete
    assert not missing_codex.complete


def test_jaccard_and_role_reversal():
    assert jaccard("S1|S2", "S2|S3") == 1 / 3
    assert jaccard("", "") == 1.0

    assert primary_context_role_reversal("S1|S2", "S3", "S2|S3", "S1") == "S1|S3"


def test_case_comparison_and_field_agreement_are_version_aware_common_fields():
    left = pd.DataFrame([_left_record()])
    right = pd.DataFrame([_right_record()])

    comparison = case_comparison(left, right)
    row = comparison.iloc[0]

    assert row["function_label_match"]
    assert not row["uncertainty_flag_match"]
    assert row["primary_evidence_jaccard"] == 1 / 3
    assert row["primary_context_role_reversal"] == "S1|S3"
    assert row["Claude_alternative_signature_present"]

    agreement = field_agreement(comparison)
    rationale = agreement.set_index("field").loc["rationale_mechanism"]
    assert rationale["exact_agreements"] == 0
    assert rationale["compatible_agreements"] == 1


def test_evidence_overlap_projection():
    comparison = case_comparison(
        pd.DataFrame([_left_record()]),
        pd.DataFrame([_right_record()]),
    )

    overlap = evidence_overlap(comparison).iloc[0]

    assert overlap["case_id"] == "case-1"
    assert not overlap["exact_primary_segment_match"]
    assert overlap["primary_context_role_reversal"] == "S1|S3"


def test_pathway_classification_categories():
    assert (
        classify_pathway(_left_record(), _left_record())
        == "same_function_same_pathway"
    )
    assert (
        classify_pathway(_left_record(), _right_record())
        == "same_function_different_pathway"
    )
    assert (
        classify_pathway(
            _left_record(),
            _right_record(function_label="extended_deliberation"),
        )
        == "different_function_partially_shared_pathway"
    )
    assert (
        classify_pathway(
            _left_record(function_label="no_fit"),
            _right_record(function_label="immediate_stabilization"),
        )
        == "no_fit_disagreement"
    )
    assert classify_pathway({}, _right_record()) == "insufficient_comparable_data"


def test_uncertainty_and_alternative_frequency_reports():
    frame = pd.DataFrame(
        [
            _left_record(uncertainty_flag="medium", alternative_signature="alt"),
            _left_record(uncertainty_flag="low", alternative_signature=""),
        ]
    )

    uncertainty = uncertainty_distribution(frame, "Claude")
    assert set(uncertainty["uncertainty_flag"]) == {"low", "medium"}
    frequency = alternative_signature_frequency(frame, "Claude")
    assert frequency["alternative_signature_count"] == 1
    assert frequency["alternative_signature_rate"] == 0.5


def test_model_pattern_summary_separates_style_from_method_claim():
    frame = pd.DataFrame(
        [
            _left_record(uncertainty_flag="medium", alternative_signature="alt"),
            _left_record(uncertainty_flag="medium", alternative_signature="alt"),
            _left_record(uncertainty_flag="low", alternative_signature=""),
        ]
    )

    summary = model_pattern_summary(frame, "Claude")

    assert summary["case_count"] == 3
    assert summary["medium_uncertainty_count"] == 2
    assert summary["alternative_signature_count"] == 2
    assert summary["all_segment_primary_count"] == 0
