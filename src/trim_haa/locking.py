"""Cryptographic lock support for TRIM-HAA Core annotations."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from trim_haa.hashing import sha256_text
from trim_haa.schema import CORE_FIELDS, TrimHAAAnnotation, clean_text

LOCK_MANIFEST_FIELDS: tuple[str, ...] = (
    "lock_manifest_id",
    "annotation_id",
    "case_id",
    "annotation_stage",
    "actor_id",
    "canonical_record_sha256",
    "locked_at",
    "lock_status",
    "locked_by",
    "notes",
)


@dataclass(slots=True)
class LockRecord:
    """A stored hash proving a Core record was locked in a known state."""

    lock_manifest_id: str = ""
    annotation_id: str = ""
    case_id: str = ""
    annotation_stage: str = ""
    actor_id: str = ""
    canonical_record_sha256: str = ""
    locked_at: str = ""
    lock_status: str = "locked"
    locked_by: str = ""
    notes: str = ""

    def __post_init__(self) -> None:
        for field_name in LOCK_MANIFEST_FIELDS:
            setattr(self, field_name, clean_text(getattr(self, field_name)))

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "LockRecord":
        return cls(
            **{
                field_name: record.get(field_name, "")
                for field_name in LOCK_MANIFEST_FIELDS
            }
        )

    def to_record(self) -> dict[str, str]:
        return asdict(self)


def canonical_annotation_payload(
    annotation: TrimHAAAnnotation | Mapping[str, Any],
) -> str:
    """Return deterministic UTF-8-ready JSON payload for a Core annotation."""

    if not isinstance(annotation, TrimHAAAnnotation):
        annotation = TrimHAAAnnotation.from_record(annotation)
    values: dict[str, str] = {}
    for field_name in CORE_FIELDS:
        value = getattr(annotation, field_name)
        if field_name == "primary_evidence_segment_ids":
            values[field_name] = "|".join(value)
        else:
            values[field_name] = clean_text(value).replace("\r\n", "\n").replace("\r", "\n")
    return json.dumps(
        values,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=False,
    )


def annotation_sha256(annotation: TrimHAAAnnotation | Mapping[str, Any]) -> str:
    """Hash the canonical Core annotation payload with SHA-256."""

    return sha256_text(canonical_annotation_payload(annotation))


def create_lock_record(
    annotation: TrimHAAAnnotation | Mapping[str, Any],
    *,
    lock_manifest_id: str,
    locked_at: str,
    locked_by: str,
    notes: str = "",
) -> LockRecord:
    """Create a lock-manifest row from the current annotation payload."""

    if not isinstance(annotation, TrimHAAAnnotation):
        annotation = TrimHAAAnnotation.from_record(annotation)
    return LockRecord(
        lock_manifest_id=lock_manifest_id,
        annotation_id=annotation.annotation_id,
        case_id=annotation.case_id,
        annotation_stage=annotation.annotation_stage,
        actor_id=annotation.actor_id,
        canonical_record_sha256=annotation_sha256(annotation),
        locked_at=locked_at,
        lock_status=annotation.status,
        locked_by=locked_by,
        notes=notes,
    )


def lock_annotation(
    annotation: TrimHAAAnnotation | Mapping[str, Any],
    *,
    lock_manifest_id: str,
    locked_at: str,
    locked_by: str,
    notes: str = "",
) -> LockRecord:
    """Public alias for creating a lock record from a Core annotation."""

    return create_lock_record(
        annotation,
        lock_manifest_id=lock_manifest_id,
        locked_at=locked_at,
        locked_by=locked_by,
        notes=notes,
    )


def verify_locked_annotation(
    annotation: TrimHAAAnnotation | Mapping[str, Any],
    lock_record: LockRecord | Mapping[str, Any],
) -> bool:
    """Return whether the annotation matches its stored lock hash."""

    if not isinstance(annotation, TrimHAAAnnotation):
        annotation = TrimHAAAnnotation.from_record(annotation)
    if not isinstance(lock_record, LockRecord):
        lock_record = LockRecord.from_record(lock_record)
    return (
        lock_record.annotation_id == annotation.annotation_id
        and lock_record.case_id == annotation.case_id
        and lock_record.annotation_stage == annotation.annotation_stage
        and lock_record.actor_id == annotation.actor_id
        and lock_record.lock_status == "locked"
        and annotation_sha256(annotation) == lock_record.canonical_record_sha256
    )
