import hashlib
import json
import urllib.error
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from scripts import audit_openai_model_metadata
from scripts.validate_provider_runtime_capability_audit import (
    FROZEN_PUBLIC_PR18_BYTE_HASHES,
    HISTORICAL_BYTE_HASHES,
    validate as validate_provider_runtime_audit,
)
from trim_haa.llm.hashing import compute_record_hash, verify_record_hash
from trim_haa.llm.provider_metadata import (
    FROZEN_CANDIDATE_MODEL,
    MODEL_METADATA_ENDPOINT_CLASS,
    MODEL_METADATA_URL,
    audit_exact_model_metadata,
    redact_sensitive_text,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "studies" / "human_llm_pilot"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def provider_record():
    return load_json(DATA / "provider_model_account_verification_v0_2.json")


def runtime_record():
    return load_json(DATA / "runtime_capability_audit_v0_1.json")


def schema_errors(record, name):
    schema = load_json(ROOT / "schemas" / name)
    return list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))


class FakeResponse:
    def __init__(self, payload, status=200):
        self.status = status
        self._raw = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, _limit):
        return self._raw


def http_error(code):
    return urllib.error.HTTPError(MODEL_METADATA_URL, code, "safe", {}, None)


def test_no_key_path_is_blocked_without_network(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def forbidden_opener(*_args, **_kwargs):
        raise AssertionError("network opener must not be called")

    result = audit_exact_model_metadata(None, opener=forbidden_opener)
    assert result.audit_status == "BLOCKED_NO_CREDENTIAL_AVAILABLE"
    assert result.metadata_request_performed is False
    assert result.credential_present is False
    assert result.inference_performed is False
    assert result.prompt_transmitted is False


def test_no_key_command_is_a_successful_fail_closed_audit(monkeypatch, capsys):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert audit_openai_model_metadata.main() == 0
    public = json.loads(capsys.readouterr().out)
    assert public["audit_status"] == "BLOCKED_NO_CREDENTIAL_AVAILABLE"
    assert public["credential_present"] is False
    assert "api_key" not in public


def test_exact_model_metadata_success_uses_mock_only():
    captured = {}

    def opener(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["has_body"] = request.data is not None
        captured["timeout"] = timeout
        return FakeResponse({"id": FROZEN_CANDIDATE_MODEL, "object": "model", "owned_by": "openai"})

    result = audit_exact_model_metadata("synthetic-test-credential", opener=opener, timestamp="2026-07-13T00:00:00+00:00")
    assert captured == {"url": MODEL_METADATA_URL, "method": "GET", "has_body": False, "timeout": 10}
    assert result.audit_status == "METADATA_ACCESS_VERIFIED_INFERENCE_NOT_AUTHORIZED"
    assert result.account_access_result == "EXACT_MODEL_METADATA_ACCESS_VERIFIED"
    assert result.returned_model_identifier == FROZEN_CANDIDATE_MODEL
    assert result.metadata_endpoint_class == MODEL_METADATA_ENDPOINT_CLASS
    assert result.inference_performed is False
    assert result.responses_api_called is False
    assert result.prompt_transmitted is False


def test_non_provider_owned_by_value_is_suppressed():
    result = audit_exact_model_metadata(
        "synthetic-test-credential",
        opener=lambda *_args, **_kwargs: FakeResponse(
            {"id": FROZEN_CANDIDATE_MODEL, "object": "model", "owned_by": "synthetic_non_provider_owner"}
        ),
        timestamp="2026-07-13T00:00:00+00:00",
    )
    assert result.provider_owned_by is None
    assert result.provider_owned_by_suppressed is True


def test_model_not_accessible_path_is_blocked():
    def opener(*_args, **_kwargs):
        raise http_error(404)

    result = audit_exact_model_metadata("synthetic-test-credential", opener=opener)
    assert result.audit_status == "BLOCKED_MODEL_NOT_ACCESSIBLE"
    assert result.account_access_result == "EXACT_MODEL_NOT_ACCESSIBLE"
    assert result.inference_performed is False


def test_authentication_failure_path_is_blocked():
    def opener(*_args, **_kwargs):
        raise http_error(401)

    result = audit_exact_model_metadata("synthetic-test-credential", opener=opener)
    assert result.audit_status == "BLOCKED_AUTHENTICATION_FAILED"
    assert result.http_result_class == "AUTHENTICATION_FAILURE"
    assert result.error_message_summary == "provider metadata request returned HTTP 401"


@pytest.mark.parametrize("status, result_class", [(429, "RATE_LIMITED"), (500, "PROVIDER_ERROR")])
def test_rate_limit_and_provider_error_paths_fail_closed(status, result_class):
    def opener(*_args, **_kwargs):
        raise http_error(status)

    result = audit_exact_model_metadata("synthetic-test-credential", opener=opener)
    assert result.audit_status == "BLOCKED_PROVIDER_ERROR"
    assert result.http_result_class == result_class
    assert result.inference_performed is False


def test_secret_redaction_removes_credential_like_values():
    secret = "sk-" + "x" * 32
    message = f"Authorization: Bearer {secret}; api failed"
    redacted = redact_sensitive_text(message)
    assert secret not in redacted
    assert "Bearer" not in redacted
    assert "Authorization:" not in redacted
    assert "[REDACTED]" in redacted


@pytest.mark.parametrize("field", ["prompt", "prompt_text", "source", "source_text", "api_key", "request_headers"])
def test_provider_schema_rejects_forbidden_public_fields(field):
    record = provider_record()
    record[field] = "synthetic-forbidden-value"
    assert schema_errors(record, "human_llm_provider_account_verification.schema.json")


@pytest.mark.parametrize(
    "field",
    [
        "inference_performed",
        "responses_api_called",
        "prompt_transmitted",
        "private_content_transmitted",
        "private_packet_accessed",
        "credential_material_recorded",
    ],
)
def test_provider_record_cannot_claim_forbidden_activity(field):
    record = provider_record()
    record[field] = True
    assert schema_errors(record, "human_llm_provider_account_verification.schema.json")


def test_provider_pass_requires_successful_exact_model_metadata_evidence():
    record = provider_record()
    record["provider_account_gate_status"] = "PASSED_METADATA_ACCESS_VERIFIED_INFERENCE_NOT_AUTHORIZED"
    record["record_hash"] = compute_record_hash(record)
    assert schema_errors(record, "human_llm_provider_account_verification.schema.json")


def test_zero_data_retention_cannot_be_inferred_from_public_documentation():
    record = runtime_record()
    boundary = record["data_handling_boundary"]
    boundary["zero_data_retention_claimed"] = True
    boundary["zero_data_retention_status"] = "VERIFIED"
    boundary["account_level_control_evidence_present"] = False
    assert schema_errors(record, "human_llm_runtime_capability_audit.schema.json")


def test_account_metadata_pass_does_not_pass_runtime_pricing_authorization_or_execution():
    result = audit_exact_model_metadata(
        "synthetic-test-credential",
        opener=lambda *_args, **_kwargs: FakeResponse(
            {"id": FROZEN_CANDIDATE_MODEL, "object": "model", "owned_by": "openai"}
        ),
        timestamp="2026-07-13T00:00:00+00:00",
    )
    runtime = runtime_record()
    assert result.audit_status == "METADATA_ACCESS_VERIFIED_INFERENCE_NOT_AUTHORIZED"
    assert runtime["runtime_gate_status"] == "BLOCKED_PENDING_SYNTHETIC_NO_SOURCE_INFERENCE_VERIFICATION"
    assert runtime["pricing_status"] == "BLOCKED_PENDING_POINT_IN_TIME_PRICING_FREEZE"
    assert runtime["final_authorization_status"] == "BLOCKED"
    assert runtime["human_coding_status"] == "BLOCKED"
    assert runtime["model_execution_status"] == "BLOCKED"
    assert runtime["execution_allowed"] is False


def test_runtime_cannot_be_frozen_without_synthetic_inference_verification():
    record = runtime_record()
    record["runtime_frozen"] = True
    assert schema_errors(record, "human_llm_runtime_capability_audit.schema.json")


def test_checked_in_records_validate_and_have_canonical_hashes():
    provider = provider_record()
    runtime = runtime_record()
    assert not schema_errors(provider, "human_llm_provider_account_verification.schema.json")
    assert not schema_errors(runtime, "human_llm_runtime_capability_audit.schema.json")
    assert verify_record_hash(provider)
    assert verify_record_hash(runtime)
    assert runtime["provider_verification_record_hash"] == provider["record_hash"]


def test_historical_v01_records_remain_byte_identical():
    for relative, expected in HISTORICAL_BYTE_HASHES.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_frozen_public_pr18_references_remain_byte_identical():
    for relative, expected in FROZEN_PUBLIC_PR18_BYTE_HASHES.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_wheel_and_sdist_exclusions_remain_unchanged():
    packaging = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"trim_haa.llm"' in packaging
    assert '"trim_haa.llm.*"' in packaging
    assert '"trim_haa.human_coding"' in packaging
    assert '"trim_haa.human_coding.*"' in packaging
    assert "provider-runtime" not in packaging


def test_validator_accepts_checked_in_blocked_audit():
    assert validate_provider_runtime_audit(ROOT) == []


def test_validator_rejects_credential_like_error_summary(tmp_path):
    provider = provider_record()
    provider["error_class"] = "SyntheticError"
    provider["error_message_summary"] = "Bearer " + ("x" * 32)
    provider["record_hash"] = compute_record_hash(provider)
    target = tmp_path / "data/studies/human_llm_pilot"
    target.mkdir(parents=True)
    for relative in HISTORICAL_BYTE_HASHES:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((ROOT / relative).read_bytes())
    for relative in FROZEN_PUBLIC_PR18_BYTE_HASHES:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((ROOT / relative).read_bytes())
    for relative in (
        "schemas/human_llm_provider_account_verification.schema.json",
        "schemas/human_llm_runtime_capability_audit.schema.json",
        "data/studies/human_llm_pilot/runtime_capability_audit_v0_1.json",
        "data/studies/human_llm_pilot/gate_status_manifest.json",
        "src/trim_haa/llm/provider_metadata.py",
        "scripts/audit_openai_model_metadata.py",
    ):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((ROOT / relative).read_bytes())
    (target / "provider_model_account_verification_v0_2.json").write_text(
        json.dumps(provider), encoding="utf-8"
    )
    errors = validate_provider_runtime_audit(tmp_path)
    assert any("credential-like material" in error for error in errors)
