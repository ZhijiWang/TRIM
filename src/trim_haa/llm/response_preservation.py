"""Raw synthetic-response preservation followed by parsing and schema validation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hashing import canonical_json_bytes, compute_record_hash, response_byte_hash, sha256_bytes
from .schema_validation import schema_error_summaries


@dataclass(frozen=True)
class ResponseParseResult:
    envelope: dict[str, Any]
    payload: dict[str, Any] | None
    lifecycle_events: tuple[str, ...]


def preserve_raw_response(raw_response: bytes, controlled_path: str | Path) -> str:
    """Write exact bytes to controlled storage and return their hash."""

    path = Path(controlled_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw_response)
    return response_byte_hash(raw_response)


def parse_preserved_response(
    controlled_path: str | Path,
    *,
    expected_raw_hash: str,
    response_schema: dict[str, Any],
    controlled_reference: str,
    run_id: str = "synthetic_run_id",
) -> ResponseParseResult:
    """Parse only bytes already preserved at ``controlled_path``; never echo content in metadata."""

    path = Path(controlled_path)
    raw = path.read_bytes()
    lifecycle = ["raw_response_preserved", "raw_response_hashed"]
    actual_hash = response_byte_hash(raw)
    if actual_hash != expected_raw_hash:
        raise ValueError("preserved raw response hash mismatch")
    lifecycle.append("parsing_attempted")

    payload: dict[str, Any] | None = None
    parsing_status = "invalid_json"
    validation_status = "not_attempted"
    parsed_hash: str | None = None
    error_class: str | None = None
    error_summary: str | None = None
    try:
        decoded = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        error_class = "INVALID_JSON"
        if isinstance(exc, json.JSONDecodeError):
            error_summary = f"invalid_json:line={exc.lineno}:column={exc.colno}"
        else:
            error_summary = "invalid_json:utf8_decode_failed"
    else:
        parsing_status = "parsed_json"
        lifecycle.append("schema_validation_attempted")
        if not isinstance(decoded, dict):
            errors = ["schema_validation_failed:type:<root>"]
        else:
            errors = schema_error_summaries(decoded, response_schema)
        if errors:
            validation_status = "FAILED"
            error_class = "SCHEMA_VALIDATION_FAILED"
            error_summary = ";".join(errors[:8])
        else:
            validation_status = "PASSED"
            payload = decoded
            parsed_hash = sha256_bytes(canonical_json_bytes(decoded))

    envelope: dict[str, Any] = {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "request_record_hash": "sha256:" + "6" * 64,
        "provider": "synthetic_fixture_provider",
        "model": "synthetic_fixture_model",
        "provider_response_id": None,
        "response_received": True,
        "raw_response_preserved": True,
        "controlled_response_reference": controlled_reference,
        "raw_response_byte_hash": actual_hash,
        "provider_metadata_hash": None,
        "parsing_attempted": True,
        "parsing_status": parsing_status,
        "parsed_payload_hash": parsed_hash,
        "model_response_schema_validation_status": validation_status,
        "retry_metadata": {
            "retry_count": 0,
            "retry_policy_status": "no_retry_synthetic_fixture",
        },
        "error_class": error_class,
        "error_message_summary": error_summary,
        "record_hash": "",
    }
    envelope["record_hash"] = compute_record_hash(envelope)
    return ResponseParseResult(envelope=envelope, payload=payload, lifecycle_events=tuple(lifecycle))


def preserve_and_parse_synthetic_response(
    raw_response: bytes,
    controlled_path: str | Path,
    *,
    response_schema: dict[str, Any],
    controlled_reference: str = "controlled://synthetic/response",
) -> ResponseParseResult:
    raw_hash = preserve_raw_response(raw_response, controlled_path)
    return parse_preserved_response(
        controlled_path,
        expected_raw_hash=raw_hash,
        response_schema=response_schema,
        controlled_reference=controlled_reference,
    )
