import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from scripts.validate_human_llm_rights_gate import (
    EXPECTED_CASE_IDS,
    OVERALL_BLOCKED_STATUS,
    canonical_record_hash,
    validate_access_log_record,
    validate_rights_evidence_record,
)


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def with_hash(record):
    record = deepcopy(record)
    record["record_hash"] = canonical_record_hash(record)
    return record


def test_rights_gate_validator_passes():
    result = subprocess.run(
        [sys.executable, "scripts/validate_human_llm_rights_gate.py"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "human_llm_rights_gate_validation: ok" in result.stdout


def test_rights_inventory_matches_selected_cases_and_contains_no_private_text():
    manifest = load_json("data/studies/human_llm_pilot/rights_inventory_manifest.json")

    assert manifest["selected_case_count"] == 25
    assert [record["case_id"] for record in manifest["records"]] == EXPECTED_CASE_IDS
    assert manifest["content_policy"] == "metadata_only_no_private_text_no_private_packet_hashes"
    assert all("canonical_text" not in record for record in manifest["records"])
    assert all("private_source_text_hash" not in record for record in manifest["records"])
    assert all(record["private_packet_inspection_blocked"] is True for record in manifest["records"])


def test_rights_statuses_keep_execution_blocked():
    manifest = load_json("data/studies/human_llm_pilot/rights_inventory_manifest.json")
    gate_manifest = load_json("data/studies/human_llm_pilot/gate_status_manifest.json")

    assert manifest["translation_rights_unresolved_count"] == 10
    assert manifest["source_rights_unresolved_count"] == 25
    assert manifest["overall_execution_status"] == OVERALL_BLOCKED_STATUS
    gate_status = {gate["gate"]: gate["status"] for gate in gate_manifest["gates"]}
    assert gate_status["rights_evidence"] == "BLOCKED"
    assert gate_status["controlled_private_packet_handling"] == "BLOCKED"
    assert gate_status["human_coding"] == "BLOCKED"
    assert gate_status["model_execution"] == "BLOCKED"


def test_blocked_rights_evidence_record_can_exist_without_documentary_evidence():
    record = with_hash(
        {
            "case_id": "L1_AUSTEN_PNP_001",
            "source_layer": "English original",
            "source_identifier": "metadata-only source identifier",
            "rights_basis": "",
            "jurisdiction_note": "not yet assessed",
            "publication_or_death_date_evidence": "",
            "translation_rights_basis": "",
            "edition_rights_basis": "",
            "evidence_documents": [],
            "evidence_urls_or_citations": [],
            "reviewer": "author-assisted internal preparation",
            "review_date": None,
            "status": "RIGHTS_SOURCE_REVIEW_REQUIRED",
            "uncertainty": "not_assessed",
            "notes": "blocked pending documentary evidence",
            "record_hash": "",
        }
    )

    assert validate_rights_evidence_record(record) == []


def test_non_blocked_rights_evidence_requires_documentary_evidence():
    record = with_hash(
        {
            "case_id": "L1_AUSTEN_PNP_001",
            "source_layer": "English original",
            "source_identifier": "metadata-only source identifier",
            "rights_basis": "public domain asserted",
            "jurisdiction_note": "reviewed jurisdiction note",
            "publication_or_death_date_evidence": "publication date evidence",
            "translation_rights_basis": "",
            "edition_rights_basis": "edition evidence",
            "evidence_documents": [],
            "evidence_urls_or_citations": [],
            "reviewer": "rights reviewer",
            "review_date": "2026-07-04",
            "status": "RIGHTS_DOCUMENTED_PUBLIC_DOMAIN",
            "uncertainty": "low",
            "notes": "missing evidence should fail",
            "record_hash": "",
        }
    )

    assert any("documentary evidence" in error for error in validate_rights_evidence_record(record))


def test_translation_case_cannot_pass_without_translation_specific_evidence():
    record = with_hash(
        {
            "case_id": "L2_HOMER_ODYSSEY_001",
            "source_layer": "English translation from Ancient Greek",
            "source_identifier": "metadata-only source identifier",
            "rights_basis": "public domain asserted",
            "jurisdiction_note": "reviewed jurisdiction note",
            "publication_or_death_date_evidence": "publication date evidence",
            "translation_rights_basis": "",
            "edition_rights_basis": "edition evidence",
            "evidence_documents": ["rights/evidence/example.md"],
            "evidence_urls_or_citations": [],
            "reviewer": "rights reviewer",
            "review_date": "2026-07-04",
            "status": "RIGHTS_DOCUMENTED_PUBLIC_DOMAIN",
            "uncertainty": "low",
            "notes": "missing translation basis should fail",
            "record_hash": "",
        }
    )

    assert any("translation-specific evidence" in error for error in validate_rights_evidence_record(record))


def test_access_to_packet_text_requires_authorization_reference():
    record = with_hash(
        {
            "access_event_id": "ACCESS-001",
            "packet_id": "PKT-001",
            "case_id": "L1_AUSTEN_PNP_001",
            "actor_id": "auditor",
            "actor_role": "private_packet_auditor",
            "access_reason": "protocol test",
            "access_timestamp": "2026-07-04T00:00:00+10:00",
            "packet_hash_before": "sha256:" + "a" * 64,
            "packet_hash_after": None,
            "content_viewed": True,
            "content_transformed": False,
            "content_exported": False,
            "content_transmitted_to_provider": False,
            "destination": None,
            "rights_status_at_access": "RIGHTS_SOURCE_REVIEW_REQUIRED",
            "provider_model_account_status": "BLOCKED",
            "private_packet_gate_status": "BLOCKED",
            "runtime_settings_status": "BLOCKED",
            "authorization_reference": "",
            "notes": "viewing without authorization should fail",
            "record_hash": "",
        }
    )

    assert any("authorization_reference" in error for error in validate_access_log_record(record))


def test_provider_transmission_invalid_while_gates_blocked():
    record = with_hash(
        {
            "access_event_id": "ACCESS-002",
            "packet_id": "PKT-001",
            "case_id": "L1_AUSTEN_PNP_001",
            "actor_id": "execution-harness",
            "actor_role": "execution_harness",
            "access_reason": "provider transmission",
            "access_timestamp": "2026-07-04T00:00:00+10:00",
            "packet_hash_before": "sha256:" + "b" * 64,
            "packet_hash_after": None,
            "content_viewed": True,
            "content_transformed": False,
            "content_exported": True,
            "content_transmitted_to_provider": True,
            "destination": "provider endpoint",
            "rights_status_at_access": "RIGHTS_SOURCE_REVIEW_REQUIRED",
            "provider_model_account_status": "BLOCKED",
            "private_packet_gate_status": "BLOCKED",
            "runtime_settings_status": "BLOCKED",
            "authorization_reference": "AUTH-001",
            "notes": "transmission while blocked should fail",
            "record_hash": "",
        }
    )

    errors = validate_access_log_record(record)
    assert any("non-blocked rights" in error for error in errors)
    assert any("provider/model gate" in error for error in errors)
    assert any("private-packet gate" in error for error in errors)
    assert any("runtime settings" in error for error in errors)


def test_public_gate_artifacts_do_not_contain_private_packet_text_markers():
    paths = [
        ROOT / "docs/studies/human_llm_rights_inventory.md",
        ROOT / "data/studies/human_llm_pilot/rights_inventory_manifest.json",
        ROOT / "docs/studies/private_packet_handling_protocol.md",
        ROOT / "data/studies/human_llm_pilot/gate_status_manifest.json",
        ROOT / "docs/studies/human_llm_gate_resolution_plan.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    assert "BEGIN_SOURCE_PACKET" not in combined
    assert "canonical_text" not in combined
    assert "translation_text" not in combined
    assert "fixed_context" not in combined


def test_existing_package_and_study_boundaries_remain_unchanged():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    existing_study_schema = (ROOT / "schemas/human_llm_coder_output.schema.json").read_text(encoding="utf-8")

    assert 'version = "0.3.0a1"' in pyproject
    assert "does not alter TRIM-HAA Core or provenance schemas" in existing_study_schema
    assert (ROOT / "schemas/human_llm_rights_evidence.schema.json").exists()
    assert (ROOT / "schemas/private_packet_access_log.schema.json").exists()
