import csv
from pathlib import Path

import pytest

from trim_haa.exposure import ExposureEvent
from trim_haa.hashing import looks_like_sha256, sha256_text
from trim_haa.locking import LockRecord
from trim_haa.provenance import AssistanceProvenance, lineage_for, prompt_hash
from trim_haa.schema import TrimHAAAnnotation
from trim_haa.validator import validate_dataset, validate_provenance_record


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "trim_haa"


def _load_core(name):
    with (FIXTURE_DIR / name).open(newline="", encoding="utf-8") as handle:
        return [TrimHAAAnnotation.from_record(row) for row in csv.DictReader(handle)]


def _load_provenance(name):
    with (FIXTURE_DIR / name).open(newline="", encoding="utf-8") as handle:
        return [
            AssistanceProvenance.from_record(row)
            for row in csv.DictReader(handle)
            if row.get("annotation_id")
        ]


def _load_exposure(name):
    with (FIXTURE_DIR / name).open(newline="", encoding="utf-8") as handle:
        return [
            ExposureEvent.from_record(row)
            for row in csv.DictReader(handle)
            if row.get("exposure_event_id")
        ]


def _load_lock(name):
    with (FIXTURE_DIR / name).open(newline="", encoding="utf-8") as handle:
        return [
            LockRecord.from_record(row)
            for row in csv.DictReader(handle)
            if row.get("lock_manifest_id")
        ]


def _timestamp_provenance(**overrides):
    values = {
        "annotation_id": "AI-TIME",
        "case_id": "C-TIME",
        "actor_id": "MODEL",
        "actor_type": "model",
        "annotation_stage": "ai_independent",
        "pre_ai_annotation_locked": "not_applicable",
        "ai_output_exposed": "none",
        "exposure_order": "none",
        "interface_condition": "independent",
        "model_provider": "synthetic",
        "model_name": "synthetic-model",
        "model_version_or_date": "synthetic-version",
        "prompt_template_id": "SYNTHETIC",
        "prompt_hash": "a" * 64,
        "model_run_id": "RUN-SYNTHETIC",
        "retry_count": "0",
        "regenerated_output": "no",
        "exposure_timestamp": "2026-07-01T10:00:00Z",
        "post_edit_timestamp": "2026-07-01T10:05:00+00:00",
        "changed_label": "not_applicable",
        "changed_primary_evidence": "not_applicable",
        "changed_rationale_mechanism": "not_applicable",
        "changed_uncertainty": "not_applicable",
        "changed_alternative": "not_applicable",
        "self_reported_revision_reason": "not_applicable",
        "lock_status": "locked",
    }
    values.update(overrides)
    return AssistanceProvenance(**values)


@pytest.mark.parametrize("retry_count", ["0", "1", 2])
def test_retry_count_accepts_non_negative_integers(retry_count):
    issues = validate_provenance_record(_timestamp_provenance(retry_count=retry_count))

    assert not [issue for issue in issues if issue.field == "retry_count" and issue.severity == "error"]


@pytest.mark.parametrize("retry_count", [-1, True, "1.5", "invalid"])
def test_retry_count_rejects_negative_boolean_and_malformed_values(retry_count):
    issues = validate_provenance_record(_timestamp_provenance(retry_count=retry_count))

    assert any(
        issue.field == "retry_count"
        and issue.message == "retry_count must be a non-negative integer."
        for issue in issues
    )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("exposure_timestamp", "not-a-date"),
        ("post_edit_timestamp", "2026-99-99T25:61:00Z"),
    ],
)
def test_malformed_timestamps_are_errors(field_name, value):
    issues = validate_provenance_record(_timestamp_provenance(**{field_name: value}))

    assert any(
        issue.field == field_name and "not valid ISO 8601" in issue.message
        for issue in issues
    )


def test_utc_z_and_aware_offset_timestamps_are_valid():
    issues = validate_provenance_record(
        _timestamp_provenance(
            exposure_timestamp="2026-07-01T10:00:00Z",
            post_edit_timestamp="2026-07-01T12:05:00+02:00",
        )
    )

    assert not [
        issue for issue in issues
        if issue.field in {"exposure_timestamp", "post_edit_timestamp"}
    ]


def test_naive_and_mixed_timezone_timestamps_fail_without_type_error():
    issues = validate_provenance_record(
        _timestamp_provenance(
            exposure_timestamp="2026-07-01T10:00:00",
            post_edit_timestamp="2026-07-01T10:05:00Z",
        )
    )

    assert any(
        issue.field == "exposure_timestamp"
        and issue.message == "exposure_timestamp must include a timezone offset."
        for issue in issues
    )


def test_timestamp_chronology_violation_is_an_error():
    issues = validate_provenance_record(
        _timestamp_provenance(
            exposure_timestamp="2026-07-01T10:05:00Z",
            post_edit_timestamp="2026-07-01T10:00:00Z",
        )
    )

    assert any(
        issue.field == "post_edit_timestamp"
        and issue.message == "post_edit_timestamp must not precede exposure_timestamp."
        for issue in issues
    )


def test_parent_child_validity_and_lineage():
    records = _load_core("core_valid.csv")

    assert lineage_for("H01_C03_POST", records) == ["H01_C03_PRE", "H01_C03_POST"]
    assert validate_dataset([row for row in records if row.case_id == "C01"], _load_provenance("provenance_valid.csv"), _load_exposure("exposure_valid.csv"), _load_lock("lock_valid.csv")).valid


def test_invalid_missing_parent_cycle_and_unlocked_parent():
    report = validate_dataset(_load_core("core_invalid.csv"))
    messages = [issue.message for issue in report.errors]

    assert "Parent annotation does not exist." in messages
    assert "Cycles are forbidden." in messages
    assert "human_post_ai parent must be locked." in messages


def test_ai_metadata_requirements():
    issues = validate_provenance_record(_load_provenance("provenance_invalid_ai_metadata.csv")[0])
    fields = {issue.field for issue in issues}

    assert {"model_provider", "model_name", "prompt_template_id", "prompt_hash", "model_run_id"} <= fields


def test_prompt_hashing():
    digest = prompt_hash("exact prompt text")

    assert digest == sha256_text("exact prompt text")
    assert looks_like_sha256(digest)


def test_model_run_manifest_template_headers():
    path = Path(__file__).parents[1] / "data" / "trim_haa_model_run_manifest_template.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        headers = next(csv.reader(handle))

    assert "model_run_id" in headers
    assert "output_sha256" in headers
    assert "conversation_context_description" in headers


def test_provenance_completeness_valid_fixture_subset():
    records = [row for row in _load_core("core_valid.csv") if row.case_id == "C01"]
    provenance = _load_provenance("provenance_valid.csv")
    report = validate_dataset(
        records,
        provenance,
        _load_exposure("exposure_valid.csv"),
        _load_lock("lock_valid.csv"),
    )

    assert report.valid
    assert not [issue for issue in report.warnings if issue.field == "provenance"]


def test_exposure_linkage_and_model_run_match():
    records = [row for row in _load_core("core_valid.csv") if row.case_id == "C01"]
    report = validate_dataset(
        records,
        _load_provenance("provenance_valid.csv"),
        _load_exposure("exposure_valid.csv"),
        _load_lock("lock_valid.csv"),
    )

    assert report.valid


def test_missing_exposed_ai_annotation_is_error():
    records = [row for row in _load_core("core_valid.csv") if row.case_id == "C01"]
    provenance = _load_provenance("provenance_valid.csv")
    provenance[-1].exposed_ai_annotation_id = "AI_MISSING"
    report = validate_dataset(records, provenance, [], _load_lock("lock_valid.csv"))

    assert any(issue.field == "exposed_ai_annotation_id" for issue in report.errors)


def test_exposed_annotation_must_be_ai_independent_and_same_case():
    records = [row for row in _load_core("core_valid.csv") if row.case_id in {"C01", "C02"}]
    provenance = _load_provenance("provenance_valid.csv")
    provenance[-1].exposed_ai_annotation_id = "H01_C02_PRE"
    provenance[-1].exposed_model_run_id = "RUN_C01"
    report = validate_dataset(records, provenance, [], _load_lock("lock_valid.csv"))
    messages = [issue.message for issue in report.errors]

    assert "exposed_ai_annotation_id must reference an ai_independent record." in messages
    assert "Exposed AI record must have the same case_id." in messages


def test_exposure_event_validation_and_model_run_mismatch():
    records = [row for row in _load_core("core_valid.csv") if row.case_id == "C01"]
    report = validate_dataset(
        records,
        _load_provenance("provenance_valid.csv"),
        _load_exposure("exposure_invalid.csv"),
        _load_lock("lock_valid.csv"),
    )
    messages = [issue.message for issue in report.issues]

    assert "Duplicate exposure_event_id." in messages
    assert "Exposure event model_run_id must match AI provenance." in messages
    assert "Multiple exposure events for one human-post record." in messages


def test_lock_tampering_detection():
    records = [row for row in _load_core("core_valid.csv") if row.case_id == "C01"]
    report = validate_dataset(
        records,
        _load_provenance("provenance_valid.csv"),
        _load_exposure("exposure_valid.csv"),
        _load_lock("lock_tampered.csv"),
    )

    assert any(issue.field == "canonical_record_sha256" for issue in report.errors)


def test_missing_lock_manifest_error():
    records = [row for row in _load_core("core_valid.csv") if row.case_id == "C01"]
    report = validate_dataset(
        records,
        _load_provenance("provenance_valid.csv"),
        _load_exposure("exposure_valid.csv"),
        [],
    )

    assert any(issue.field == "lock_manifest" for issue in report.errors)
