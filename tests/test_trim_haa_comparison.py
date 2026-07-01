import csv
from pathlib import Path

from trim_haa.comparison import (
    ai_associated_change_summary,
    compare_pre_ai_post,
    compare_pre_control,
    copied_phrase_overlap,
    exposure_associated_convergence,
    independent_convergence,
    normalised_token_overlap,
    rationale_comparison,
    segment_set_metrics,
)
from trim_haa.schema import TrimHAAAnnotation


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "trim_haa"


def _records_by_id():
    with (FIXTURE_DIR / "core_valid.csv").open(newline="", encoding="utf-8") as handle:
        return {
            row["annotation_id"]: TrimHAAAnnotation.from_record(row)
            for row in csv.DictReader(handle)
        }


def test_label_adoption():
    records = _records_by_id()
    result = compare_pre_ai_post(records["H01_C03_PRE"], records["AI_C03"], records["H01_C03_POST"])

    assert result["label_changed"] is True
    assert result["label_adopted_from_ai"] is True


def test_evidence_jaccard():
    assert segment_set_metrics("S1|S2", "S2|S3")["jaccard"] == 1 / 3


def test_evidence_adoption():
    records = _records_by_id()
    result = compare_pre_ai_post(records["H01_C04_PRE"], records["AI_C04"], records["H01_C04_POST"])

    assert result["evidence_adoption"] is True
    assert result["evidence_adopted_from_ai"] == "C04_S2"


def test_evidential_displacement():
    records = _records_by_id()
    result = compare_pre_ai_post(records["H01_C05_PRE"], records["AI_C05"], records["H01_C05_POST"])

    assert result["evidential_displacement"] is True


def test_mechanism_adoption():
    records = _records_by_id()
    result = compare_pre_ai_post(records["H01_C06_PRE"], records["AI_C06"], records["H01_C06_POST"])

    assert result["mechanism_adopted_from_ai"] is True


def test_uncertainty_shift():
    records = _records_by_id()
    result = compare_pre_ai_post(records["H01_C07_PRE"], records["AI_C07"], records["H01_C07_POST"])

    assert result["uncertainty_shift"] == "decreased"


def test_alternative_suppression():
    records = _records_by_id()
    result = compare_pre_ai_post(records["H01_C08_PRE"], records["AI_C08"], records["H01_C08_POST"])

    assert result["alternative_suppressed"] is True


def test_alternative_generation():
    records = _records_by_id()
    result = compare_pre_ai_post(records["H01_C09_PRE"], records["AI_C09"], records["H01_C09_POST"])

    assert result["alternative_generated"] is True


def test_rationale_overlap_measures_are_lexical_only():
    assert normalised_token_overlap("AI selected evidence", "AI selected other evidence") > 0
    assert copied_phrase_overlap("one two three four five", "one two three four six") > 0
    assert rationale_comparison(
        TrimHAAAnnotation(rationale_note="same text"),
        TrimHAAAnnotation(rationale_note="same text"),
    )["exact_text_match"] is True


def test_control_second_pass_comparison():
    records = _records_by_id()
    control = compare_pre_control(records["H01_C10_PRE"], records["H01_C10_CONTROL"])
    summary = ai_associated_change_summary(
        records["H01_C10_PRE"],
        records["AI_C10"],
        records["H01_C10_PRE"],
        records["H01_C10_CONTROL"],
    )

    assert control["pre_to_control_primary_jaccard"] < 1
    assert summary["descriptive_ai_associated_label_change_minus_control"] == 0


def test_construct_functions():
    records = _records_by_id()

    assert independent_convergence(records["H01_C01_PRE"], records["AI_C01"], "function_label")
    assert exposure_associated_convergence(
        records["H01_C04_PRE"],
        records["AI_C04"],
        records["H01_C04_POST"],
        "primary_evidence_segment_ids",
    )

