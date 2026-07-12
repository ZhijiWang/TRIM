"""Copy-on-transition human annotation lifecycle and amendment workflow."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .locking import (
    AnnotationStateError,
    LockedAnnotationError,
    assert_mutable,
    assert_record_hash_valid,
    finalize_record,
    verify_frozen_coder_payload_hash,
)


PROTECTED_DRAFT_FIELDS = {
    "annotation_id",
    "annotation_record_version",
    "coder_id",
    "case_id",
    "session_id",
    "annotation_lifecycle_status",
    "created_timestamp",
    "submitted_timestamp",
    "locked_timestamp",
    "amendment_count",
    "supersedes_record",
    "superseded_by_record",
    "record_hash",
}


def edit_draft(record: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    """Edit a draft by returning a new hash-finalized copy."""

    assert_mutable(record)
    protected = PROTECTED_DRAFT_FIELDS.intersection(updates)
    if protected:
        raise AnnotationStateError(f"draft edit attempts protected fields: {sorted(protected)}")
    edited = deepcopy(record)
    edited.update(deepcopy(updates))
    payload = edited.get("coder_payload")
    if not isinstance(payload, dict) or not verify_frozen_coder_payload_hash(payload):
        raise AnnotationStateError("edited draft requires a valid frozen-schema coder payload hash")
    return finalize_record(edited)


def submit_annotation(record: dict[str, Any], *, submitted_timestamp: str) -> dict[str, Any]:
    assert_mutable(record)
    submitted = deepcopy(record)
    submitted["annotation_lifecycle_status"] = "SUBMITTED"
    submitted["submitted_timestamp"] = submitted_timestamp
    submitted["locked_timestamp"] = None
    return finalize_record(submitted)


def lock_annotation(record: dict[str, Any], *, locked_timestamp: str) -> dict[str, Any]:
    if record.get("annotation_lifecycle_status") != "SUBMITTED":
        if record.get("annotation_lifecycle_status") in {"LOCKED", "AMENDED", "SUPERSEDED", "ADJUDICATED"}:
            raise LockedAnnotationError("annotation is already immutable")
        raise AnnotationStateError("only a submitted annotation may be locked")
    assert_record_hash_valid(record)
    locked = deepcopy(record)
    locked["annotation_lifecycle_status"] = "LOCKED"
    locked["locked_timestamp"] = locked_timestamp
    return finalize_record(locked)


def create_amendment(
    prior_record: dict[str, Any],
    *,
    amendment_annotation_id: str,
    amended_coder_payload: dict[str, Any],
    created_timestamp: str,
    submitted_timestamp: str,
    locked_timestamp: str,
) -> dict[str, Any]:
    """Create a new immutable amendment; never alter the prior locked record."""

    if prior_record.get("annotation_lifecycle_status") != "LOCKED":
        raise LockedAnnotationError("correction requires a valid LOCKED prior annotation")
    assert_record_hash_valid(prior_record)
    if not verify_frozen_coder_payload_hash(amended_coder_payload):
        raise AnnotationStateError("amendment coder payload hash is invalid")
    amendment = deepcopy(prior_record)
    amendment.update(
        {
            "annotation_id": amendment_annotation_id,
            "coder_payload": deepcopy(amended_coder_payload),
            "annotation_lifecycle_status": "AMENDED",
            "created_timestamp": created_timestamp,
            "submitted_timestamp": submitted_timestamp,
            "locked_timestamp": locked_timestamp,
            "amendment_count": int(prior_record.get("amendment_count", 0)) + 1,
            "supersedes_record": {
                "annotation_id": prior_record["annotation_id"],
                "record_hash": prior_record["record_hash"],
            },
            "superseded_by_record": None,
            "record_hash": "",
        }
    )
    return finalize_record(amendment)


def create_superseded_record(
    prior_record: dict[str, Any], amendment_record: dict[str, Any]
) -> dict[str, Any]:
    """Return a new superseded lifecycle record while preserving both inputs."""

    if prior_record.get("annotation_lifecycle_status") != "LOCKED":
        raise LockedAnnotationError("only a locked record may receive a supersession link")
    assert_record_hash_valid(prior_record)
    assert_record_hash_valid(amendment_record)
    expected = {
        "annotation_id": prior_record.get("annotation_id"),
        "record_hash": prior_record.get("record_hash"),
    }
    if amendment_record.get("supersedes_record") != expected:
        raise AnnotationStateError("amendment does not reference the prior locked record hash")
    superseded = deepcopy(prior_record)
    superseded["annotation_lifecycle_status"] = "SUPERSEDED"
    superseded["superseded_by_record"] = {
        "annotation_id": amendment_record["annotation_id"],
        "record_hash": amendment_record["record_hash"],
    }
    return finalize_record(superseded)


def validate_adjudication_sources(
    adjudication_record: dict[str, Any], source_annotation_records: list[dict[str, Any]]
) -> None:
    if len(source_annotation_records) < 2:
        raise AnnotationStateError("adjudication requires at least two source annotations")
    for record in source_annotation_records:
        assert_record_hash_valid(record)
    expected = sorted(record["record_hash"] for record in source_annotation_records)
    claimed = sorted(adjudication_record.get("source_annotation_record_hashes", []))
    if claimed != expected:
        raise AnnotationStateError("adjudication does not reference every source annotation hash")
