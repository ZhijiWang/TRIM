import csv
from pathlib import Path

import pandas as pd
import pytest

from trim_haa.locking import LockRecord
from trim_haa.provenance import AssistanceProvenance
from trim_haa.reporting import case_level_report, participant_level_report, study_level_report
from trim_haa.schema import TrimHAAAnnotation


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "trim_haa"


def _records():
    with (FIXTURE_DIR / "core_valid.csv").open(newline="", encoding="utf-8") as handle:
        return [TrimHAAAnnotation.from_record(row) for row in csv.DictReader(handle)]


def _provenance():
    with (FIXTURE_DIR / "provenance_valid.csv").open(newline="", encoding="utf-8") as handle:
        return [AssistanceProvenance.from_record(row) for row in csv.DictReader(handle) if row.get("annotation_id")]


def _locks():
    with (FIXTURE_DIR / "lock_valid.csv").open(newline="", encoding="utf-8") as handle:
        return [LockRecord.from_record(row) for row in csv.DictReader(handle) if row.get("lock_manifest_id")]


def test_case_level_report_generation():
    report = case_level_report(_records(), _provenance(), _locks())

    assert "label_adoption" in report.columns
    assert "label_changed" in report.columns
    assert "exposed_ai_annotation_id" in report.columns
    assert "ai_evidence_incorporated" in report.columns
    assert "evidence_convergence_increased" in report.columns
    assert "copied_phrase_overlap" in report.columns
    assert bool(report.loc[report["case_id"] == "C03", "label_adoption"].iloc[0]) is True


def test_participant_level_report_generation():
    report = participant_level_report(_records())

    assert report.loc[0, "number_of_cases"] >= 10
    assert "evidence_adoptions" in report.columns


def test_study_level_report_generation():
    report = study_level_report(_records(), _provenance(), [], _locks())

    assert report["case_count"] >= 10
    assert "validation_issue_count" in report
    assert "ai_evidence_incorporation_count" in report
    assert "evidence_convergence_increased_count" in report
    assert "missingness" in report


def _report_record(annotation_id, case_id, stage, label, *, actor_id="H01"):
    return TrimHAAAnnotation(
        annotation_id=annotation_id,
        case_id=case_id,
        parent_annotation_id=f"{case_id}-PRE" if stage == "human_post_ai" else "",
        actor_id="MODEL" if stage == "ai_independent" else actor_id,
        actor_type="model" if stage == "ai_independent" else "human",
        annotation_stage=stage,
        primary_evidence_segment_ids="S1",
        function_label=label,
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="Synthetic rationale.",
        alternative_pathway_present="no",
        status="locked",
    )


def test_label_changes_and_adoptions_are_distinct_metrics():
    records = [
        _report_record("C1-PRE", "C1", "human_pre", "a"),
        _report_record("C1-AI", "C1", "ai_independent", "b"),
        _report_record("C1-POST", "C1", "human_post_ai", "c"),
        _report_record("C2-PRE", "C2", "human_pre", "a"),
        _report_record("C2-AI", "C2", "ai_independent", "b"),
        _report_record("C2-POST", "C2", "human_post_ai", "b"),
    ]

    case_report = case_level_report(records)
    participant = participant_level_report(records, case_report).iloc[0]

    assert bool(case_report.loc[case_report["case_id"] == "C1", "label_changed"].iloc[0])
    assert not bool(case_report.loc[case_report["case_id"] == "C1", "label_adoption"].iloc[0])
    assert participant["label_changes"] == 2
    assert participant["label_adoptions"] == 1


def test_boolean_aggregation_ignores_missing_and_false_values():
    records = [
        _report_record(f"C{index}-PRE", f"C{index}", "human_pre", "a")
        for index in range(1, 9)
    ]
    case_report = pd.DataFrame(
        {
            "case_id": [f"C{index}" for index in range(1, 9)],
            "label_changed": [True, False, None, float("nan"), "", "true", "yes", "1"],
            "label_adoption": [False, True, None, float("nan"), "", "false", "no", "0"],
        }
    )

    participant = participant_level_report(records, case_report).iloc[0]

    assert participant["label_changes"] == 4
    assert participant["label_adoptions"] == 1


def test_duplicate_stage_rows_fail_instead_of_selecting_first():
    records = [
        _report_record("C1-PRE-A", "C1", "human_pre", "a"),
        _report_record("C1-PRE-B", "C1", "human_pre", "a"),
    ]

    with pytest.raises(ValueError, match="multiple 'human_pre' records"):
        case_level_report(records)
