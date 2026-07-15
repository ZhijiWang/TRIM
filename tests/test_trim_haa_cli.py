import csv
import subprocess
import sys

from trim_haa.locking import LOCK_MANIFEST_FIELDS, create_lock_record
from trim_haa.schema import CORE_FIELDS, TrimHAAAnnotation


def _annotation():
    return TrimHAAAnnotation(
        annotation_id="SYNTHETIC-LOCK-TARGET",
        case_id="SYNTHETIC-CASE",
        actor_id="SYNTHETIC-CODER",
        actor_type="human",
        annotation_stage="human_pre",
        primary_evidence_segment_ids="S1",
        function_label="label_a",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="Synthetic lock verification record.",
        alternative_pathway_present="no",
        status="locked",
    )


def _write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _run_verify_lock(tmp_path, lock_rows):
    annotation = _annotation()
    annotation_path = tmp_path / "annotation.csv"
    lock_path = tmp_path / "locks.csv"
    _write_csv(annotation_path, CORE_FIELDS, [annotation.to_csv_record()])
    _write_csv(lock_path, LOCK_MANIFEST_FIELDS, lock_rows)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "trim_haa",
            "verify-lock",
            str(annotation_path),
            str(lock_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def _matching_lock(lock_id="LOCK-1"):
    return create_lock_record(
        _annotation(),
        lock_manifest_id=lock_id,
        locked_at="2026-07-01T00:00:00Z",
        locked_by="SYNTHETIC-REVIEWER",
    ).to_record()


def test_verify_lock_succeeds_for_exactly_one_matching_row(tmp_path):
    result = _run_verify_lock(tmp_path, [_matching_lock()])

    assert result.returncode == 0
    assert "verification=passed" in result.stdout
    assert "Traceback" not in result.stderr


def test_verify_lock_rejects_no_match_without_fallback_or_traceback(tmp_path):
    nonmatching = _matching_lock()
    nonmatching["annotation_id"] = "OTHER-ANNOTATION"
    result = _run_verify_lock(tmp_path, [nonmatching])

    assert result.returncode == 2
    assert "no lock row matches annotation_id" in result.stderr
    assert "verification=" not in result.stdout
    assert "Traceback" not in result.stderr


def test_verify_lock_rejects_multiple_matching_rows_as_ambiguous(tmp_path):
    result = _run_verify_lock(
        tmp_path,
        [_matching_lock("LOCK-1"), _matching_lock("LOCK-2")],
    )

    assert result.returncode == 2
    assert "verification is ambiguous" in result.stderr
    assert "verification=" not in result.stdout
    assert "Traceback" not in result.stderr
