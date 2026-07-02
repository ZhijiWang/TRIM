import csv
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
VALID_ROOT = ROOT / "examples" / "synthetic_dry_run" / "valid"
INVALID_ROOT = ROOT / "examples" / "synthetic_dry_run" / "invalid"


@pytest.fixture(scope="session", autouse=True)
def _build_and_run_dry_runs():
    subprocess.run(
        [sys.executable, "scripts/build_trim_haa_synthetic_dry_run.py"],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            "scripts/run_trim_haa_synthetic_dry_run.py",
            "--root",
            str(VALID_ROOT),
        ],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            "scripts/run_trim_haa_synthetic_dry_run.py",
            "--root",
            str(INVALID_ROOT),
            "--expect-invalid",
        ],
        cwd=ROOT,
        check=True,
    )


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_dry_run_package_loads_and_counts_match_expected_totals():
    core = _rows(VALID_ROOT / "core_annotations.csv")
    stages = {}
    for row in core:
        stages[row["annotation_stage"]] = stages.get(row["annotation_stage"], 0) + 1

    assert len(_rows(VALID_ROOT / "participant_metadata.csv")) == 4
    assert len(_rows(VALID_ROOT / "cases.csv")) == 6
    assert stages["human_pre"] == 24
    assert stages["ai_independent"] == 6
    assert stages["human_post_ai"] == 16
    assert stages["human_second_pass_control"] == 8


def test_valid_dry_run_has_zero_validation_errors():
    report = _rows(VALID_ROOT / "outputs" / "validation_report.csv")

    assert not [row for row in report if row["severity"] == "error"]


def test_all_human_pre_locks_verify():
    rows = _rows(VALID_ROOT / "outputs" / "lock_verification_report.csv")

    assert len(rows) == 24
    assert all(row["lock_verified"] == "True" for row in rows)


def test_human_post_records_link_to_correct_exposed_ai_and_controls_do_not():
    core = {row["annotation_id"]: row for row in _rows(VALID_ROOT / "core_annotations.csv")}
    provenance = {row["annotation_id"]: row for row in _rows(VALID_ROOT / "assistance_provenance.csv")}
    for row in core.values():
        prov = provenance[row["annotation_id"]]
        if row["annotation_stage"] == "human_post_ai":
            ai = core[prov["exposed_ai_annotation_id"]]
            assert ai["annotation_stage"] == "ai_independent"
            assert ai["case_id"] == row["case_id"]
            assert prov["exposed_model_run_id"] == provenance[ai["annotation_id"]]["model_run_id"]
            assert prov["ai_output_exposed"] != "none"
        elif row["annotation_stage"] == "human_second_pass_control":
            assert prov["exposed_ai_annotation_id"] == ""
            assert prov["exposed_model_run_id"] == ""
            assert prov["ai_output_exposed"] == "none"


def test_construct_separation_combinations_are_present():
    rows = _rows(VALID_ROOT / "outputs" / "construct_separation_check.csv")
    combos = {
        (
            row["ai_evidence_incorporated"],
            row["evidence_convergence_increased"],
            row["evidential_displacement"],
        )
        for row in rows
        if row["condition"] == "ai_exposure"
    }

    assert ("True", "False", "False") in combos
    assert ("True", "True", "False") in combos
    assert ("True", "True", "True") in combos
    assert ("False", "False", "False") in combos


def test_reports_contain_required_columns_and_counts():
    case_headers = _rows(VALID_ROOT / "outputs" / "case_level_report.csv")[0].keys()
    required = {
        "participant_id",
        "condition",
        "human_pre_annotation_id",
        "ai_annotation_id",
        "human_post_annotation_id",
        "control_annotation_id",
        "pre_lock_verified",
        "label_changed",
        "label_adopted_from_ai",
        "ai_evidence_incorporated",
        "evidence_convergence_increased",
        "evidential_displacement",
        "incorporated_ai_segments",
        "removed_pre_segments",
        "retained_pre_segments",
        "new_non_ai_segments",
        "mechanism_changed",
        "mechanism_adopted_from_ai",
        "uncertainty_shift",
        "alternative_changed_without_suppression",
        "alternative_mechanism_adopted_from_ai",
        "rationale_overlap",
        "copied_phrase_overlap",
        "self_reported_revision_reason",
        "validation_status",
        "warning_count",
    }
    assert required <= set(case_headers)

    study = {row["metric"]: row["value"] for row in _rows(VALID_ROOT / "outputs" / "study_level_report.csv")}
    assert study["total_ai_exposure_observations"] == "16"
    assert study["total_control_observations"] == "8"
    assert study["validation_error_count"] == "0"


def test_invalid_package_fails_and_detects_all_intended_defects():
    report = _rows(INVALID_ROOT / "outputs" / "invalid_scenario_detection_report.csv")

    assert report
    assert all(row["detected"] == "True" for row in report)


def test_output_generation_is_deterministic():
    outputs = sorted((VALID_ROOT / "outputs").glob("*"))
    before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in outputs if path.is_file()}
    subprocess.run(
        [
            sys.executable,
            "scripts/run_trim_haa_synthetic_dry_run.py",
            "--root",
            str(VALID_ROOT),
        ],
        cwd=ROOT,
        check=True,
    )
    after = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((VALID_ROOT / "outputs").glob("*"))
        if path.is_file()
    }

    assert after == before
