import hashlib
import http.client
import json
import os
import socket
import sys
import types
import urllib.request
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from scripts import dry_run_human_coding
from scripts.validate_human_coding_scaffold import validate as validate_human_scaffold
from scripts.validate_human_llm_execution_scaffold import UNCHANGED_BOUNDARY_HASHES, protected_boundary_errors
from trim_haa.human_coding.disagreement import compare_annotations
from trim_haa.human_coding.dry_run import build_synthetic_lifecycle, run_human_coding_dry_run
from trim_haa.human_coding.gates import (
    HumanCodingBlockedError,
    assert_human_coding_allowed,
    evaluate_human_coding_gate,
)
from trim_haa.human_coding.lifecycle import (
    create_amendment,
    create_superseded_record,
    edit_draft,
    submit_annotation,
    validate_adjudication_sources,
)
from trim_haa.human_coding.locking import (
    AnnotationStateError,
    LockedAnnotationError,
    frozen_coder_payload_hash,
    verify_frozen_coder_payload_hash,
)
from trim_haa.human_coding.schema_validation import load_schema, schema_errors
from trim_haa.llm.frozen_reference import load_and_verify_public_freeze
from trim_haa.llm.hashing import verify_record_hash


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "studies" / "human_llm_pilot"
FIXTURES = ROOT / "tests" / "fixtures" / "human_coding"
SCHEMAS = ROOT / "schemas"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def all_pass_human_gate_inputs():
    return {
        "rights_gate_status": "PASSED_WITH_DOWNSTREAM_GATES_BLOCKED",
        "private_packet_gate_status": "PASSED_WITH_CONTROLLED_ACCESS_ONLY",
        "packet_hash_verification_status": "VERIFIED",
        "coding_environment_verified": True,
        "coder_eligible": True,
        "coder_training_status": "PASSED_DOCUMENTED",
        "coder_authorization_status": "PASSED",
        "session_authorization_status": "PASSED",
        "packet_access_authorization_reference": "SYNTHETIC_PACKET_ACCESS_AUTHORIZATION_REFERENCE",
        "final_authorization_status": "PASSED",
        "human_coding_gate_status": "PASSED",
        "record_locking_ready": True,
    }


def blocked_decision(**overrides):
    values = all_pass_human_gate_inputs()
    values.update(overrides)
    return evaluate_human_coding_gate(**values)


def test_synthetic_coder_registry_validates():
    record = load_json(DATA / "coder_registry_dry_run.json")
    schema = load_schema(SCHEMAS / "human_llm_coder_registry.schema.json")
    assert schema_errors(record, schema, root=ROOT) == []
    assert verify_record_hash(record)
    assert all(verify_record_hash(coder) for coder in record["coders"])


def test_real_looking_secret_fields_are_rejected():
    record = load_json(DATA / "coder_registry_dry_run.json")
    record["coders"][0]["password"] = "synthetic_invalid_value"
    schema = load_schema(SCHEMAS / "human_llm_coder_registry.schema.json")
    assert schema_errors(record, schema, root=ROOT)


def test_dry_run_enforces_coding_eligibility_false():
    record = load_json(DATA / "coder_registry_dry_run.json")
    assert all(coder["coding_eligibility"] is False for coder in record["coders"])
    assert all(coder["private_packet_access_eligibility"] is False for coder in record["coders"])


def test_coding_session_cannot_start_while_human_gate_blocked():
    decision = blocked_decision(human_coding_gate_status="BLOCKED")
    with pytest.raises(HumanCodingBlockedError, match="human-coding gate blocked"):
        assert_human_coding_allowed(decision)


def test_coding_session_cannot_start_without_final_authorization():
    decision = blocked_decision(final_authorization_status="BLOCKED")
    with pytest.raises(HumanCodingBlockedError, match="final authorization blocked"):
        assert_human_coding_allowed(decision)


def test_coding_session_cannot_start_without_packet_hash_verification():
    decision = blocked_decision(packet_hash_verification_status="NOT_PERFORMED")
    with pytest.raises(HumanCodingBlockedError, match="packet hash verification"):
        assert_human_coding_allowed(decision)


def test_coding_session_cannot_start_without_coder_eligibility():
    decision = blocked_decision(coder_eligible=False)
    with pytest.raises(HumanCodingBlockedError, match="coder eligibility false"):
        assert_human_coding_allowed(decision)


def test_coding_session_cannot_start_without_passed_training():
    decision = blocked_decision(coder_training_status="NOT_STARTED")
    with pytest.raises(HumanCodingBlockedError, match="coder training incomplete"):
        assert_human_coding_allowed(decision)


def test_coding_session_cannot_start_without_authorization_reference():
    decision = blocked_decision(packet_access_authorization_reference=None)
    with pytest.raises(HumanCodingBlockedError, match="session authorization absent"):
        assert_human_coding_allowed(decision)


def test_coding_session_cannot_start_without_environment_verification():
    decision = blocked_decision(coding_environment_verified=False)
    with pytest.raises(HumanCodingBlockedError, match="coding environment unverified"):
        assert_human_coding_allowed(decision)


def test_current_restricted_rights_and_packet_passes_are_preparation_sufficient():
    decision = blocked_decision(human_coding_gate_status="BLOCKED")
    assert decision.preparation_gates_sufficient is True
    assert decision.coding_allowed is False


def test_provider_runtime_and_pricing_are_not_direct_human_gate_inputs():
    inputs = all_pass_human_gate_inputs()
    assert "provider_model_account" not in inputs
    assert "runtime_settings" not in inputs
    assert "pricing" not in inputs


def test_draft_annotation_can_be_edited():
    lifecycle = build_synthetic_lifecycle(ROOT)
    draft = lifecycle["draft_a"]
    edited = edit_draft(draft, {"adjudication_status": "PENDING"})
    assert edited["adjudication_status"] == "PENDING"
    assert edited["record_hash"] != draft["record_hash"]
    assert draft["adjudication_status"] == "BLOCKED"


def test_submitted_annotation_cannot_be_silently_edited():
    draft = build_synthetic_lifecycle(ROOT)["draft_a"]
    submitted = submit_annotation(draft, submitted_timestamp="2026-07-11T01:00:00+10:00")
    with pytest.raises(AnnotationStateError):
        edit_draft(submitted, {"adjudication_status": "PENDING"})


def test_locked_annotation_is_immutable():
    locked = build_synthetic_lifecycle(ROOT)["locked_a"]
    with pytest.raises(LockedAnnotationError):
        edit_draft(locked, {"adjudication_status": "PENDING"})


def test_locked_annotation_correction_requires_amendment():
    lifecycle = build_synthetic_lifecycle(ROOT)
    locked = lifecycle["locked_a"]
    before = deepcopy(locked)
    amendment = lifecycle["amendment"]
    assert locked == before
    assert amendment["annotation_id"] != locked["annotation_id"]
    assert amendment["annotation_lifecycle_status"] == "AMENDED"


def test_amendment_references_prior_record_hash():
    lifecycle = build_synthetic_lifecycle(ROOT)
    assert lifecycle["amendment"]["supersedes_record"] == {
        "annotation_id": lifecycle["locked_a"]["annotation_id"],
        "record_hash": lifecycle["locked_a"]["record_hash"],
    }


def test_invalid_prior_hash_blocks_amendment():
    lifecycle = build_synthetic_lifecycle(ROOT)
    locked = deepcopy(lifecycle["locked_a"])
    locked["record_hash"] = "sha256:" + "0" * 64
    payload = load_json(FIXTURES / "synthetic_coder_payload_a.json")
    with pytest.raises(AnnotationStateError, match="hash is invalid"):
        create_amendment(
            locked,
            amendment_annotation_id="SYNTHETIC_INVALID_AMENDMENT",
            amended_coder_payload=payload,
            created_timestamp="2026-07-11T01:00:00+10:00",
            submitted_timestamp="2026-07-11T01:01:00+10:00",
            locked_timestamp="2026-07-11T01:02:00+10:00",
        )


def test_superseded_record_remains_hash_valid_and_original_preserved():
    lifecycle = build_synthetic_lifecycle(ROOT)
    original = deepcopy(lifecycle["locked_a"])
    superseded = create_superseded_record(lifecycle["locked_a"], lifecycle["amendment"])
    assert verify_record_hash(superseded)
    assert lifecycle["locked_a"] == original
    assert verify_record_hash(lifecycle["locked_a"])


def test_adjudication_references_all_source_annotation_hashes():
    lifecycle = build_synthetic_lifecycle(ROOT)
    validate_adjudication_sources(
        lifecycle["adjudication"],
        [lifecycle["locked_a"], lifecycle["locked_b"]],
    )


def test_checked_synthetic_adjudication_draft_validates():
    record = load_json(FIXTURES / "synthetic_adjudication_draft.json")
    schema = load_schema(SCHEMAS / "human_llm_adjudication_record.schema.json")
    assert schema_errors(record, schema, root=ROOT) == []
    assert verify_record_hash(record)
    assert record["adjudication_status"] == "DRAFT_BLOCKED"
    assert record["adjudicated_payload"] is None


def test_adjudication_missing_source_hash_fails():
    lifecycle = build_synthetic_lifecycle(ROOT)
    adjudication = deepcopy(lifecycle["adjudication"])
    adjudication["source_annotation_record_hashes"] = [lifecycle["locked_a"]["record_hash"]]
    with pytest.raises(AnnotationStateError, match="every source annotation hash"):
        validate_adjudication_sources(adjudication, [lifecycle["locked_a"], lifecycle["locked_b"]])


def test_disagreement_utility_detects_field_level_differences():
    payload_a = load_json(FIXTURES / "synthetic_coder_payload_a.json")
    payload_b = load_json(FIXTURES / "synthetic_coder_payload_b.json")
    result = compare_annotations([payload_a, payload_b])
    assert "primary_label" in result["field_disagreements"]
    assert result["category_set_agreement"] is False
    assert result["confidence_disagreement"] is True
    assert result["adjudication_required"] is True


def test_disagreement_utility_excludes_free_text_comments():
    payload_a = load_json(FIXTURES / "synthetic_coder_payload_a.json")
    payload_b = deepcopy(payload_a)
    payload_b["free_text_rationale"] = "A different invented comment."
    payload_b["unresolved_ambiguity"] = "A different invented ambiguity."
    payload_b["record_hash"] = frozen_coder_payload_hash(payload_b)
    result = compare_annotations([payload_a, payload_b])
    assert result["exact_agreement"] is True
    assert "free_text_rationale" not in result["field_disagreements"]


def test_synthetic_valid_coder_payload_passes_frozen_schema():
    payload = load_json(FIXTURES / "synthetic_coder_payload_a.json")
    coder_schema = load_schema(SCHEMAS / "human_llm_coder_output.schema.json")
    schema = {"$ref": coder_schema["$id"] + "#/$defs/human_coder_record"}
    assert schema_errors(payload, schema, root=ROOT) == []
    assert verify_frozen_coder_payload_hash(payload)


def test_synthetic_invalid_coder_payload_fails_frozen_schema():
    payload = load_json(FIXTURES / "synthetic_coder_payload_invalid.json")
    coder_schema = load_schema(SCHEMAS / "human_llm_coder_output.schema.json")
    schema = {"$ref": coder_schema["$id"] + "#/$defs/human_coder_record"}
    assert schema_errors(payload, schema, root=ROOT)


def test_annotation_wrapper_schema_validates_all_synthetic_lifecycle_records():
    schema = load_schema(SCHEMAS / "human_llm_human_annotation_record.schema.json")
    lifecycle = build_synthetic_lifecycle(ROOT)
    for key in ("draft_a", "draft_b", "locked_a", "locked_b", "amendment", "superseded"):
        assert schema_errors(lifecycle[key], schema, root=ROOT) == []


def test_environment_and_session_records_remain_blocked():
    environment = load_json(DATA / "coding_environment_dry_run.json")
    session = load_json(DATA / "coding_session_authorization_dry_run.json")
    assert environment["environment_verified"] is False
    assert environment["coding_allowed"] is False
    assert environment["selected_packet_mounted"] is False
    assert session["coding_allowed"] is False
    assert session["packet_hash_verification_status"] == "NOT_PERFORMED"


def test_human_coding_dry_run_reports_all_zero_activity_counts():
    plan = run_human_coding_dry_run(ROOT)
    assert plan["actual_packets_inspected"] == 0
    assert plan["actual_coding_sessions_started"] == 0
    assert plan["actual_annotations_created"] == 0
    assert plan["actual_annotations_locked"] == 0
    assert plan["actual_adjudications_completed"] == 0


def test_human_coding_dry_run_succeeds_only_because_coding_is_blocked(capsys):
    assert dry_run_human_coding.main() == 0
    output = capsys.readouterr().out
    assert "DRY_RUN_VALID_HUMAN_CODING_BLOCKED" in output
    assert '"coding_allowed":false' in output


def test_human_coding_dry_run_requires_no_network_or_provider_client(monkeypatch):
    def no_network(*args, **kwargs):
        raise AssertionError("network/provider access attempted")

    def no_subprocess(*args, **kwargs):
        raise AssertionError("subprocess access attempted")

    fake_openai = types.ModuleType("openai")
    fake_openai.OpenAI = no_network
    monkeypatch.setitem(sys.modules, "openai", fake_openai)
    monkeypatch.setattr("subprocess.run", no_subprocess)
    monkeypatch.setattr(socket, "socket", no_network)
    monkeypatch.setattr(socket, "create_connection", no_network)
    monkeypatch.setattr(urllib.request, "urlopen", no_network)
    monkeypatch.setattr(http.client.HTTPConnection, "connect", no_network)
    assert run_human_coding_dry_run(ROOT)["overall_status"] == "HUMAN_CODING_BLOCKED"


def test_human_coding_dry_run_requires_no_api_key(monkeypatch):
    def forbidden_getenv(*args, **kwargs):
        raise AssertionError("environment lookup attempted")

    monkeypatch.setattr(os, "getenv", forbidden_getenv)
    assert run_human_coding_dry_run(ROOT)["coding_allowed"] is False


def test_no_real_coder_identity_is_required():
    registry = load_json(DATA / "coder_registry_dry_run.json")
    assert {coder["coder_id"] for coder in registry["coders"]} == {
        "SYNTHETIC_CODER_A",
        "SYNTHETIC_CODER_B",
        "SYNTHETIC_ADJUDICATOR",
    }
    assert registry["no_real_coder_registered"] is True


def test_no_selected_source_text_or_case_ids_appear_in_human_fixtures():
    text = "\n".join(path.read_text(encoding="utf-8") for path in FIXTURES.iterdir())
    assert "L1_" not in text
    assert "L2_" not in text
    for name in ("Austen", "Dickens", "Homer", "Ovid", "Sophocles", "Beowulf"):
        assert name not in text


def test_selected_case_order_is_unchanged():
    rights = load_json(DATA / "rights_inventory_manifest.json")
    frozen = load_and_verify_public_freeze(ROOT)
    assert [record["case_id"] for record in rights["records"]] == frozen["sample"]["selected_case_ids"]


def test_pr18_artifacts_and_frozen_prompts_are_unchanged():
    assert protected_boundary_errors() == []


@pytest.mark.parametrize(
    "path",
    [
        "docs/manuals/friction_locus_manual_manifest.json",
        "docs/manuals/friction_locus_manual_v0_1.json",
        "docs/manuals/friction_locus_manual_v0_1.md",
    ],
)
def test_authoritative_manual_is_unchanged(path):
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == UNCHANGED_BOUNDARY_HASHES[path]


def test_no_force_unlock_environment_bypass_or_deletion_workflow_exists():
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "src" / "trim_haa" / "human_coding").glob("*.py")
    )
    assert "force_unlock" not in text
    assert "os.getenv" not in text
    assert "delete_annotation" not in text


def test_human_coding_scaffold_validator_passes():
    assert validate_human_scaffold() == []
