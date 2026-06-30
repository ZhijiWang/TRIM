import pandas as pd
from zipfile import ZipFile

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
    question_log_comparison,
    question_log_summary,
    review_triggers,
    uncertainty_distribution,
    zip_member_hashes,
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
    left = pd.DataFrame(
        [
            _left_record(
                cue_family="researcher_only",
                broad_function_family="researcher_only",
            )
        ]
    )
    right = pd.DataFrame(
        [
            _right_record(
                cue_family="researcher_only",
                broad_function_family="researcher_only",
            )
        ]
    )

    comparison = case_comparison(left, right)
    row = comparison.iloc[0]

    assert "cue_family" not in comparison.columns
    assert "broad_function_family" not in comparison.columns
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
        classify_pathway(
            _left_record(),
            _right_record(friction_locus="reader_inference"),
        )
        == "same_function_different_pathway"
    )
    assert (
        classify_pathway(
            _left_record(uncertainty_flag="low"),
            _left_record(uncertainty_flag="medium"),
        )
        == "same_function_same_pathway"
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


def test_zip_member_hashes_extracts_all_files(tmp_path):
    zip_path = tmp_path / "submission.zip"
    with ZipFile(zip_path, "w") as archive:
        archive.writestr("coding.csv", "case_id,coder_id\ncase-1,coder\n")
        archive.writestr("readme.txt", "locked")

    hashes = zip_member_hashes(zip_path)

    assert set(hashes) == {"coding.csv", "readme.txt"}
    assert all(len(value) == 64 for value in hashes.values())


def test_question_log_summary_and_comparison():
    left = pd.DataFrame(
        [
            {
                "case_id": "case-1",
                "question_type": "interpretive",
                "did_question_change_code": "yes",
                "blocking_or_nonblocking": "nonblocking",
                "requires_manual_revision": "no",
                "timestamp_utc": "2026-06-30T00:00:00Z~",
            }
        ]
    )
    right = pd.DataFrame(
        [
            {
                "case_id": "case-1",
                "question_type": "definitional",
                "did_question_change_code": "no",
                "blocking_or_nonblocking": "blocking",
                "requires_manual_revision": "yes",
                "timestamp_utc": "2026-06-30T00:01:00Z~",
            },
            {
                "case_id": "case-2",
                "question_type": "procedural",
                "did_question_change_code": "no",
                "blocking_or_nonblocking": "nonblocking",
                "requires_manual_revision": "no",
                "timestamp_utc": "2026-06-30T00:02:00Z~",
            },
        ]
    )

    summary = question_log_summary(right, "Claude").iloc[0]
    comparison = question_log_comparison(left, right).iloc[0]

    assert summary["question_count"] == 2
    assert summary["manual_revision_requested_count"] == 1
    assert comparison["overlapping_cases"] == "case-1"
    assert comparison["right_only_cases"] == "case-2"


def test_review_triggers_are_non_adjudicated():
    comparison = case_comparison(
        pd.DataFrame([_left_record()]),
        pd.DataFrame([_right_record(function_label="extended_deliberation")]),
    )

    triggers = review_triggers(
        comparison,
        primary_jaccard_threshold=0.5,
        repeated_question_cases={"case-1"},
    )
    row = triggers.iloc[0]

    assert "not human intercoder reliability" in row["disclaimer"]
    assert "different_function" in row["trigger_reasons"]
    assert "primary_jaccard_below_threshold" in row["trigger_reasons"]
    assert "repeated_question_log_friction" in row["trigger_reasons"]
    assert row["human_review_override"] == ""
