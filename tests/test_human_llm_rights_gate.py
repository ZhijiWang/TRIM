import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from scripts.validate_human_llm_rights_gate import (
    BLOCKED_RIGHTS,
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


def blocked_rights_record(**overrides):
    record = {
        "case_id": "L1_AUSTEN_PNP_001",
        "source_layer": "English original",
        "source_identifier": "metadata-only source identifier",
        "rights_basis": "blocked_pending_documentary_review",
        "jurisdiction_note": "blocked_pending_jurisdiction_review",
        "publication_or_death_date_evidence": "blocked_pending_publication_date_review",
        "translation_rights_basis": "not_applicable",
        "edition_rights_basis": "blocked_pending_edition_review",
        "evidence_documents": [],
        "evidence_urls_or_citations": [],
        "reviewer": "blocked_pending_reviewer_assignment",
        "review_date": None,
        "status": "RIGHTS_SOURCE_REVIEW_REQUIRED",
        "uncertainty": "not_assessed",
        "notes": "blocked pending documentary evidence",
        "record_hash": "",
    }
    record.update(overrides)
    return with_hash(record)


def passed_public_domain_record(**overrides):
    record = {
        "case_id": "L1_AUSTEN_PNP_001",
        "source_layer": "English original",
        "source_identifier": "metadata-only source identifier",
        "rights_basis": "documented public-domain basis",
        "jurisdiction_note": "documented jurisdiction note",
        "publication_or_death_date_evidence": "documented publication date evidence",
        "translation_rights_basis": "not_applicable",
        "edition_rights_basis": "documented edition/source basis",
        "evidence_documents": ["rights/evidence/source_edition_public_domain.md"],
        "evidence_urls_or_citations": [],
        "reviewer": "rights reviewer",
        "review_date": "2026-07-04",
        "status": "RIGHTS_DOCUMENTED_PUBLIC_DOMAIN",
        "uncertainty": "low",
        "notes": "documented non-blocked rights record",
        "record_hash": "",
    }
    record.update(overrides)
    return with_hash(record)


def passed_translation_record(**overrides):
    record = passed_public_domain_record(
        case_id="L2_HOMER_ODYSSEY_001",
        source_layer="English translation from Ancient Greek",
        translation_rights_basis="documented translator and translation edition rights basis",
        evidence_documents=["rights/evidence/translator_translation_source_edition.md"],
        notes="documented non-blocked translation rights record",
    )
    record.update(overrides)
    return with_hash(record)


def access_record(**overrides):
    record = {
        "access_event_id": "ACCESS-001",
        "packet_id": "PKT-001",
        "case_id": "L1_AUSTEN_PNP_001",
        "actor_id": "auditor",
        "actor_role": "private_packet_auditor",
        "access_reason": "authorized metadata-only gate test",
        "access_timestamp": "2026-07-04T00:00:00+10:00",
        "packet_hash_before": "sha256:" + "a" * 64,
        "transformation_type": "none",
        "packet_hash_after": None,
        "content_viewed": False,
        "content_transformed": False,
        "content_exported": False,
        "content_transmitted_to_provider": False,
        "destination": None,
        "rights_status_at_access": "RIGHTS_SOURCE_REVIEW_REQUIRED",
        "provider_model_account_status": "BLOCKED",
        "private_packet_gate_status": "BLOCKED",
        "runtime_settings_status": "BLOCKED",
        "authorization_reference": "AUTH-001",
        "notes": "authorized administrative event without packet text viewing",
        "record_hash": "",
    }
    record.update(overrides)
    return with_hash(record)


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


def test_all_25_rights_evidence_records_exist_and_validate():
    manifest = load_json("data/studies/human_llm_pilot/rights_inventory_manifest.json")

    evidence_paths = [ROOT / record["rights_evidence_path"] for record in manifest["records"]]
    assert len(evidence_paths) == 25
    assert all(path.exists() for path in evidence_paths)

    for path in evidence_paths:
        evidence = json.loads(path.read_text(encoding="utf-8"))
        assert validate_rights_evidence_record(evidence) == []


def test_rights_evidence_record_hashes_are_correct():
    manifest = load_json("data/studies/human_llm_pilot/rights_inventory_manifest.json")

    for record in manifest["records"]:
        evidence = load_json(record["rights_evidence_path"])
        assert evidence["record_hash"] == canonical_record_hash(evidence)


def test_inventory_and_rights_evidence_records_agree():
    manifest = load_json("data/studies/human_llm_pilot/rights_inventory_manifest.json")

    for record in manifest["records"]:
        evidence = load_json(record["rights_evidence_path"])
        assert evidence["case_id"] == record["case_id"]
        assert evidence["status"] == record["rights_status"]
        assert record["private_packet_inspection_blocked"] is True
        assert record["private_packet_model_transmission_blocked"] is True


def test_rights_statuses_keep_execution_blocked():
    manifest = load_json("data/studies/human_llm_pilot/rights_inventory_manifest.json")
    gate_manifest = load_json("data/studies/human_llm_pilot/gate_status_manifest.json")

    assert manifest["translation_rights_unresolved_count"] == 0
    assert manifest["source_rights_unresolved_count"] == 0
    assert manifest["rights_status_summary"] == {
        "RIGHTS_DOCUMENTED_PUBLIC_DOMAIN": 25,
    }
    assert manifest["overall_execution_status"] == OVERALL_BLOCKED_STATUS
    gate_status = {gate["gate"]: gate["status"] for gate in gate_manifest["gates"]}
    assert gate_status["rights_evidence"] == "PASSED_WITH_DOWNSTREAM_GATES_BLOCKED"
    assert gate_status["controlled_private_packet_handling"] == "BLOCKED"
    assert gate_status["human_coding"] == "BLOCKED"
    assert gate_status["model_execution"] == "BLOCKED"
    assert all(record["rights_status"] == "RIGHTS_DOCUMENTED_PUBLIC_DOMAIN" for record in manifest["records"])


def test_blocked_rights_evidence_record_can_exist_without_documentary_evidence():
    record = blocked_rights_record()

    assert validate_rights_evidence_record(record) == []


def test_blocked_translation_rights_evidence_record_remains_valid():
    record = blocked_rights_record(
        case_id="L2_HOMER_ODYSSEY_001",
        source_layer="English translation from Ancient Greek",
        status="RIGHTS_TRANSLATION_REVIEW_REQUIRED",
        translation_rights_basis="blocked_pending_translation_specific_review",
    )

    assert validate_rights_evidence_record(record) == []


def test_l2_translation_records_have_documented_or_blocked_statuses():
    manifest = load_json("data/studies/human_llm_pilot/rights_inventory_manifest.json")

    l2_records = [record for record in manifest["records"] if record["case_id"].startswith("L2_")]
    assert len(l2_records) == 10
    assert all(record["rights_status"] == "RIGHTS_DOCUMENTED_PUBLIC_DOMAIN" for record in l2_records)
    for inventory_record in l2_records:
        evidence = load_json(inventory_record["rights_evidence_path"])
        assert evidence["status"] == inventory_record["rights_status"]
        assert validate_rights_evidence_record(evidence) == []


def test_blocked_rights_record_with_empty_reviewer_fails():
    record = blocked_rights_record(reviewer="")

    assert any("non-empty reviewer" in error for error in validate_rights_evidence_record(record))


def test_blocked_rights_record_with_empty_rights_basis_fails():
    record = blocked_rights_record(rights_basis="")

    assert any("non-empty rights_basis" in error for error in validate_rights_evidence_record(record))


def test_non_blocked_public_domain_null_review_date_fails():
    record = passed_public_domain_record(review_date=None)

    assert any("non-null YYYY-MM-DD review_date" in error for error in validate_rights_evidence_record(record))


def test_non_blocked_public_domain_empty_reviewer_fails():
    record = passed_public_domain_record(reviewer="")

    assert any("non-empty reviewer" in error for error in validate_rights_evidence_record(record))


def test_non_blocked_public_domain_empty_jurisdiction_note_fails():
    record = passed_public_domain_record(jurisdiction_note="")

    assert any("non-empty jurisdiction_note" in error for error in validate_rights_evidence_record(record))


def test_l1_documented_public_domain_records_validate_with_evidence():
    manifest = load_json("data/studies/human_llm_pilot/rights_inventory_manifest.json")

    l1_records = [record for record in manifest["records"] if record["case_id"].startswith("L1_")]
    assert len(l1_records) == 15
    for inventory_record in l1_records:
        evidence = load_json(inventory_record["rights_evidence_path"])
        assert evidence["status"] == "RIGHTS_DOCUMENTED_PUBLIC_DOMAIN"
        assert evidence["review_date"] is not None
        assert evidence["translation_rights_basis"] == "not_applicable"
        assert evidence["evidence_urls_or_citations"]
        assert "private-packet inspection" in evidence["notes"].lower()
        assert validate_rights_evidence_record(evidence) == []


def test_l1_documented_public_domain_record_with_placeholder_basis_fails():
    record = passed_public_domain_record(rights_basis="blocked_pending_documentary_review")

    assert any("blocked placeholder for rights_basis" in error for error in validate_rights_evidence_record(record))


def test_non_blocked_rights_evidence_requires_documentary_evidence():
    record = passed_public_domain_record(evidence_documents=[], evidence_urls_or_citations=[])

    assert any("documentary evidence" in error for error in validate_rights_evidence_record(record))


def test_non_blocked_licensed_record_requires_evidence():
    record = passed_public_domain_record(status="RIGHTS_DOCUMENTED_LICENSED", evidence_documents=[], evidence_urls_or_citations=[])

    assert any("documentary evidence" in error for error in validate_rights_evidence_record(record))


def test_non_blocked_record_rejects_not_assessed_uncertainty():
    record = passed_public_domain_record(uncertainty="not_assessed")

    assert any("not_assessed" in error for error in validate_rights_evidence_record(record))


def test_translation_case_cannot_pass_without_translation_specific_evidence():
    record = passed_translation_record(translation_rights_basis="blocked_pending_translation_review")

    assert any("blocked translation_rights_basis" in error for error in validate_rights_evidence_record(record))


def test_translation_case_cannot_pass_without_translation_specific_evidence_item():
    record = passed_translation_record(evidence_documents=["rights/evidence/general_public_domain.md"])

    assert any("translation-specific evidence item" in error for error in validate_rights_evidence_record(record))


def test_translation_case_with_translation_specific_evidence_passes():
    record = passed_translation_record()

    assert validate_rights_evidence_record(record) == []


def test_l2_documented_translation_records_include_translation_specific_evidence():
    manifest = load_json("data/studies/human_llm_pilot/rights_inventory_manifest.json")

    documented_l2 = [
        record
        for record in manifest["records"]
        if record["case_id"].startswith("L2_") and record["rights_status"] == "RIGHTS_DOCUMENTED_PUBLIC_DOMAIN"
    ]
    assert len(documented_l2) == 10
    for inventory_record in documented_l2:
        evidence = load_json(inventory_record["rights_evidence_path"])
        evidence_text = "\n".join(evidence["evidence_urls_or_citations"]).lower()
        assert "translation" in evidence["translation_rights_basis"].lower() or "edition" in evidence["translation_rights_basis"].lower()
        assert "translation" in evidence_text or "source_edition" in evidence_text
        assert validate_rights_evidence_record(evidence) == []


def test_l2_original_only_evidence_without_translation_or_edition_basis_fails():
    record = passed_translation_record(
        translation_rights_basis="blocked_pending_translation_review",
        evidence_documents=["rights/evidence/ancient_original_public_domain.md"],
    )

    assert any("blocked translation_rights_basis" in error for error in validate_rights_evidence_record(record))


def test_kjv_records_use_conservative_jurisdiction_note():
    for case_id in ["L2_BIBLE_GENESIS_001", "L2_BIBLE_SAMUEL_001"]:
        evidence = load_json(f"data/studies/human_llm_pilot/rights_evidence/{case_id}.rights.json")
        note = evidence["jurisdiction_note"].lower()
        assert evidence["status"] == "RIGHTS_DOCUMENTED_PUBLIC_DOMAIN"
        assert "global copyright clearance" in note
        assert "downstream gates remain blocked" in note
        assert validate_rights_evidence_record(evidence) == []


def test_beowulf_and_herodotus_translation_metadata_conflicts_are_reconciled():
    expected = {
        "L2_BEOWULF_DRAGON_001": "J. Lesslie Hall",
        "L2_HERODOTUS_SCYTHIAN_001": "G. C. Macaulay",
    }
    for case_id, translator in expected.items():
        evidence = load_json(f"data/studies/human_llm_pilot/rights_evidence/{case_id}.rights.json")
        assert evidence["status"] == "RIGHTS_DOCUMENTED_PUBLIC_DOMAIN"
        assert translator in evidence["translation_rights_basis"]
        assert "prior inventory label" in evidence["notes"]
        assert validate_rights_evidence_record(evidence) == []


def test_beowulf_record_cannot_pass_without_translator_or_edition_evidence():
    record = passed_translation_record(
        case_id="L2_BEOWULF_DRAGON_001",
        source_layer="English translation from Old English",
        translation_rights_basis="blocked_pending_translation_review",
        evidence_documents=["rights/evidence/old_english_original_public_domain.md"],
    )

    assert any("blocked translation_rights_basis" in error for error in validate_rights_evidence_record(record))


def test_arabian_nights_record_cannot_pass_without_translation_or_edition_evidence():
    record = passed_translation_record(
        case_id="L2_ARABIAN_NIGHTS_001",
        source_layer="English translation from Arabic/Persian narrative tradition",
        evidence_documents=["rights/evidence/traditional_source_public_domain.md"],
        evidence_urls_or_citations=[],
    )

    assert any("translation-specific evidence item" in error for error in validate_rights_evidence_record(record))


def test_rights_record_hash_rule_remains_non_circular():
    record = passed_public_domain_record()
    tampered = deepcopy(record)
    tampered["rights_basis"] = "changed after hash"

    assert validate_rights_evidence_record(record) == []
    assert any("record_hash mismatch" in error for error in validate_rights_evidence_record(tampered))


def test_access_to_packet_text_requires_authorization_reference():
    record = access_record(content_viewed=True, authorization_reference="")

    assert any("authorization_reference" in error for error in validate_access_log_record(record))


def test_any_access_record_with_empty_authorization_reference_fails():
    record = access_record(authorization_reference="")

    assert any("non-empty authorization_reference" in error for error in validate_access_log_record(record))


def test_export_without_destination_fails():
    record = access_record(
        content_exported=True,
        rights_status_at_access="RIGHTS_DOCUMENTED_PUBLIC_DOMAIN",
        private_packet_gate_status="PASSED",
        provider_model_account_status="PASSED",
        runtime_settings_status="PASSED",
        destination=None,
        notes="export rationale documented",
    )

    assert any("export requires destination" in error for error in validate_access_log_record(record))


def test_export_while_rights_blocked_fails():
    record = access_record(
        content_exported=True,
        destination="local_controlled_storage",
        private_packet_gate_status="PASSED",
        notes="export rationale documented",
    )

    assert any("export requires non-blocked rights" in error for error in validate_access_log_record(record))


def test_export_while_private_packet_gate_blocked_fails():
    record = access_record(
        content_exported=True,
        destination="local_controlled_storage",
        rights_status_at_access="RIGHTS_DOCUMENTED_PUBLIC_DOMAIN",
        private_packet_gate_status="BLOCKED",
        notes="export rationale documented",
    )

    assert any("export requires private-packet gate passed" in error for error in validate_access_log_record(record))


def test_provider_transmission_invalid_while_gates_blocked():
    record = access_record(
        actor_id="execution-harness",
        actor_role="execution_harness",
        content_viewed=True,
        content_exported=True,
        content_transmitted_to_provider=True,
        destination="provider endpoint",
        notes="provider transmission export while blocked should fail",
    )

    errors = validate_access_log_record(record)
    assert any("non-blocked rights" in error for error in errors)
    assert any("provider/model gate" in error for error in errors)
    assert any("private-packet gate" in error for error in errors)
    assert any("runtime settings" in error for error in errors)


def test_private_packet_handling_remains_separately_blocked_even_with_rights_records():
    gate_manifest = load_json("data/studies/human_llm_pilot/gate_status_manifest.json")
    gate_status = {gate["gate"]: gate["status"] for gate in gate_manifest["gates"]}

    assert gate_status["rights_evidence"] == "PASSED_WITH_DOWNSTREAM_GATES_BLOCKED"
    assert gate_status["controlled_private_packet_handling"] == "BLOCKED"
    assert gate_status["provider_model_account"] == "BLOCKED"
    assert gate_status["runtime_settings"] == "BLOCKED"
    assert gate_status["human_coding"] == "BLOCKED"
    assert gate_status["model_execution"] == "BLOCKED"


def test_provider_transmission_without_export_flag_fails():
    record = access_record(
        content_transmitted_to_provider=True,
        content_exported=False,
        destination="provider endpoint",
        rights_status_at_access="RIGHTS_DOCUMENTED_PUBLIC_DOMAIN",
        provider_model_account_status="PASSED",
        private_packet_gate_status="PASSED",
        runtime_settings_status="PASSED",
        notes="provider transmission rationale documented",
    )

    assert any("classified as export" in error for error in validate_access_log_record(record))


def test_transformation_without_transformation_type_fails():
    record = access_record(
        content_transformed=True,
        transformation_type="none",
        private_packet_gate_status="PASSED",
        notes="transformation rationale documented",
    )

    assert any("requires actual transformation_type" in error for error in validate_access_log_record(record))


def test_transformation_without_rationale_fails():
    record = access_record(
        content_transformed=True,
        transformation_type="normalization_for_hashing",
        private_packet_gate_status="PASSED",
        notes="authorized event",
    )

    assert any("transformation requires rationale" in error for error in validate_access_log_record(record))


def test_packet_hash_after_without_transformation_or_hash_verification_fails():
    record = access_record(packet_hash_after="sha256:" + "c" * 64)

    assert any("packet_hash_after requires transformation" in error for error in validate_access_log_record(record))


def test_content_transformed_true_with_null_after_hash_fails():
    record = access_record(
        content_transformed=True,
        transformation_type="normalization_for_hashing",
        packet_hash_after=None,
        private_packet_gate_status="PASSED",
        notes="normalization transformation rationale documented",
    )

    assert any("content_transformed=true requires valid non-null packet_hash_after" in error for error in validate_access_log_record(record))


def test_normalization_for_hashing_with_null_after_hash_fails():
    record = access_record(
        content_transformed=True,
        transformation_type="normalization_for_hashing",
        packet_hash_after=None,
        private_packet_gate_status="PASSED",
        notes="normalization transformation rationale documented",
    )

    assert any("valid packet_hash_after" in error for error in validate_access_log_record(record))


def test_redaction_for_public_metadata_with_null_after_hash_fails():
    record = access_record(
        content_transformed=True,
        transformation_type="redaction_for_public_metadata",
        packet_hash_after=None,
        private_packet_gate_status="PASSED",
        notes="redaction transform rationale documented",
    )

    assert any("valid packet_hash_after" in error for error in validate_access_log_record(record))


def test_packet_construction_with_null_after_hash_fails():
    record = access_record(
        content_transformed=True,
        transformation_type="packet_construction",
        packet_hash_after=None,
        rights_status_at_access="RIGHTS_DOCUMENTED_PUBLIC_DOMAIN",
        private_packet_gate_status="PASSED",
        notes="packet construction transform rationale documented",
    )

    assert any("valid packet_hash_after" in error for error in validate_access_log_record(record))


def test_provider_request_construction_with_null_after_hash_fails():
    record = access_record(
        content_transformed=True,
        transformation_type="provider_request_construction",
        packet_hash_after=None,
        rights_status_at_access="RIGHTS_DOCUMENTED_PUBLIC_DOMAIN",
        provider_model_account_status="PASSED",
        private_packet_gate_status="PASSED",
        runtime_settings_status="PASSED",
        notes="provider request construction transform rationale documented",
    )

    assert any("valid packet_hash_after" in error for error in validate_access_log_record(record))


def test_transformation_type_none_with_after_hash_fails():
    record = access_record(packet_hash_after="sha256:" + "d" * 64)

    assert any("transformation_type=none requires packet_hash_after=null" in error for error in validate_access_log_record(record))


def test_transformation_type_none_with_content_transformed_true_fails():
    record = access_record(
        content_transformed=True,
        transformation_type="none",
        packet_hash_after="sha256:" + "e" * 64,
        private_packet_gate_status="PASSED",
        notes="transformation rationale documented",
    )

    assert any("transformed content requires actual transformation_type" in error for error in validate_access_log_record(record))


def test_hash_only_verification_with_authorization_and_no_text_viewing_passes():
    record = access_record(
        transformation_type="hash_verification_only",
        packet_hash_after="sha256:" + "a" * 64,
        notes="authorized hash verification after controlled metadata check",
    )

    assert validate_access_log_record(record) == []


def test_actual_transformation_with_valid_after_hash_passes_when_required_gate_passes():
    record = access_record(
        content_transformed=True,
        transformation_type="normalization_for_hashing",
        packet_hash_after="sha256:" + "f" * 64,
        private_packet_gate_status="PASSED",
        notes="normalization transformation hash rationale documented",
    )

    assert validate_access_log_record(record) == []


def test_provider_request_construction_still_requires_provider_and_runtime_gates():
    record = access_record(
        content_transformed=True,
        transformation_type="provider_request_construction",
        packet_hash_after="sha256:" + "1" * 64,
        rights_status_at_access="RIGHTS_DOCUMENTED_PUBLIC_DOMAIN",
        private_packet_gate_status="PASSED",
        provider_model_account_status="BLOCKED",
        runtime_settings_status="BLOCKED",
        notes="provider request construction transform hash rationale documented",
    )

    errors = validate_access_log_record(record)
    assert any("provider/model gate" in error for error in errors)
    assert any("runtime settings" in error for error in errors)


def test_access_log_raw_text_like_fields_fail():
    record = access_record()
    record["packet_text"] = "some source text"
    record["record_hash"] = canonical_record_hash(record)

    assert any("raw source text" in error for error in validate_access_log_record(record))


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
