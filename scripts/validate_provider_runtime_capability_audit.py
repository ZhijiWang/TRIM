"""Validate the metadata-only provider/runtime audit and frozen boundaries."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trim_haa.llm.hashing import verify_record_hash  # noqa: E402


HISTORICAL_BYTE_HASHES = {
    "data/studies/human_llm_pilot/provider_model_account_verification.json": "7db8d139b84601db605b7a0a4ebf977ec5ad4f33c1dc856b9007ebfee36ca357",
    "data/studies/human_llm_pilot/runtime_settings_draft.json": "4382f806b125f9e28314d83f4e4e1c2f69072e34f9b1cea12c00bc62118e8534",
}
FROZEN_PUBLIC_PR18_BYTE_HASHES = {
    "data/studies/human_llm_pilot/allocation_manifest.json": "bfbef4ab96f1772070d54061244fbf16b57b988bf725e75e01db23960dd800db",
    "data/studies/human_llm_pilot/freeze_package_manifest.json": "5ca8b38cf007c6c2d903b85750110f600ca49c170dabe95d870baa89a1aa1b9d",
    "data/studies/human_llm_pilot/manual_freeze_manifest.json": "86749490e12fa14e164d7affb80e81654bfb7549114b67de3322cf831a97a19d",
    "data/studies/human_llm_pilot/prompt_assembly_manifest.json": "1c20de3eef8279220df8e6be2ae3337fc4a40e9f91d789ca8f305e601c805d08",
    "data/studies/human_llm_pilot/sample_manifest.json": "2679d8fbcbb4da74b6232b3a82cebe653116b35c28a69562387562c36c2b6a7f",
    "schemas/human_llm_model_response.schema.json": "84fbc5413951c712925d85738bc820d776c1ab06172382f143e48495d4a095ec",
}
SECRET_VALUE_RE = re.compile(
    r"(sk-[A-Za-z0-9_-]{8,}|Bearer\s+[A-Za-z0-9._-]+|Authorization\s*[:=]\s*[^\s,;]+)",
    re.IGNORECASE,
)
FORBIDDEN_PUBLIC_KEYS = {
    "api_key",
    "authorization_header",
    "credential_value",
    "input",
    "prompt",
    "prompt_text",
    "raw_headers",
    "raw_provider_request",
    "request_headers",
    "source",
    "source_packet",
    "source_text",
}


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _walk(value: Any):
    yield value
    if isinstance(value, dict):
        for item in value.values():
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)


def _forbidden_key_paths(value: Any, prefix: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}"
            if key.lower() in FORBIDDEN_PUBLIC_KEYS:
                found.append(path)
            found.extend(_forbidden_key_paths(item, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(_forbidden_key_paths(item, f"{prefix}[{index}]"))
    return found


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    provider_path = root / "data/studies/human_llm_pilot/provider_model_account_verification_v0_2.json"
    runtime_path = root / "data/studies/human_llm_pilot/runtime_capability_audit_v0_1.json"
    provider_schema_path = root / "schemas/human_llm_provider_account_verification.schema.json"
    runtime_schema_path = root / "schemas/human_llm_runtime_capability_audit.schema.json"

    for path in (provider_path, runtime_path, provider_schema_path, runtime_schema_path):
        if not path.is_file():
            errors.append(f"missing provider/runtime audit path: {path.relative_to(root)}")
    if errors:
        return errors

    provider = _load_json(provider_path)
    runtime = _load_json(runtime_path)
    provider_schema = _load_json(provider_schema_path)
    runtime_schema = _load_json(runtime_schema_path)
    checker = FormatChecker()
    for label, record, schema in (
        ("provider verification", provider, provider_schema),
        ("runtime capability", runtime, runtime_schema),
    ):
        schema_errors = list(Draft202012Validator(schema, format_checker=checker).iter_errors(record))
        if schema_errors:
            errors.append(f"{label} schema validation failed: {schema_errors[0].message}")
        if not verify_record_hash(record):
            errors.append(f"{label} canonical record hash mismatch")
        forbidden = _forbidden_key_paths(record)
        if forbidden:
            errors.append(f"{label} contains forbidden public fields: {', '.join(forbidden)}")
        for item in _walk(record):
            if isinstance(item, str) and SECRET_VALUE_RE.search(item):
                errors.append(f"{label} contains credential-like material")
                break

    for relative, expected in {**HISTORICAL_BYTE_HASHES, **FROZEN_PUBLIC_PR18_BYTE_HASHES}.items():
        path = root / relative
        if not path.is_file() or _sha256(path) != expected:
            errors.append(f"protected historical/frozen file changed: {relative}")

    if runtime.get("provider_verification_record_hash") != provider.get("record_hash"):
        errors.append("runtime audit does not reference the provider record hash")
    if runtime.get("historical_runtime_draft_byte_hash") != "sha256:" + HISTORICAL_BYTE_HASHES[
        "data/studies/human_llm_pilot/runtime_settings_draft.json"
    ]:
        errors.append("runtime audit historical draft byte hash mismatch")

    provider_passed = provider.get("provider_account_gate_status") == (
        "PASSED_METADATA_ACCESS_VERIFIED_INFERENCE_NOT_AUTHORIZED"
    )
    exact_metadata_evidence = all(
        (
            provider.get("credential_present") is True,
            provider.get("metadata_request_performed") is True,
            provider.get("http_result_class") == "SUCCESS",
            provider.get("account_access_result") == "EXACT_MODEL_METADATA_ACCESS_VERIFIED",
            provider.get("returned_model_identifier") == "gpt-5.4-mini",
        )
    )
    if provider_passed and not exact_metadata_evidence:
        errors.append("provider account is passed without successful exact-model metadata evidence")

    for record_name, record in (("provider", provider), ("runtime", runtime)):
        if record.get("inference_performed", False) is not False:
            errors.append(f"{record_name} record claims inference")
        if record.get("responses_api_called", False) is not False:
            errors.append(f"{record_name} record claims Responses API inference use")
        if record.get("prompt_transmitted", False) is not False:
            errors.append(f"{record_name} record claims prompt transmission")
        if record.get("private_packet_accessed", False) is not False:
            errors.append(f"{record_name} record claims private packet access")

    if runtime.get("runtime_frozen") is not False or runtime.get("synthetic_inference_verification_performed") is not False:
        errors.append("runtime is frozen or synthetic inference is incorrectly claimed")
    if runtime.get("data_handling_boundary", {}).get("zero_data_retention_claimed") is not False:
        errors.append("Zero Data Retention is claimed without account-level evidence")
    if runtime.get("data_handling_boundary", {}).get("account_level_control_evidence_present") is not False:
        errors.append("account-level retention evidence is incorrectly claimed")

    for label, record in (("provider", provider), ("runtime", runtime)):
        if record.get("pricing_status") != "BLOCKED_PENDING_POINT_IN_TIME_PRICING_FREEZE":
            errors.append(f"{label} pricing is not blocked")
        if record.get("final_authorization_status") != "BLOCKED":
            errors.append(f"{label} final authorization is not blocked")
        if record.get("human_coding_status") != "BLOCKED":
            errors.append(f"{label} human coding is not blocked")
        if record.get("model_execution_status") != "BLOCKED":
            errors.append(f"{label} model execution is not blocked")
        if record.get("overall_execution_status") != "EXECUTION_BLOCKED":
            errors.append(f"{label} overall execution is not blocked")
    if runtime.get("execution_allowed") is not False:
        errors.append("runtime audit allows execution")

    gate_manifest = _load_json(root / "data/studies/human_llm_pilot/gate_status_manifest.json")
    gate_status = {entry["gate"]: entry["status"] for entry in gate_manifest["gates"]}
    for gate in ("provider_model_account", "runtime_settings", "pricing", "final_authorization", "human_coding", "model_execution"):
        if gate_status.get(gate) != "BLOCKED":
            errors.append(f"existing gate manifest changed: {gate}")

    implementation = "\n".join(
        (root / path).read_text(encoding="utf-8")
        for path in (
            "src/trim_haa/llm/provider_metadata.py",
            "scripts/audit_openai_model_metadata.py",
        )
    )
    for forbidden_transport in ("/v1/responses", "/v1/chat/completions", ".responses.create", ".chat.completions.create"):
        if forbidden_transport in implementation:
            errors.append(f"provider metadata implementation contains inference transport: {forbidden_transport}")
    if "https://api.openai.com/v1/models/gpt-5.4-mini" not in implementation:
        errors.append("provider metadata implementation is not pinned to exact-model retrieval")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PROVIDER_RUNTIME_CAPABILITY_AUDIT_VALID_EXECUTION_BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
