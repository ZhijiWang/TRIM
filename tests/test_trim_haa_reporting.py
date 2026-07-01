import csv
from pathlib import Path

from trim_haa.reporting import case_level_report, participant_level_report, study_level_report
from trim_haa.schema import TrimHAAAnnotation


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "trim_haa"


def _records():
    with (FIXTURE_DIR / "core_valid.csv").open(newline="", encoding="utf-8") as handle:
        return [TrimHAAAnnotation.from_record(row) for row in csv.DictReader(handle)]


def test_case_level_report_generation():
    report = case_level_report(_records())

    assert "label_adoption" in report.columns
    assert bool(report.loc[report["case_id"] == "C03", "label_adoption"].iloc[0]) is True


def test_participant_level_report_generation():
    report = participant_level_report(_records())

    assert report.loc[0, "number_of_cases"] >= 10
    assert "evidence_adoptions" in report.columns


def test_study_level_report_generation():
    report = study_level_report(_records())

    assert report["case_count"] >= 10
    assert "validation_issue_count" in report
    assert "missingness" in report

