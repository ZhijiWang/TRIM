"""Validate the no-call human--LLM execution scaffold and frozen boundaries."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tomllib
from copy import deepcopy
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trim_haa.llm.dry_run import build_execution_plan, run_dry_run  # noqa: E402
from trim_haa.llm.frozen_reference import load_and_verify_public_freeze  # noqa: E402
from trim_haa.llm.hashing import compute_record_hash, verify_record_hash  # noqa: E402
from trim_haa.llm.openai_adapter import BlockedOpenAIAdapter  # noqa: E402
from trim_haa.llm.request_preservation import (  # noqa: E402
    build_synthetic_request_representation,
    create_request_envelope,
    serialize_synthetic_request,
)


PR18_HEAD = "eac65f27bbe302a17e5f508ac1d516178e917aea"
EXPECTED_PACKAGE_VERSION = "0.3.0a1"
EXPECTED_RIGHTS_RECORDS_HASH = "55181054871c4d10be0f56bcfcfbd57b01c5b813c77d6f15cbfb1ff707cfb179"
EXPECTED_CASE_IDS = [
    "L1_AUSTEN_PNP_001",
    "L1_SHELLEY_FRANK_001",
    "L1_DICKENS_GE_001",
    "L1_BRONTE_JE_001",
    "L1_WILDE_DG_001",
    "L1_JAMES_TS_001",
    "L1_STEVENSON_JH_001",
    "L1_POE_TELLTALE_001",
    "L1_HAWTHORNE_SL_001",
    "L1_CHOPIN_AWAKENING_001",
    "L1_HARDY_TESS_001",
    "L1_MELVILLE_BARTLEBY_001",
    "L1_WHARTON_MIRTH_001",
    "L1_COLLINS_MOONSTONE_001",
    "L1_CONRAD_SECRET_001",
    "L2_HOMER_ODYSSEY_001",
    "L2_SOPHOCLES_ANTIGONE_001",
    "L2_HERODOTUS_SCYTHIAN_001",
    "L2_BIBLE_GENESIS_001",
    "L2_BIBLE_SAMUEL_001",
    "L2_AESOP_001",
    "L2_OVID_DAPHNE_001",
    "L2_MALORY_MORTE_001",
    "L2_BEOWULF_DRAGON_001",
    "L2_ARABIAN_NIGHTS_001",
]
PR18_PROTECTED_EXACT = {
    "data/studies/human_llm_pilot/allocation_manifest.json",
    "data/studies/human_llm_pilot/authoritative_manual_reference.json",
    "data/studies/human_llm_pilot/candidate_count_reconciliation.json",
    "data/studies/human_llm_pilot/cost_ceiling.json",
    "data/studies/human_llm_pilot/freeze_package_manifest.json",
    "data/studies/human_llm_pilot/freeze_status.json",
    "data/studies/human_llm_pilot/governance_status.json",
    "data/studies/human_llm_pilot/manual_freeze_manifest.json",
    "data/studies/human_llm_pilot/model_execution_spec.json",
    "data/studies/human_llm_pilot/prompt_assembly_manifest.json",
    "data/studies/human_llm_pilot/prompt_bundle_manifest.json",
    "data/studies/human_llm_pilot/prompt_condition_difference_audit.json",
    "data/studies/human_llm_pilot/researcher_familiarity_audit.csv",
    "data/studies/human_llm_pilot/sample_manifest.json",
    "data/studies/human_llm_pilot/source_manifest.csv",
    "data/studies/human_llm_pilot/source_packet_substantive_audit.csv",
    "data/studies/human_llm_pilot/source_rights_manifest.csv",
    "docs/studies/human_coder_access_and_record_spec.md",
    "docs/studies/human_llm_manual_gap_report.md",
    "docs/studies/human_llm_pilot_freeze_report.md",
    "docs/studies/human_llm_prompt_assembly_spec.md",
    "docs/studies/human_llm_prompt_condition_audit.md",
    "docs/studies/human_llm_rights_redaction_note.md",
    "docs/studies/human_llm_runtime_and_retry_spec.md",
    "docs/studies/model_record_enrichment_contract.md",
    "docs/studies/pr18_condition_manipulation_audit.md",
    "docs/studies/pr18_manual_dependency_audit.md",
    "docs/studies/pr18_prompt_contamination_audit.md",
    "docs/studies/pr18_prompt_parity_audit.md",
    "schemas/human_llm_model_response.schema.json",
    "scripts/validate_human_llm_pilot_freeze.py",
    "templates/human_llm_run_manifest.json",
    "templates/model_response_payload.json",
    "tests/test_human_llm_pilot_freeze.py",
}
PR18_PROTECTED_PREFIXES = (
    "data/studies/human_llm_pilot/source_packets/",
    "prompts/human_llm_pilot/",
)
VENDORED_PUBLIC_PR18_PATHS = {
    "data/studies/human_llm_pilot/allocation_manifest.json",
    "data/studies/human_llm_pilot/freeze_package_manifest.json",
    "data/studies/human_llm_pilot/manual_freeze_manifest.json",
    "data/studies/human_llm_pilot/prompt_assembly_manifest.json",
    "data/studies/human_llm_pilot/sample_manifest.json",
    "schemas/human_llm_model_response.schema.json",
}
PR18_BASELINE_PATH_HASHES = {
    "templates/human_llm_run_manifest.json": "b8babe6aaa556673de947e67d8eddcbc4f7d54ead65cc923f8a69e818ee9f740",
}
UNCHANGED_BOUNDARY_HASHES = {
    "docs/manuals/friction_locus_manual_manifest.json": "1b80c0931a0ed8159aaeeb6e7b348331beb33130776469f223ae2a8cfe89d8de",
    "docs/manuals/friction_locus_manual_v0_1.json": "797d79fcdb29fc32850c3778c6afb029ac0768207ea33f66d714fe8fa8cb591a",
    "docs/manuals/friction_locus_manual_v0_1.md": "f26f5de05819c4fd36c0d88e7d86320d7374c27185c36575b18b584fc5d9b426",
    "docs/core_schema.md": "e2ee7e73bfc4239a69b3d3534af508525775a3840aa228cbcbe24389fcb0d6e4",
    "docs/provenance.md": "66fbd4c679650797e8d4194c52527075c77b90734963389ce9226c9271774e74",
    "src/trim_haa/schema.py": "bf0540c2c34e02e93f19f2559d5794f6fc59579a363e29a7858e478bb88a4264",
    "src/trim_haa/provenance.py": "92e075aa74afd0661fb6446c1253863883b651df735aaec0ec073638af0fdd14",
    "data/trim_haa_core_template.csv": "fb4392ed27fb943d5b05d35f889985806c54f1f2323965465756b64e9edca3a2",
    "data/trim_haa_assistance_provenance_template.csv": "150124b1c928122fe7d06c6de128952c7e1731b9d53a307966da4b295fc30c62",
}
SECRET_VALUE_RE = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|Bearer\s+[A-Za-z0-9._-]{20,})")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _schema_errors(instance: Any, schema: dict[str, Any]) -> list[str]:
    return [error.message for error in Draft202012Validator(schema).iter_errors(instance)]


def _sha256(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def protected_boundary_errors(root: Path = ROOT) -> list[str]:
    """Validate frozen boundaries without depending on Git history."""

    errors: list[str] = []
    for path in VENDORED_PUBLIC_PR18_PATHS:
        if not (root / path).is_file():
            errors.append(f"missing vendored public PR #18 artifact: {path}")
    for path in PR18_PROTECTED_EXACT - VENDORED_PUBLIC_PR18_PATHS:
        candidate = root / path
        expected = PR18_BASELINE_PATH_HASHES.get(path)
        if expected is not None:
            if _sha256(candidate) != expected:
                errors.append(f"protected PR #18 baseline path changed: {path}")
        elif candidate.exists():
            errors.append(f"unexpected non-vendored PR #18 artifact present: {path}")
    for prefix in PR18_PROTECTED_PREFIXES:
        directory = root / prefix
        if directory.exists() and any(path.is_file() for path in directory.rglob("*")):
            errors.append(f"controlled or prompt PR #18 prefix present: {prefix}")
    for path, expected in UNCHANGED_BOUNDARY_HASHES.items():
        if _sha256(root / path) != expected:
            errors.append(f"protected manual/Core/provenance path changed: {path}")
    return errors


def _response_schema_has_no_content_property(schema: dict[str, Any]) -> bool:
    forbidden = {"content", "raw_response", "response_content", "parsed_payload", "raw_output"}

    def walk(value: Any) -> bool:
        if isinstance(value, dict):
            properties = value.get("properties")
            if isinstance(properties, dict) and forbidden.intersection(properties):
                return False
            return all(walk(item) for item in value.values())
        if isinstance(value, list):
            return all(walk(item) for item in value)
        return True

    return walk(schema)


def validate() -> list[str]:
    errors: list[str] = []
    data_dir = ROOT / "data" / "studies" / "human_llm_pilot"
    schema_dir = ROOT / "schemas"
    required_paths = [
        data_dir / "runtime_settings_draft.json",
        data_dir / "execution_plan_dry_run.json",
        schema_dir / "human_llm_runtime_settings.schema.json",
        schema_dir / "human_llm_provider_request_envelope.schema.json",
        schema_dir / "human_llm_provider_response_envelope.schema.json",
        schema_dir / "human_llm_execution_plan.schema.json",
        ROOT / "scripts" / "dry_run_human_llm_execution.py",
        ROOT / "src" / "trim_haa" / "llm" / "openai_adapter.py",
    ]
    for path in required_paths:
        _require(path.exists(), f"missing execution scaffold path: {path}", errors)
    if errors:
        return errors

    runtime = _load_json(data_dir / "runtime_settings_draft.json")
    plan = _load_json(data_dir / "execution_plan_dry_run.json")
    gate_manifest = _load_json(data_dir / "gate_status_manifest.json")
    rights_manifest = _load_json(data_dir / "rights_inventory_manifest.json")
    runtime_schema = _load_json(schema_dir / "human_llm_runtime_settings.schema.json")
    plan_schema = _load_json(schema_dir / "human_llm_execution_plan.schema.json")
    request_schema = _load_json(schema_dir / "human_llm_provider_request_envelope.schema.json")
    response_schema = _load_json(schema_dir / "human_llm_provider_response_envelope.schema.json")

    _require(not _schema_errors(runtime, runtime_schema), "runtime settings draft fails its schema", errors)
    _require(verify_record_hash(runtime), "runtime settings draft hash mismatch", errors)
    _require(runtime.get("record_status") == "DRAFT_BLOCKED_PENDING_ACCOUNT_AND_RUNTIME_VERIFICATION", "runtime settings must remain draft and blocked", errors)
    _require(runtime.get("runtime_verification_status") == "BLOCKED", "runtime verification must remain blocked", errors)
    _require(runtime.get("execution_allowed") is False, "runtime settings must prohibit execution", errors)
    _require(runtime.get("pricing_status") == "BLOCKED_UNRESOLVED", "pricing must remain unresolved", errors)

    gate_status = {entry["gate"]: entry["status"] for entry in gate_manifest["gates"]}
    for gate in ("provider_model_account", "runtime_settings", "pricing", "final_authorization", "human_coding", "model_execution"):
        _require(gate_status.get(gate) == "BLOCKED", f"{gate} must remain BLOCKED", errors)
    _require(gate_status.get("rights_evidence") == "PASSED_WITH_DOWNSTREAM_GATES_BLOCKED", "rights gate status mismatch", errors)
    _require(gate_status.get("controlled_private_packet_handling") == "PASSED_WITH_CONTROLLED_ACCESS_ONLY", "private-packet gate status mismatch", errors)

    _require(not _schema_errors(plan, plan_schema), "execution plan fails its schema", errors)
    _require(verify_record_hash(plan), "execution plan hash mismatch", errors)
    for field in ("actual_provider_calls_performed", "packets_inspected", "requests_transmitted", "responses_received", "outputs_generated"):
        _require(plan.get(field) == 0, f"execution plan requires {field}=0", errors)
    _require(plan.get("execution_allowed") is False and plan.get("overall_execution_status") == "EXECUTION_BLOCKED", "execution plan must remain blocked", errors)

    try:
        _require(build_execution_plan(ROOT) == plan, "deterministic execution plan mismatch", errors)
        _require(run_dry_run(ROOT) == plan, "dry-run validation mismatch", errors)
        frozen = load_and_verify_public_freeze(ROOT)
        _require(frozen["sample"]["selected_case_ids"] == EXPECTED_CASE_IDS, "PR #18 selected-case order changed", errors)
    except Exception as exc:
        errors.append(f"public freeze/dry-run validation failed: {type(exc).__name__}: {exc}")

    synthetic = build_synthetic_request_representation(
        model_candidate="gpt-5.4-mini",
        response_schema_hash="sha256:84fbc5413951c712925d85738bc820d776c1ab06172382f143e48495d4a095ec",
    )
    envelope = create_request_envelope(
        request_bytes=serialize_synthetic_request(synthetic),
        controlled_payload_reference="controlled://synthetic/request",
    )
    _require(not _schema_errors(envelope, request_schema), "synthetic request envelope fails schema", errors)
    for forbidden_field in ("prompt_text", "source_text", "credentials"):
        invalid = deepcopy(envelope)
        invalid[forbidden_field] = "synthetic_forbidden_field_test"
        _require(bool(_schema_errors(invalid, request_schema)), f"request schema accepts forbidden field: {forbidden_field}", errors)
    _require(envelope["transmission_authorized"] is False and envelope["transmitted"] is False, "request envelope is not blocked", errors)

    dry_response = {
        "schema_version": "1.0.0",
        "run_id": "synthetic_run_id",
        "request_record_hash": "sha256:" + "6" * 64,
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
        "record_hash": "",
    }
    dry_response["record_hash"] = compute_record_hash(dry_response)
    _require(not _schema_errors(dry_response, response_schema), "dry response envelope fails schema", errors)
    _require(_response_schema_has_no_content_property(response_schema), "response envelope schema exposes response content", errors)

    adapter_text = (ROOT / "src" / "trim_haa" / "llm" / "openai_adapter.py").read_text(encoding="utf-8")
    for network_token in ("import requests", "import httpx", "import openai", "urlopen(", "socket(", "/v1/responses", "/v1/models"):
        _require(network_token not in adapter_text, f"provider adapter contains network implementation token: {network_token}", errors)
    _require(BlockedOpenAIAdapter.network_enabled is False, "provider adapter reports network enabled", errors)

    _require([record.get("case_id") for record in rights_manifest["records"]] == EXPECTED_CASE_IDS, "selected case IDs/order changed", errors)
    rights_records_hash = hashlib.sha256(
        json.dumps(rights_manifest["records"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    _require(rights_records_hash == EXPECTED_RIGHTS_RECORDS_HASH, "rights inventory selected records changed from frozen PR #20 baseline", errors)

    errors.extend(protected_boundary_errors())
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    _require(pyproject["project"]["version"] == EXPECTED_PACKAGE_VERSION, "package version changed", errors)
    package_find = pyproject["tool"]["setuptools"]["packages"]["find"]
    excluded = set(package_find.get("exclude", []))
    _require(
        {
            "trim_haa.llm",
            "trim_haa.llm.*",
            "trim_haa.human_coding",
            "trim_haa.human_coding.*",
        }.issubset(excluded),
        "study-only modules must be excluded from package discovery",
        errors,
    )
    _require("llm" not in pyproject["project"].get("optional-dependencies", {}), "wheel must not advertise an excluded llm extra", errors)
    manifest_text = (ROOT / "MANIFEST.in").read_text(encoding="utf-8") if (ROOT / "MANIFEST.in").is_file() else ""
    _require("prune src/trim_haa/llm" in manifest_text, "sdist must exclude the study-only llm module", errors)
    _require("prune src/trim_haa/human_coding" in manifest_text, "sdist must exclude the study-only human-coding module", errors)

    fixture_dir = ROOT / "tests" / "fixtures" / "human_llm_execution"
    fixture_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(fixture_dir.iterdir()) if path.is_file())
    _require(not any(case_id in fixture_text for case_id in EXPECTED_CASE_IDS), "synthetic fixtures contain selected case IDs", errors)
    _require(not re.search(r"\b(Austen|Bronte|Dickens|Homer|Ovid|Sophocles|Beowulf)\b", fixture_text, re.IGNORECASE), "synthetic fixtures contain selected-source names", errors)
    _require(SECRET_VALUE_RE.search(fixture_text) is None, "synthetic fixtures contain a credential-like value", errors)
    _require(SECRET_VALUE_RE.search(adapter_text) is None, "provider adapter contains a credential-like value", errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("human_llm_execution_scaffold_validation: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
