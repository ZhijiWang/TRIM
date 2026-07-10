import json
import http.client
import os
import socket
import subprocess
import sys
import types
import urllib.request
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from scripts import dry_run_human_llm_execution
from scripts.validate_human_llm_execution_scaffold import (
    EXPECTED_CASE_IDS,
    PR18_PROTECTED_EXACT,
    PR18_PROTECTED_PREFIXES,
    STARTING_PR20_HEAD,
    validate as validate_scaffold,
)
from trim_haa.llm.dry_run import build_execution_plan, run_dry_run
from trim_haa.llm.frozen_reference import load_and_verify_public_freeze
from trim_haa.llm.gates import (
    GateBlockedError,
    assert_human_coding_allowed,
    assert_model_execution_allowed,
    normalize_gate_manifest,
)
from trim_haa.llm.hashing import (
    canonical_json_bytes,
    compute_record_hash,
    request_byte_hash,
    verify_record_hash,
)
from trim_haa.llm.openai_adapter import (
    BlockedOpenAIAdapter,
    assert_provider_preconditions,
)
from trim_haa.llm.provider import ExecutionBlockedError
from trim_haa.llm.request_preservation import (
    build_synthetic_request_representation,
    create_request_envelope,
    preserve_synthetic_request,
    serialize_synthetic_request,
)
from trim_haa.llm.response_preservation import preserve_and_parse_synthetic_response
from trim_haa.llm.schema_validation import schema_error_summaries


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "human_llm_execution"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_schema(name: str):
    return load_json(ROOT / "schemas" / name)


def frozen_model_response_schema():
    return load_and_verify_public_freeze(ROOT)["model_response_schema"]


def synthetic_envelope():
    request = build_synthetic_request_representation(
        model_candidate="gpt-5.4-mini",
        response_schema_hash="sha256:84fbc5413951c712925d85738bc820d776c1ab06172382f143e48495d4a095ec",
    )
    return create_request_envelope(
        request_bytes=serialize_synthetic_request(request),
        controlled_payload_reference="controlled://synthetic/request",
    )


def current_gate_manifest():
    return load_json(ROOT / "data" / "studies" / "human_llm_pilot" / "gate_status_manifest.json")


def all_passed_gate_statuses():
    return {
        "provider_model_account": "PASSED",
        "runtime_settings": "PASSED",
        "pricing": "PASSED",
        "final_authorization": "PASSED",
        "human_coding": "PASSED",
        "model_execution": "PASSED",
    }


def hypothetical_frozen_runtime():
    return {
        "account_availability_status": "AVAILABLE_VERIFIED",
        "record_status": "FROZEN_VERIFIED",
        "provider_transmission_authorization_status": "PASSED",
        "final_authorization_status": "PASSED",
        "execution_allowed": True,
    }


def hypothetical_authorized_envelope():
    envelope = synthetic_envelope()
    envelope["transmission_authorized"] = True
    envelope["record_hash"] = compute_record_hash(envelope)
    return envelope


def git_bytes(revision: str, path: str):
    return subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def test_canonical_json_hashing_is_deterministic():
    first = {"z": [2, 1], "a": "synthetic"}
    second = {"a": "synthetic", "z": [2, 1]}

    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    assert compute_record_hash({**first, "record_hash": "ignored"}) == compute_record_hash(second)


def test_modifying_record_invalidates_hash():
    record = {"status": "BLOCKED", "record_hash": ""}
    record["record_hash"] = compute_record_hash(record)
    assert verify_record_hash(record)

    record["status"] = "PASSED"
    assert not verify_record_hash(record)


@pytest.mark.parametrize("field", ["prompt_text", "source_text", "credentials"])
def test_request_envelope_rejects_forbidden_public_fields(field):
    instance = synthetic_envelope()
    instance[field] = "synthetic_forbidden_field_value"

    assert list(Draft202012Validator(load_schema("human_llm_provider_request_envelope.schema.json")).iter_errors(instance))


def test_request_envelope_requires_transmission_authorized_false():
    instance = synthetic_envelope()
    instance["transmission_authorized"] = True

    assert list(Draft202012Validator(load_schema("human_llm_provider_request_envelope.schema.json")).iter_errors(instance))


def test_request_envelope_requires_transmitted_false():
    instance = synthetic_envelope()
    instance["transmitted"] = True

    assert list(Draft202012Validator(load_schema("human_llm_provider_request_envelope.schema.json")).iter_errors(instance))


def test_synthetic_request_is_preserved_before_envelope_creation(tmp_path):
    request = build_synthetic_request_representation(
        model_candidate="gpt-5.4-mini",
        response_schema_hash="sha256:" + "5" * 64,
    )
    raw, digest = preserve_synthetic_request(request, tmp_path / "controlled" / "request.json")

    assert (tmp_path / "controlled" / "request.json").read_bytes() == raw
    assert digest == request_byte_hash(raw)
    assert b"synthetic_placeholder_non_source_text_v1" in raw


def test_response_envelope_dry_run_requires_no_response():
    schema = load_schema("human_llm_provider_response_envelope.schema.json")
    instance = {
        "schema_version": "1.0.0",
        "run_id": "synthetic_run",
        "request_record_hash": "sha256:" + "1" * 64,
        "provider": "OpenAI",
        "model": "gpt-5.4-mini",
        "provider_response_id": None,
        "response_received": False,
        "raw_response_preserved": False,
        "controlled_response_reference": None,
        "raw_response_byte_hash": None,
        "provider_metadata_hash": None,
        "parsing_attempted": False,
        "parsing_status": "not_attempted",
        "parsed_payload_hash": None,
        "model_response_schema_validation_status": "not_attempted",
        "retry_metadata": {"retry_count": 0, "retry_policy_status": "no_call"},
        "error_class": None,
        "error_message_summary": None,
        "record_hash": "sha256:" + "2" * 64,
    }
    assert not list(Draft202012Validator(schema).iter_errors(instance))

    instance["response_received"] = True
    assert not list(Draft202012Validator(schema).iter_errors(instance))
    instance["response_received"] = False
    instance["raw_response_preserved"] = True
    assert list(Draft202012Validator(schema).iter_errors(instance))


def test_blocked_provider_adapter_raises_execution_blocked_error():
    decision = normalize_gate_manifest(current_gate_manifest())
    runtime = load_json(ROOT / "data" / "studies" / "human_llm_pilot" / "runtime_settings_draft.json")

    with pytest.raises(ExecutionBlockedError, match="provider_model_account"):
        BlockedOpenAIAdapter().send_request(
            synthetic_envelope(),
            gate_statuses=decision.statuses,
            runtime_settings=runtime,
            request_preserved=True,
            private_packet_access_authorization=None,
        )


def test_blocked_provider_adapter_performs_no_network_call(monkeypatch):
    calls = []

    def forbidden_socket(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("network attempted")

    monkeypatch.setattr(socket, "socket", forbidden_socket)
    with pytest.raises(ExecutionBlockedError):
        BlockedOpenAIAdapter().send_request(
            synthetic_envelope(),
            gate_statuses=normalize_gate_manifest(current_gate_manifest()).statuses,
            runtime_settings=load_json(ROOT / "data" / "studies" / "human_llm_pilot" / "runtime_settings_draft.json"),
            request_preserved=True,
            private_packet_access_authorization=None,
        )
    assert calls == []


def test_missing_provider_account_pass_blocks_execution():
    gates = all_passed_gate_statuses()
    gates["provider_model_account"] = "BLOCKED"
    with pytest.raises(ExecutionBlockedError, match="provider_model_account"):
        assert_provider_preconditions(
            hypothetical_authorized_envelope(),
            gate_statuses=gates,
            runtime_settings=hypothetical_frozen_runtime(),
            request_preserved=True,
            private_packet_access_authorization="synthetic_authorization_reference",
        )


def test_missing_runtime_pass_blocks_execution():
    gates = all_passed_gate_statuses()
    gates["runtime_settings"] = "BLOCKED"
    with pytest.raises(ExecutionBlockedError, match="runtime_settings"):
        assert_provider_preconditions(
            hypothetical_authorized_envelope(),
            gate_statuses=gates,
            runtime_settings=hypothetical_frozen_runtime(),
            request_preserved=True,
            private_packet_access_authorization="synthetic_authorization_reference",
        )


def test_missing_pricing_pass_blocks_execution():
    gates = all_passed_gate_statuses()
    gates["pricing"] = "BLOCKED"
    with pytest.raises(ExecutionBlockedError, match="pricing"):
        assert_provider_preconditions(
            hypothetical_authorized_envelope(),
            gate_statuses=gates,
            runtime_settings=hypothetical_frozen_runtime(),
            request_preserved=True,
            private_packet_access_authorization="synthetic_authorization_reference",
        )


def test_missing_final_authorization_blocks_execution():
    gates = all_passed_gate_statuses()
    gates["final_authorization"] = "BLOCKED"
    with pytest.raises(ExecutionBlockedError, match="final_authorization"):
        assert_provider_preconditions(
            hypothetical_authorized_envelope(),
            gate_statuses=gates,
            runtime_settings=hypothetical_frozen_runtime(),
            request_preserved=True,
            private_packet_access_authorization="synthetic_authorization_reference",
        )


def test_private_packet_authorization_absence_blocks_execution():
    with pytest.raises(ExecutionBlockedError, match="private-packet"):
        assert_provider_preconditions(
            hypothetical_authorized_envelope(),
            gate_statuses=all_passed_gate_statuses(),
            runtime_settings=hypothetical_frozen_runtime(),
            request_preserved=True,
            private_packet_access_authorization=None,
        )


def test_even_hypothetical_passes_have_no_network_implementation():
    with pytest.raises(ExecutionBlockedError, match="no provider network implementation"):
        BlockedOpenAIAdapter().send_request(
            hypothetical_authorized_envelope(),
            gate_statuses=all_passed_gate_statuses(),
            runtime_settings=hypothetical_frozen_runtime(),
            request_preserved=True,
            private_packet_access_authorization="synthetic_authorization_reference",
        )


def test_human_coding_blocked_state_blocks_coding_start():
    decision = normalize_gate_manifest(current_gate_manifest())
    with pytest.raises(GateBlockedError, match="human coding"):
        assert_human_coding_allowed(decision)


def test_model_execution_blocked_state_blocks_model_start():
    decision = normalize_gate_manifest(current_gate_manifest())
    with pytest.raises(GateBlockedError, match="model execution"):
        assert_model_execution_allowed(decision)


def test_rights_restricted_pass_is_sufficient_for_preparation():
    decision = normalize_gate_manifest(current_gate_manifest())
    assert decision.statuses["rights_evidence"] == "PASSED_WITH_DOWNSTREAM_GATES_BLOCKED"
    assert decision.preparation_allowed is True


def test_controlled_access_only_is_preparation_not_execution():
    decision = normalize_gate_manifest(current_gate_manifest())
    assert decision.statuses["controlled_private_packet_handling"] == "PASSED_WITH_CONTROLLED_ACCESS_ONLY"
    assert decision.preparation_allowed is True
    assert decision.execution_allowed is False
    assert decision.decision == "EXECUTION_BLOCKED"


def test_synthetic_valid_model_response_passes_frozen_schema():
    payload = load_json(FIXTURES / "synthetic_model_response_valid.json")
    assert schema_error_summaries(payload, frozen_model_response_schema()) == []


@pytest.mark.parametrize(
    "fixture_name",
    [
        "synthetic_model_response_unknown_category.json",
        "synthetic_model_response_missing_required.json",
        "synthetic_model_response_malformed_fields.json",
        "synthetic_model_response_extra_property.json",
    ],
)
def test_synthetic_invalid_model_responses_fail_frozen_schema(fixture_name):
    payload = load_json(FIXTURES / fixture_name)
    assert schema_error_summaries(payload, frozen_model_response_schema())


def test_invalid_json_is_reported_without_content(tmp_path):
    raw = (FIXTURES / "synthetic_model_response_invalid_json.txt").read_bytes()
    result = preserve_and_parse_synthetic_response(
        raw,
        tmp_path / "controlled" / "raw-response.json",
        response_schema=frozen_model_response_schema(),
    )
    assert result.envelope["parsing_status"] == "invalid_json"
    assert result.envelope["error_class"] == "INVALID_JSON"
    assert "selected_evidence" not in result.envelope["error_message_summary"]
    assert result.payload is None


def test_response_is_hashed_before_parsing(tmp_path):
    raw = (FIXTURES / "synthetic_model_response_valid.json").read_bytes()
    result = preserve_and_parse_synthetic_response(
        raw,
        tmp_path / "controlled" / "raw-response.json",
        response_schema=frozen_model_response_schema(),
    )
    assert result.lifecycle_events[:3] == (
        "raw_response_preserved",
        "raw_response_hashed",
        "parsing_attempted",
    )
    assert result.envelope["model_response_schema_validation_status"] == "PASSED"
    assert result.envelope["raw_response_byte_hash"].startswith("sha256:")
    assert result.envelope["parsed_payload_hash"].startswith("sha256:")


def test_schema_failure_summary_does_not_copy_response_content(tmp_path):
    raw = (FIXTURES / "synthetic_model_response_unknown_category.json").read_bytes()
    result = preserve_and_parse_synthetic_response(
        raw,
        tmp_path / "controlled" / "raw-response.json",
        response_schema=frozen_model_response_schema(),
    )
    public_json = json.dumps(result.envelope, sort_keys=True)
    assert "invented_unknown_category" not in public_json
    assert "Invented invalid category fixture" not in public_json


def test_dry_run_reports_zero_provider_calls_packets_and_outputs():
    plan = run_dry_run(ROOT)
    assert plan["actual_provider_calls_performed"] == 0
    assert plan["packets_inspected"] == 0
    assert plan["requests_transmitted"] == 0
    assert plan["responses_received"] == 0
    assert plan["outputs_generated"] == 0


def test_dry_run_works_with_network_and_provider_clis_disabled(monkeypatch):
    import trim_haa.llm.frozen_reference as frozen_reference

    original_run = frozen_reference.subprocess.run
    observed = []

    def local_git_only(command, *args, **kwargs):
        observed.append(command)
        assert command[0] == "git"
        assert command[1] == "show"
        return original_run(command, *args, **kwargs)

    def no_network(*args, **kwargs):
        raise AssertionError("network access attempted")

    fake_openai = types.ModuleType("openai")
    fake_openai.OpenAI = no_network
    monkeypatch.setitem(sys.modules, "openai", fake_openai)
    monkeypatch.setattr(frozen_reference.subprocess, "run", local_git_only)
    monkeypatch.setattr(socket, "socket", no_network)
    monkeypatch.setattr(socket, "create_connection", no_network)
    monkeypatch.setattr(urllib.request, "urlopen", no_network)
    monkeypatch.setattr(http.client.HTTPConnection, "connect", no_network)
    assert run_dry_run(ROOT)["overall_execution_status"] == "EXECUTION_BLOCKED"
    assert observed and all(command[0] not in {"curl", "openai"} for command in observed)


def test_no_api_key_or_environment_lookup_is_required(monkeypatch):
    def forbidden_getenv(*args, **kwargs):
        raise AssertionError("environment lookup attempted")

    monkeypatch.setattr(os, "getenv", forbidden_getenv)
    assert build_execution_plan(ROOT)["execution_allowed"] is False


def test_dry_run_command_succeeds_only_because_execution_is_blocked(capsys):
    assert dry_run_human_llm_execution.main() == 0
    output = capsys.readouterr().out
    assert "DRY_RUN_VALID_EXECUTION_BLOCKED" in output
    assert '"execution_allowed":false' in output


def test_selected_case_order_is_unchanged():
    rights = load_json(ROOT / "data" / "studies" / "human_llm_pilot" / "rights_inventory_manifest.json")
    frozen = load_and_verify_public_freeze(ROOT)
    assert [record["case_id"] for record in rights["records"]] == EXPECTED_CASE_IDS
    assert frozen["sample"]["selected_case_ids"] == EXPECTED_CASE_IDS
    assert frozen["allocation"]["case_order"] == frozen["allocation"]["human_record_completion_order"]


def test_prompt_files_and_pr18_artifacts_are_unchanged():
    changed = subprocess.run(
        ["git", "diff", "--name-only", STARTING_PR20_HEAD, "--"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.splitlines()
    assert not {
        path
        for path in changed
        if path in PR18_PROTECTED_EXACT or any(path.startswith(prefix) for prefix in PR18_PROTECTED_PREFIXES)
    }


@pytest.mark.parametrize(
    "path",
    [
        "docs/manuals/friction_locus_manual_manifest.json",
        "docs/manuals/friction_locus_manual_v0_1.json",
        "docs/manuals/friction_locus_manual_v0_1.md",
    ],
)
def test_authoritative_manual_is_unchanged(path):
    assert (ROOT / path).read_bytes() == git_bytes(STARTING_PR20_HEAD, path)


def test_runtime_record_and_execution_plan_hashes_validate():
    runtime = load_json(ROOT / "data" / "studies" / "human_llm_pilot" / "runtime_settings_draft.json")
    plan = load_json(ROOT / "data" / "studies" / "human_llm_pilot" / "execution_plan_dry_run.json")
    assert verify_record_hash(runtime)
    assert verify_record_hash(plan)


def test_synthetic_fixtures_contain_no_selected_source_identifiers():
    text = "\n".join(path.read_text(encoding="utf-8") for path in FIXTURES.iterdir())
    assert not any(case_id in text for case_id in EXPECTED_CASE_IDS)


def test_execution_scaffold_validator_passes():
    assert validate_scaffold() == []
