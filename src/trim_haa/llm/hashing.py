"""Deterministic UTF-8 serialization and SHA-256 helpers for LLM records."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any


HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize JSON deterministically as compact UTF-8 bytes."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    """Return a prefixed lowercase SHA-256 digest."""

    return f"sha256:{hashlib.sha256(value).hexdigest()}"


def compute_record_hash(record: dict[str, Any]) -> str:
    """Hash a record after excluding its top-level ``record_hash`` field."""

    payload = deepcopy(record)
    payload.pop("record_hash", None)
    return sha256_bytes(canonical_json_bytes(payload))


def verify_record_hash(record: dict[str, Any]) -> bool:
    """Return whether a record carries its valid canonical hash."""

    claimed = record.get("record_hash")
    return isinstance(claimed, str) and bool(HASH_PATTERN.fullmatch(claimed)) and claimed == compute_record_hash(record)


def request_byte_hash(value: bytes) -> str:
    """Hash the exact preserved provider-bound request bytes."""

    return sha256_bytes(value)


def response_byte_hash(value: bytes) -> str:
    """Hash the exact raw response bytes before parsing."""

    return sha256_bytes(value)


def normalized_file_bytes(path: str | Path) -> bytes:
    """Read public file bytes and normalize line endings for frozen file hashes."""

    return Path(path).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def verify_schema_hash(path: str | Path, expected_hash: str) -> bool:
    """Verify a schema's LF-normalized bytes against a prefixed digest."""

    return bool(HASH_PATTERN.fullmatch(expected_hash)) and sha256_bytes(normalized_file_bytes(path)) == expected_hash
