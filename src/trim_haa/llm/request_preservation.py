"""Synthetic-only request serialization and preservation lifecycle."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .hashing import canonical_json_bytes, compute_record_hash, request_byte_hash


SYNTHETIC_CASE_ID = "synthetic_case_id"
SYNTHETIC_TEXT = "synthetic_placeholder_non_source_text_v1"
ALLOWED_SYNTHETIC_FIELDS = {
    "case_id",
    "condition",
    "model_candidate",
    "placeholder_input",
    "response_schema_hash",
}


def build_synthetic_request_representation(
    *,
    model_candidate: str,
    response_schema_hash: str,
    condition: str = "synthetic_condition",
) -> dict[str, Any]:
    """Build a provider-neutral placeholder representation, never a live request body."""

    return {
        "case_id": SYNTHETIC_CASE_ID,
        "condition": condition,
        "model_candidate": model_candidate,
        "placeholder_input": SYNTHETIC_TEXT,
        "response_schema_hash": response_schema_hash,
    }


def serialize_synthetic_request(request: dict[str, Any]) -> bytes:
    if set(request) != ALLOWED_SYNTHETIC_FIELDS:
        raise ValueError("synthetic request representation has unexpected fields")
    if request.get("case_id") != SYNTHETIC_CASE_ID or request.get("placeholder_input") != SYNTHETIC_TEXT:
        raise ValueError("request preservation scaffold accepts only the fixed synthetic placeholder")
    return canonical_json_bytes(request)


def preserve_synthetic_request(
    request: dict[str, Any],
    controlled_path: str | Path,
) -> tuple[bytes, str]:
    """Serialize and preserve exact synthetic bytes before creating public metadata."""

    serialized = serialize_synthetic_request(request)
    path = Path(controlled_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(serialized)
    return serialized, request_byte_hash(serialized)


def create_request_envelope(
    *,
    request_bytes: bytes,
    controlled_payload_reference: str,
    run_id: str = "synthetic_run_id",
    created_at: str = "2026-07-10T00:00:00+10:00",
) -> dict[str, Any]:
    """Create public metadata after synthetic request preservation has completed."""

    byte_hash = request_byte_hash(request_bytes)
    envelope: dict[str, Any] = {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "case_id": SYNTHETIC_CASE_ID,
        "condition": "synthetic_condition",
        "provider": "OpenAI",
        "model": "gpt-5.4-mini",
        "runtime_settings_record_hash": "sha256:" + "1" * 64,
        "prompt_template_hash": "sha256:" + "2" * 64,
        "prompt_instance_hash": "sha256:" + "3" * 64,
        "source_packet_hash": "sha256:" + "4" * 64,
        "response_schema_hash": "sha256:" + "5" * 64,
        "request_serialization_format": "canonical_json_utf8",
        "request_byte_hash": byte_hash,
        "created_at": created_at,
        "gate_snapshot": {
            "decision": "EXECUTION_BLOCKED",
            "provider_model_account": "BLOCKED",
            "runtime_settings": "BLOCKED",
            "pricing": "BLOCKED",
            "final_authorization": "BLOCKED",
            "model_execution": "BLOCKED",
        },
        "request_preserved": True,
        "transmission_authorized": False,
        "transmitted": False,
        "provider_request_id": None,
        "controlled_payload": {
            "controlled_payload_reference": controlled_payload_reference,
            "controlled_payload_hash": byte_hash,
            "controlled_storage_location_class": "ephemeral_synthetic_test_storage",
            "private_packet_access_log_reference": "not_applicable_synthetic_fixture",
            "provider_transmission_authorization_reference": "not_authorized",
        },
        "record_hash": "",
    }
    envelope["record_hash"] = compute_record_hash(envelope)
    return envelope
