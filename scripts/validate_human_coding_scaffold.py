"""Validate the synthetic-only, fail-closed human-coding scaffold."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from copy import deepcopy
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from scripts.validate_human_llm_execution_scaffold import (  # noqa: E402
    PR18_PROTECTED_EXACT,
    PR18_PROTECTED_PREFIXES,
)
from trim_haa.human_coding.dry_run import (  # noqa: E402
    CODER_SCHEMA_HASH,
    build_human_coding_plan,
    build_synthetic_lifecycle,
    run_human_coding_dry_run,
)
from trim_haa.human_coding.lifecycle import create_superseded_record, edit_draft  # noqa: E402
from trim_haa.human_coding.locking import LockedAnnotationError, verify_frozen_coder_payload_hash  # noqa: E402
from trim_haa.human_coding.schema_validation import load_schema, schema_errors  # noqa: E402
from trim_haa.llm.frozen_reference import load_and_verify_public_freeze  # noqa: E402
from trim_haa.llm.hashing import verify_record_hash  # noqa: E402


STARTING_PR20_HEAD = "4e3007055e700a7ea25fcd3121bae0ea025b834e"
EXPECTED_SYNTHETIC_CODERS = {
    "SYNTHETIC_CODER_A",
    "SYNTHETIC_CODER_B",
    "SYNTHETIC_ADJUDICATOR",
}
UNCHANGED_BOUNDARY_PATHS = {
    "docs/manuals/friction_locus_manual_manifest.json",
    "docs/manuals/friction_locus_manual_v0_1.json",
    "docs/manuals/friction_locus_manual_v0_1.md",
    "docs/core_schema.md",
    "docs/provenance.md",
    "src/trim_haa/schema.py",
    "src/trim_haa/provenance.py",
    "data/trim_haa_core_template.csv",
    "data/trim_haa_assistance_provenance_template.csv",
}
PII_OR_SECRET_KEYS = {
    "address",
    "api_key",
    "credential",
    "email",
    "login",
    "password",
    "phone",
    "private_email",
    "raw_signature",
    "secret",
}
SECRET_VALUE_RE = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|Bearer\s+[A-Za-z0-9._-]{20,})")
SELECTED_SOURCE_NAMES_RE = re.compile(
    r"\b(Austen|Bronte|Chopin|Collins|Conrad|Dickens|Hardy|Hawthorne|James|Melville|Poe|Shelley|Stevenson|Wharton|Wilde|Homer|Sophocles|Herodotus|Ovid|Malory|Beowulf)\b",
    re.IGNORECASE,
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _git_bytes(revision: str, path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    return result.stdout if result.returncode == 0 else None


def _changed_since_start() -> set[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", STARTING_PR20_HEAD, "--"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return set()
    return {line for line in result.stdout.splitlines() if line}


def _contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        if {str(key).lower() for key in value}.intersection(PII_OR_SECRET_KEYS):
            return True
        return any(_contains_forbidden_key(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_key(item) for item in value)
    return False


def validate() -> list[str]:
    errors: list[str] = []
    data_dir = ROOT / "data" / "studies" / "human_llm_pilot"
    schema_dir = ROOT / "schemas"
    required_paths = [
        schema_dir / "human_llm_coder_registry.schema.json",
        schema_dir / "human_llm_coding_session_authorization.schema.json",
        schema_dir / "human_llm_coding_environment.schema.json",
        schema_dir / "human_llm_human_annotation_record.schema.json",
        schema_dir / "human_llm_blinded_assignment.schema.json",
        schema_dir / "human_llm_adjudication_record.schema.json",
        schema_dir / "human_llm_human_coding_plan.schema.json",
        data_dir / "coder_registry_dry_run.json",
        data_dir / "coding_environment_dry_run.json",
        data_dir / "coding_session_authorization_dry_run.json",
        data_dir / "blinded_assignment_dry_run.json",
        data_dir / "human_coding_plan_dry_run.json",
        ROOT / "scripts" / "dry_run_human_coding.py",
        ROOT / "src" / "trim_haa" / "human_coding" / "lifecycle.py",
        ROOT / "src" / "trim_haa" / "human_coding" / "locking.py",
        ROOT / "src" / "trim_haa" / "human_coding" / "gates.py",
        ROOT / "src" / "trim_haa" / "human_coding" / "disagreement.py",
    ]
    for path in required_paths:
        _require(path.exists(), f"missing human-coding scaffold path: {path}", errors)
    if errors:
        return errors

    registry = _load_json(data_dir / "coder_registry_dry_run.json")
    environment = _load_json(data_dir / "coding_environment_dry_run.json")
    session = _load_json(data_dir / "coding_session_authorization_dry_run.json")
    assignment = _load_json(data_dir / "blinded_assignment_dry_run.json")
    plan = _load_json(data_dir / "human_coding_plan_dry_run.json")
    gate_manifest = _load_json(data_dir / "gate_status_manifest.json")
    gate_statuses = {entry["gate"]: entry["status"] for entry in gate_manifest["gates"]}

    schema_pairs = [
        (registry, "human_llm_coder_registry.schema.json"),
        (environment, "human_llm_coding_environment.schema.json"),
        (session, "human_llm_coding_session_authorization.schema.json"),
        (assignment, "human_llm_blinded_assignment.schema.json"),
        (plan, "human_llm_human_coding_plan.schema.json"),
    ]
    for record, schema_name in schema_pairs:
        schema = load_schema(schema_dir / schema_name)
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"invalid JSON schema {schema_name}: {exc}")
        _require(not schema_errors(record, schema, root=ROOT), f"record fails schema: {schema_name}", errors)
        _require(verify_record_hash(record), f"record hash mismatch: {schema_name}", errors)
    for coder in registry["coders"]:
        _require(verify_record_hash(coder), f"coder hash mismatch: {coder.get('coder_id')}", errors)

    _require(registry.get("synthetic_only") is True, "coder registry must be synthetic only", errors)
    _require({coder.get("coder_id") for coder in registry["coders"]} == EXPECTED_SYNTHETIC_CODERS, "coder registry contains a non-synthetic or missing identity", errors)
    _require(registry.get("no_real_coder_registered") is True, "coder registry claims a real coder", errors)
    _require(all(coder.get("coding_eligibility") is False for coder in registry["coders"]), "synthetic coder eligibility must remain false", errors)
    _require(all(coder.get("private_packet_access_eligibility") is False for coder in registry["coders"]), "synthetic coder packet eligibility must remain false", errors)
    _require(not _contains_forbidden_key(registry), "coder registry contains PII/secret field", errors)
    _require(environment.get("environment_verified") is False, "coding environment must remain unverified", errors)
    _require(environment.get("coding_allowed") is False, "coding environment must prohibit coding", errors)
    _require(environment.get("selected_packet_mounted") is False, "coding environment claims a selected packet mount", errors)
    _require(environment.get("real_coder_logged_in") is False, "coding environment claims a real coder login", errors)
    _require(session.get("authorization_status") == "ABSENT_BLOCKED" and session.get("coding_allowed") is False, "session authorization must remain absent and blocked", errors)
    _require(session.get("packet_hash_verification_status") == "NOT_PERFORMED", "packet hash verification must remain not performed", errors)
    _require(assignment.get("synthetic_only") is True and assignment.get("coding_allowed") is False, "blinded assignment must remain synthetic and blocked", errors)

    annotation_schema = load_schema(schema_dir / "human_llm_human_annotation_record.schema.json")
    coder_ref = annotation_schema["properties"]["coder_payload"].get("$ref", "")
    _require(coder_ref.endswith("human_llm_coder_output.schema.json#/$defs/human_coder_record"), "annotation schema does not reference frozen human coder payload", errors)
    _require(plan.get("coder_schema_hash") == CODER_SCHEMA_HASH, "human-coding plan coder schema hash mismatch", errors)
    try:
        lifecycle = build_synthetic_lifecycle(ROOT)
        _require(lifecycle["amendment"]["supersedes_record"]["record_hash"] == lifecycle["locked_a"]["record_hash"], "amendment does not preserve prior hash", errors)
        _require(verify_record_hash(lifecycle["locked_a"]), "locked source record lost hash validity", errors)
        _require(verify_record_hash(lifecycle["superseded"]), "superseded record hash invalid", errors)
        _require(
            sorted(lifecycle["adjudication"]["source_annotation_record_hashes"])
            == sorted([lifecycle["locked_a"]["record_hash"], lifecycle["locked_b"]["record_hash"]]),
            "adjudication does not reference all source annotation hashes",
            errors,
        )
        original = deepcopy(lifecycle["locked_a"])
        try:
            edit_draft(lifecycle["locked_a"], {"adjudication_status": "PENDING"})
        except LockedAnnotationError:
            pass
        else:
            errors.append("locked annotation accepted a silent edit")
        _require(original == lifecycle["locked_a"], "locking test mutated the original record", errors)
        _require(create_superseded_record(lifecycle["locked_a"], lifecycle["amendment"])["record_hash"] == lifecycle["superseded"]["record_hash"], "supersession is nondeterministic", errors)
    except Exception as exc:
        errors.append(f"synthetic lifecycle validation failed: {type(exc).__name__}: {exc}")

    _require(verify_record_hash(plan), "human-coding plan hash mismatch", errors)
    _require(plan.get("actual_packets_inspected") == 0, "human-coding plan reports packet inspection", errors)
    _require(plan.get("actual_coding_sessions_started") == 0, "human-coding plan reports a session", errors)
    _require(plan.get("actual_annotations_created") == 0, "human-coding plan reports a real annotation", errors)
    _require(plan.get("actual_annotations_locked") == 0, "human-coding plan reports a real lock", errors)
    _require(plan.get("actual_adjudications_completed") == 0, "human-coding plan reports adjudication", errors)
    _require(plan.get("coding_allowed") is False and plan.get("overall_status") == "HUMAN_CODING_BLOCKED", "human-coding plan does not fail closed", errors)
    _require(gate_statuses.get("human_coding") == "BLOCKED", "human-coding gate must remain BLOCKED", errors)
    _require(gate_statuses.get("final_authorization") == "BLOCKED", "final authorization must remain BLOCKED", errors)
    _require(gate_statuses.get("model_execution") == "BLOCKED", "model execution must remain BLOCKED", errors)
    for gate in ("provider_model_account", "runtime_settings", "pricing"):
        _require(gate_statuses.get(gate) == "BLOCKED", f"{gate} must remain BLOCKED", errors)
    try:
        _require(build_human_coding_plan(ROOT) == plan, "deterministic human-coding plan mismatch", errors)
        _require(run_human_coding_dry_run(ROOT) == plan, "human-coding dry-run mismatch", errors)
        frozen = load_and_verify_public_freeze(ROOT)
        rights = _load_json(data_dir / "rights_inventory_manifest.json")
        selected = [record["case_id"] for record in rights["records"]]
        _require(selected == frozen["sample"]["selected_case_ids"], "selected cases/order changed", errors)
    except Exception as exc:
        errors.append(f"human-coding dry-run/freeze validation failed: {type(exc).__name__}: {exc}")

    fixture_dir = ROOT / "tests" / "fixtures" / "human_coding"
    fixture_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(fixture_dir.iterdir()) if path.is_file())
    _require(SELECTED_SOURCE_NAMES_RE.search(fixture_text) is None, "human-coding fixtures contain selected-source names", errors)
    _require("L1_" not in fixture_text and "L2_" not in fixture_text, "human-coding fixtures contain selected case IDs", errors)
    _require(SECRET_VALUE_RE.search(fixture_text) is None, "human-coding fixtures contain credential-like values", errors)
    for payload_path in fixture_dir.glob("synthetic_coder_payload_[ab].json"):
        _require(verify_frozen_coder_payload_hash(_load_json(payload_path)), f"synthetic payload hash mismatch: {payload_path.name}", errors)
    checked_adjudication = _load_json(fixture_dir / "synthetic_adjudication_draft.json")
    adjudication_schema = load_schema(schema_dir / "human_llm_adjudication_record.schema.json")
    _require(not schema_errors(checked_adjudication, adjudication_schema, root=ROOT), "checked synthetic adjudication fixture fails schema", errors)
    _require(verify_record_hash(checked_adjudication), "checked synthetic adjudication fixture hash mismatch", errors)

    changed = _changed_since_start()
    protected_changes = {
        path for path in changed if path in PR18_PROTECTED_EXACT or any(path.startswith(prefix) for prefix in PR18_PROTECTED_PREFIXES)
    }
    _require(not protected_changes, f"PR #18 artifacts or prompts changed: {sorted(protected_changes)}", errors)
    for path in UNCHANGED_BOUNDARY_PATHS:
        current = (ROOT / path).read_bytes() if (ROOT / path).exists() else None
        _require(current == _git_bytes(STARTING_PR20_HEAD, path), f"protected manual/Core/provenance path changed: {path}", errors)
    current_version = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    starting_pyproject = _git_bytes(STARTING_PR20_HEAD, "pyproject.toml")
    _require(starting_pyproject is not None and current_version == tomllib.loads(starting_pyproject.decode("utf-8"))["project"]["version"], "package version changed", errors)

    implementation_paths = list((ROOT / "src" / "trim_haa" / "human_coding").glob("*.py")) + [
        ROOT / "scripts" / "dry_run_human_coding.py"
    ]
    implementation_text = "\n".join(path.read_text(encoding="utf-8") for path in implementation_paths)
    for network_token in ("import requests", "import httpx", "import openai", "urlopen(", "socket(", "/v1/"):
        _require(network_token not in implementation_text, f"human-coding scaffold contains network/provider token: {network_token}", errors)
    _require(SECRET_VALUE_RE.search(implementation_text) is None, "human-coding scaffold contains credential-like value", errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("human_coding_scaffold_validation: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
