"""Deterministic synthetic-only human-coding dry-run."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from trim_haa.llm.frozen_reference import load_and_verify_public_freeze
from trim_haa.llm.hashing import compute_record_hash, verify_record_hash

from .disagreement import compare_annotations
from .gates import evaluate_human_coding_gate
from .lifecycle import (
    create_amendment,
    create_superseded_record,
    lock_annotation,
    submit_annotation,
    validate_adjudication_sources,
)
from .locking import LockedAnnotationError, finalize_record, frozen_coder_payload_hash, verify_frozen_coder_payload_hash
from .schema_validation import load_schema, schema_errors


PLAN_TIMESTAMP = "2026-07-11T00:00:00+10:00"
MANUAL_VERSION = "friction_locus_manual_v0_1"
MANUAL_HASH = "sha256:797d79fcdb29fc32850c3778c6afb029ac0768207ea33f66d714fe8fa8cb591a"
CODER_SCHEMA_HASH = "sha256:2abdf5f5690aada67f1694f8d83dfe95236fbcba46c1bbcfca169567dbda7b12"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON record must be an object: {path}")
    return value


def _validate_record_hash(record: dict[str, Any], label: str) -> None:
    if not verify_record_hash(record):
        raise ValueError(f"{label} canonical record hash mismatch")


def _base_annotation(payload: dict[str, Any], *, annotation_id: str, coder_id: str) -> dict[str, Any]:
    record = {
        "annotation_record_version": "1.0.0",
        "annotation_id": annotation_id,
        "synthetic_only": True,
        "coder_id": coder_id,
        "case_id": "SYNTHETIC_CASE_ALPHA",
        "session_id": "SYNTHETIC_SESSION_NOT_STARTED",
        "packet_hash": "sha256:" + ("a" if coder_id == "SYNTHETIC_CODER_A" else "b") * 64,
        "manual_version": MANUAL_VERSION,
        "manual_hash": MANUAL_HASH,
        "coder_schema_hash": CODER_SCHEMA_HASH,
        "coding_condition": "synthetic_dry_run",
        "blinded_assignment_reference": "SYNTHETIC_ASSIGNMENT_ALPHA",
        "annotation_lifecycle_status": "DRAFT",
        "coder_payload": deepcopy(payload),
        "created_timestamp": PLAN_TIMESTAMP,
        "submitted_timestamp": None,
        "locked_timestamp": None,
        "amendment_count": 0,
        "supersedes_record": None,
        "superseded_by_record": None,
        "adjudication_status": "BLOCKED",
        "private_packet_access_log_reference": "synthetic_not_authorized",
        "record_hash": "",
    }
    return finalize_record(record)


def build_synthetic_lifecycle(root: str | Path) -> dict[str, Any]:
    """Construct in-memory synthetic records and prove fail-closed lifecycle rules."""

    root_path = Path(root)
    fixture_dir = root_path / "tests" / "fixtures" / "human_coding"
    payload_a = _load_json(fixture_dir / "synthetic_coder_payload_a.json")
    payload_b = _load_json(fixture_dir / "synthetic_coder_payload_b.json")
    invalid_payload = _load_json(fixture_dir / "synthetic_coder_payload_invalid.json")
    if not verify_frozen_coder_payload_hash(payload_a) or not verify_frozen_coder_payload_hash(payload_b):
        raise ValueError("synthetic coder payload hash mismatch")

    coder_schema = load_schema(root_path / "schemas" / "human_llm_coder_output.schema.json")
    human_payload_schema = {"$ref": coder_schema["$id"] + "#/$defs/human_coder_record"}
    if schema_errors(payload_a, human_payload_schema, root=root_path):
        raise ValueError("synthetic coder payload A fails frozen schema")
    if schema_errors(payload_b, human_payload_schema, root=root_path):
        raise ValueError("synthetic coder payload B fails frozen schema")
    if not schema_errors(invalid_payload, human_payload_schema, root=root_path):
        raise ValueError("invalid synthetic coder payload unexpectedly passes frozen schema")

    annotation_schema = load_schema(root_path / "schemas" / "human_llm_human_annotation_record.schema.json")
    adjudication_schema = load_schema(root_path / "schemas" / "human_llm_adjudication_record.schema.json")
    draft_a = _base_annotation(payload_a, annotation_id="SYNTHETIC_ANNOTATION_A", coder_id="SYNTHETIC_CODER_A")
    draft_b = _base_annotation(payload_b, annotation_id="SYNTHETIC_ANNOTATION_B", coder_id="SYNTHETIC_CODER_B")
    if schema_errors(draft_a, annotation_schema, root=root_path) or schema_errors(draft_b, annotation_schema, root=root_path):
        raise ValueError("synthetic draft annotation fails wrapper schema")

    submitted_a = submit_annotation(draft_a, submitted_timestamp="2026-07-11T00:01:00+10:00")
    submitted_b = submit_annotation(draft_b, submitted_timestamp="2026-07-11T00:01:30+10:00")
    locked_a = lock_annotation(submitted_a, locked_timestamp="2026-07-11T00:02:00+10:00")
    locked_b = lock_annotation(submitted_b, locked_timestamp="2026-07-11T00:02:30+10:00")
    try:
        lock_annotation(locked_a, locked_timestamp="2026-07-11T00:03:00+10:00")
    except LockedAnnotationError:
        pass
    else:
        raise ValueError("locked annotation accepted a second lock/overwrite transition")

    amended_payload = deepcopy(payload_b)
    amended_payload.update(
        {
            "analyst_id_pseudonym": "SYNTHETIC_CODER_A",
            "record_id": "SYNTHETIC_PAYLOAD_A_AMENDMENT_001",
            "source_packet_hash": "a" * 64,
            "record_hash": "",
        }
    )
    amended_payload["record_hash"] = frozen_coder_payload_hash(amended_payload)
    amendment = create_amendment(
        locked_a,
        amendment_annotation_id="SYNTHETIC_ANNOTATION_A_AMENDMENT_001",
        amended_coder_payload=amended_payload,
        created_timestamp="2026-07-11T00:03:00+10:00",
        submitted_timestamp="2026-07-11T00:03:30+10:00",
        locked_timestamp="2026-07-11T00:04:00+10:00",
    )
    superseded = create_superseded_record(locked_a, amendment)
    for label, record in {
        "locked_a": locked_a,
        "locked_b": locked_b,
        "amendment": amendment,
        "superseded": superseded,
    }.items():
        _validate_record_hash(record, label)
        if schema_errors(record, annotation_schema, root=root_path):
            raise ValueError(f"{label} fails annotation wrapper schema")

    disagreement = compare_annotations([payload_a, payload_b])
    adjudication = {
        "schema_version": "1.0.0",
        "adjudication_id": "SYNTHETIC_ADJUDICATION_DRAFT_001",
        "synthetic_only": True,
        "adjudicator_id": "SYNTHETIC_ADJUDICATOR",
        "case_id": "SYNTHETIC_CASE_ALPHA",
        "source_annotation_record_hashes": [locked_a["record_hash"], locked_b["record_hash"]],
        "disagreement_summary_hash": disagreement["disagreement_summary_hash"],
        "manual_version": MANUAL_VERSION,
        "manual_hash": MANUAL_HASH,
        "adjudication_status": "DRAFT_BLOCKED",
        "adjudicated_payload": None,
        "rationale_metadata": {
            "rationale_code": "SYNTHETIC_DISAGREEMENT_REVIEW_NOT_AUTHORIZED",
            "manual_section_reference": "synthetic_reference_only",
        },
        "created_timestamp": "2026-07-11T00:05:00+10:00",
        "locked_timestamp": None,
        "supersedes_adjudication_record": None,
        "coding_allowed": False,
        "record_hash": "",
    }
    adjudication = finalize_record(adjudication)
    validate_adjudication_sources(adjudication, [locked_a, locked_b])
    if schema_errors(adjudication, adjudication_schema, root=root_path):
        raise ValueError("synthetic adjudication draft fails schema")
    checked_adjudication = _load_json(fixture_dir / "synthetic_adjudication_draft.json")
    if checked_adjudication != adjudication:
        raise ValueError("checked synthetic adjudication fixture is not deterministic")
    return {
        "draft_a": draft_a,
        "draft_b": draft_b,
        "locked_a": locked_a,
        "locked_b": locked_b,
        "amendment": amendment,
        "superseded": superseded,
        "disagreement": disagreement,
        "adjudication": adjudication,
    }


def build_human_coding_plan(root: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    data_dir = root_path / "data" / "studies" / "human_llm_pilot"
    gates = _load_json(data_dir / "gate_status_manifest.json")
    gate_statuses = {entry["gate"]: entry["status"] for entry in gates["gates"]}
    registry = _load_json(data_dir / "coder_registry_dry_run.json")
    environment = _load_json(data_dir / "coding_environment_dry_run.json")
    session = _load_json(data_dir / "coding_session_authorization_dry_run.json")
    assignment = _load_json(data_dir / "blinded_assignment_dry_run.json")
    frozen = load_and_verify_public_freeze(root_path)

    for label, record in {
        "coder registry": registry,
        "coding environment": environment,
        "session authorization": session,
        "blinded assignment": assignment,
    }.items():
        _validate_record_hash(record, label)
    for coder in registry["coders"]:
        _validate_record_hash(coder, coder["coder_id"])
    if session["coding_environment_record_hash"] != environment["record_hash"]:
        raise ValueError("session authorization does not reference coding environment hash")
    if any(coder["coding_eligibility"] or coder["private_packet_access_eligibility"] for coder in registry["coders"]):
        raise ValueError("synthetic coder registry improperly allows coding or packet access")
    if environment["environment_verified"] or environment["coding_allowed"]:
        raise ValueError("coding environment is improperly verified or allowed")
    if session["coding_allowed"] or assignment["coding_allowed"]:
        raise ValueError("synthetic session or assignment improperly allows coding")

    decision = evaluate_human_coding_gate(
        rights_gate_status=gate_statuses["rights_evidence"],
        private_packet_gate_status=gate_statuses["controlled_private_packet_handling"],
        packet_hash_verification_status=session["packet_hash_verification_status"],
        coding_environment_verified=environment["environment_verified"],
        coder_eligible=registry["coders"][0]["coding_eligibility"],
        coder_training_status=registry["coders"][0]["training_status"],
        coder_authorization_status=registry["coders"][0]["authorization_status"],
        session_authorization_status=session["authorization_status"],
        packet_access_authorization_reference=session["packet_access_authorization_reference"],
        final_authorization_status=gate_statuses["final_authorization"],
        human_coding_gate_status=gate_statuses["human_coding"],
        record_locking_ready=False,
    )
    if decision.coding_allowed or decision.decision != "HUMAN_CODING_BLOCKED":
        raise ValueError("human-coding decision failed to block coding")
    build_synthetic_lifecycle(root_path)

    allocation = frozen["allocation"]
    sample = frozen["sample"]
    manual = frozen["manual_freeze"]
    plan: dict[str, Any] = {
        "schema_version": "1.0.0",
        "plan_status": "DRY_RUN_VALID_HUMAN_CODING_BLOCKED",
        "created_at": PLAN_TIMESTAMP,
        "selected_case_count": sample["sample_size"],
        "planned_coder_count": "pending_protocol_freeze",
        "planned_annotation_count": "pending_protocol_freeze",
        "planned_double_coded_count": "pending_protocol_freeze",
        "planned_adjudication_count": "pending_protocol_freeze",
        "manual_manifest_hash": f"sha256:{manual['manual_manifest_hash']}",
        "coder_schema_hash": CODER_SCHEMA_HASH,
        "allocation_manifest_hash": f"sha256:{allocation['allocation_hash']}",
        "rights_gate_status": gate_statuses["rights_evidence"],
        "private_packet_gate_status": gate_statuses["controlled_private_packet_handling"],
        "coding_environment_status": environment["environment_status"],
        "coder_registry_status": registry["registry_status"],
        "packet_hash_verification_status": session["packet_hash_verification_status"],
        "final_authorization_status": gate_statuses["final_authorization"],
        "human_coding_status": gate_statuses["human_coding"],
        "actual_packets_inspected": 0,
        "actual_coding_sessions_started": 0,
        "actual_annotations_created": 0,
        "actual_annotations_locked": 0,
        "actual_adjudications_completed": 0,
        "blockers": list(decision.blockers),
        "explicit_blocked_reason": "Coding environment, coder eligibility/training/authorization, session authorization, packet verification, final authorization, human-coding gate, and locking readiness remain blocked.",
        "coding_allowed": False,
        "overall_status": "HUMAN_CODING_BLOCKED",
        "record_hash": "",
    }
    plan["record_hash"] = compute_record_hash(plan)
    return plan


def run_human_coding_dry_run(root: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    planned = build_human_coding_plan(root_path)
    checked_in = _load_json(root_path / "data" / "studies" / "human_llm_pilot" / "human_coding_plan_dry_run.json")
    if checked_in != planned:
        raise ValueError("checked-in human-coding plan does not match deterministic dry-run")
    if checked_in["coding_allowed"] or checked_in["overall_status"] != "HUMAN_CODING_BLOCKED":
        raise ValueError("human-coding dry-run does not fail closed")
    return checked_in
