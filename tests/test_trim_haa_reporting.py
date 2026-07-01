import csv
from pathlib import Path

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
