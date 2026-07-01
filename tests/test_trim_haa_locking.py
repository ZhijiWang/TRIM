from trim_haa.locking import (
    annotation_sha256,
    canonical_annotation_payload,
    create_lock_record,
    verify_locked_annotation,
)
from trim_haa.schema import TrimHAAAnnotation


def _locked_record():
    return TrimHAAAnnotation(
        annotation_id="H01_C01_PRE",
        case_id="C01",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_pre",
        primary_evidence_segment_ids=("C01_S1", "C01_S2"),
        function_label="label_a",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="Human pre record.",
        alternative_pathway_present="no",
        status="locked",
    )


def test_canonical_serialisation_determinism():
    left = _locked_record()
    right = TrimHAAAnnotation.from_record(left.to_csv_record())

    assert canonical_annotation_payload(left) == canonical_annotation_payload(right)
    assert annotation_sha256(left) == annotation_sha256(right)


def test_lock_hash_generation_and_verification():
    record = _locked_record()
    lock = create_lock_record(
        record,
        lock_manifest_id="LOCK_C01_PRE",
        locked_at="2026-07-01T00:00:00+00:00",
        locked_by="researcher",
    )

    assert lock.canonical_record_sha256 == annotation_sha256(record)
    assert verify_locked_annotation(record, lock)


def test_lock_tampering_detection():
    record = _locked_record()
    lock = create_lock_record(
        record,
        lock_manifest_id="LOCK_C01_PRE",
        locked_at="2026-07-01T00:00:00+00:00",
        locked_by="researcher",
    )
    modified = TrimHAAAnnotation.from_record(
        {
            **record.to_csv_record(),
            "rationale_note": "Modified after lock.",
        }
    )

    assert not verify_locked_annotation(modified, lock)
