"""Deterministic metadata-only dry-run for the blocked human--LLM pilot."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .frozen_reference import load_and_verify_public_freeze
from .gates import PRIVATE_PACKET_PREPARATION_STATUSES, RIGHTS_PREPARATION_STATUSES, load_gate_decision
from .hashing import compute_record_hash, verify_record_hash


EXPECTED_PROVIDER_ACCOUNT_STATUS = "BLOCKED_NO_API_KEY_AVAILABLE_FOR_ACCOUNT_MODEL_LISTING"
PLAN_TIMESTAMP = "2026-07-10T00:00:00+10:00"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON record must be an object: {path}")
    return value


def _validate_rights_records(root: Path, rights_manifest: dict[str, Any]) -> None:
    records = rights_manifest.get("records", [])
    if rights_manifest.get("selected_case_count") != 25 or len(records) != 25:
        raise ValueError("rights inventory must contain exactly 25 selected cases")
    case_ids: list[str] = []
    for record in records:
        case_id = record.get("case_id")
        evidence_path = record.get("rights_evidence_path")
        if not isinstance(case_id, str) or not isinstance(evidence_path, str):
            raise ValueError("rights inventory record lacks public metadata reference")
        evidence = _load_json(root / evidence_path)
        if evidence.get("case_id") != case_id:
            raise ValueError(f"rights evidence case mismatch: {case_id}")
        if not str(evidence.get("status", "")).startswith("RIGHTS_DOCUMENTED"):
            raise ValueError(f"rights evidence remains blocked: {case_id}")
        if not verify_record_hash(evidence):
            raise ValueError(f"rights evidence hash mismatch: {case_id}")
        case_ids.append(case_id)
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("rights inventory contains duplicate selected case IDs")


def build_execution_plan(root: str | Path) -> dict[str, Any]:
    """Build the deterministic plan while confirming that execution remains blocked."""

    root_path = Path(root)
    data_dir = root_path / "data" / "studies" / "human_llm_pilot"
    gates = load_gate_decision(data_dir / "gate_status_manifest.json")
    rights = _load_json(data_dir / "rights_inventory_manifest.json")
    packet_approval = _load_json(data_dir / "private_packet_handling_approval.json")
    provider_record = _load_json(data_dir / "provider_model_account_verification.json")
    runtime = _load_json(data_dir / "runtime_settings_draft.json")
    frozen = load_and_verify_public_freeze(root_path)

    _validate_rights_records(root_path, rights)
    if gates.statuses.get("rights_evidence") not in RIGHTS_PREPARATION_STATUSES:
        raise ValueError("rights evidence gate is not sufficient for preparation")
    if packet_approval.get("approval_status") not in PRIVATE_PACKET_PREPARATION_STATUSES:
        raise ValueError("private-packet handling approval is not sufficient for preparation")
    if packet_approval.get("private_packet_text_inspected") is not False:
        raise ValueError("private-packet approval reports packet inspection")
    if packet_approval.get("execution_authorization") != "not_authorized":
        raise ValueError("private-packet approval improperly authorizes execution")
    if gates.statuses.get("provider_model_account") != "BLOCKED":
        raise ValueError("provider/model/account gate must remain blocked")
    if provider_record.get("account_availability_status") != EXPECTED_PROVIDER_ACCOUNT_STATUS:
        raise ValueError("provider account availability status changed")
    for gate in ("runtime_settings", "pricing", "final_authorization", "human_coding", "model_execution"):
        if gates.statuses.get(gate) != "BLOCKED":
            raise ValueError(f"required blocked gate changed: {gate}")
    if runtime.get("record_status") != "DRAFT_BLOCKED_PENDING_ACCOUNT_AND_RUNTIME_VERIFICATION":
        raise ValueError("runtime settings record is not the blocked draft")
    if runtime.get("execution_allowed") is not False or not verify_record_hash(runtime):
        raise ValueError("runtime settings draft is executable or has an invalid hash")
    if gates.execution_allowed or gates.decision != "EXECUTION_BLOCKED":
        raise ValueError("normalized gate decision failed to block execution")

    allocation = frozen["allocation"]
    sample = frozen["sample"]
    freeze = frozen["freeze_package"]
    if set(sample["selected_case_ids"]) != {record["case_id"] for record in rights["records"]}:
        raise ValueError("PR #18 selected cases differ from rights inventory")
    planned_run_count = allocation["planned_model_run_counts"]["total_planned_model_runs_after_human_lock"]
    ablation_assignments = allocation["condition_assignment"]["ablation_subset_conditions"]
    condition_names = {name for names in ablation_assignments.values() for name in names}

    plan: dict[str, Any] = {
        "schema_version": "1.0.0",
        "plan_status": "DRY_RUN_VALID_EXECUTION_BLOCKED",
        "created_at": PLAN_TIMESTAMP,
        "pr18_reference_head_sha": "eac65f27bbe302a17e5f508ac1d516178e917aea",
        "selected_case_count": sample["sample_size"],
        "condition_count": len(condition_names),
        "planned_run_count": planned_run_count,
        "ordering_rule": "frozen PR #18 allocation_manifest.case_order with its primary, stability, and ablation run roles",
        "allocation_manifest_hash": f"sha256:{allocation['allocation_hash']}",
        "prompt_assembly_manifest_hash": f"sha256:{freeze['prompt_assembly_manifest_hash']}",
        "manual_manifest_hash": f"sha256:{freeze['manual_manifest_hash']}",
        "model_response_schema_hash": f"sha256:{freeze['model_response_schema_hash']}",
        "rights_gate_status": gates.statuses["rights_evidence"],
        "private_packet_gate_status": gates.statuses["controlled_private_packet_handling"],
        "provider_model_account_gate_status": gates.statuses["provider_model_account"],
        "runtime_gate_status": gates.statuses["runtime_settings"],
        "pricing_gate_status": gates.statuses["pricing"],
        "final_authorization_status": gates.statuses["final_authorization"],
        "human_coding_status": gates.statuses["human_coding"],
        "model_execution_status": gates.statuses["model_execution"],
        "provider_calls_planned_but_not_authorized": planned_run_count,
        "actual_provider_calls_performed": 0,
        "packets_inspected": 0,
        "requests_transmitted": 0,
        "responses_received": 0,
        "outputs_generated": 0,
        "blockers": list(gates.blockers),
        "explicit_execution_blocked_reason": "Provider/account, runtime settings, pricing, final authorization, human coding, and model execution gates are BLOCKED.",
        "execution_allowed": False,
        "overall_execution_status": "EXECUTION_BLOCKED",
        "record_hash": "",
    }
    plan["record_hash"] = compute_record_hash(plan)
    return plan


def run_dry_run(root: str | Path) -> dict[str, Any]:
    """Validate the checked-in deterministic plan; construct no provider request."""

    root_path = Path(root)
    planned = build_execution_plan(root_path)
    checked_in = _load_json(root_path / "data" / "studies" / "human_llm_pilot" / "execution_plan_dry_run.json")
    if checked_in != planned:
        raise ValueError("checked-in execution plan does not match deterministic dry-run construction")
    if checked_in["overall_execution_status"] != "EXECUTION_BLOCKED" or checked_in["execution_allowed"]:
        raise ValueError("dry-run plan does not fail closed")
    return checked_in
