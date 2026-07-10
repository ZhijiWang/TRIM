"""Immutable annotation locking and hash verification rules."""

from __future__ import annotations

import hashlib
from copy import deepcopy
from typing import Any

from trim_haa.llm.hashing import canonical_json_bytes, compute_record_hash, verify_record_hash


IMMUTABLE_STATUSES = {"LOCKED", "AMENDED", "SUPERSEDED", "ADJUDICATED"}


class LockedAnnotationError(RuntimeError):
    """Raised when code attempts to alter an immutable annotation record."""


class AnnotationStateError(RuntimeError):
    """Raised when a lifecycle transition is not permitted."""


def finalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a copied record with its canonical prefixed record hash."""

    finalized = deepcopy(record)
    finalized["record_hash"] = compute_record_hash(finalized)
    return finalized


def frozen_coder_payload_hash(payload: dict[str, Any]) -> str:
    """Use the frozen coder schema's unprefixed 64-hex payload convention."""

    value = deepcopy(payload)
    value.pop("record_hash", None)
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def verify_frozen_coder_payload_hash(payload: dict[str, Any]) -> bool:
    claimed = payload.get("record_hash")
    return isinstance(claimed, str) and claimed == frozen_coder_payload_hash(payload)


def assert_record_hash_valid(record: dict[str, Any]) -> None:
    if not verify_record_hash(record):
        raise AnnotationStateError("annotation record hash is invalid")


def assert_mutable(record: dict[str, Any]) -> None:
    status = record.get("annotation_lifecycle_status")
    if status in IMMUTABLE_STATUSES:
        raise LockedAnnotationError(f"annotation record is immutable in state {status}")
    if status != "DRAFT":
        raise AnnotationStateError(f"annotation cannot be edited in state {status}")
