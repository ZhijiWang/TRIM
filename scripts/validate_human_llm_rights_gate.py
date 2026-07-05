"""Validate the human-LLM rights and private-packet gate artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OVERALL_BLOCKED_STATUS = (
    "BLOCKED_PENDING_RIGHTS_PRIVATE_PACKETS_MODEL_ACCOUNT_RUNTIME_SETTINGS_PRICING_"
    "AND_FINAL_EXECUTION_AUTHORIZATION"
)
PR18_HEAD = "eac65f27bbe302a17e5f508ac1d516178e917aea"
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
NON_BLOCKED_RIGHTS = {"RIGHTS_DOCUMENTED_PUBLIC_DOMAIN", "RIGHTS_DOCUMENTED_LICENSED"}
BLOCKED_RIGHTS = {
    "RIGHTS_TRANSLATION_REVIEW_REQUIRED",
    "RIGHTS_SOURCE_REVIEW_REQUIRED",
    "RIGHTS_UNKNOWN_BLOCKED",
    "RIGHTS_NOT_ASSESSED_BLOCKED",
}
PRIVATE_TEXT_KEYS = {
    "canonical_text",
    "content",
    "excerpt",
    "source_text",
    "translation_text",
    "gloss_text",
    "fixed_context",
    "model_input_text",
    "packet_text",
    "prompt_text",
    "raw_packet",
    "source_packet_text",
    "private_source_text_hash",
    "private_source_packet_hash",
}
PRIVATE_TEXT_PATTERNS = [
    "BEGIN_SOURCE_PACKET",
    "canonical text:",
    "fixed context:",
    "controlled packet text",
]
BLOCKED_PLACEHOLDER_TOKENS = {
    "blocked_pending",
    "pending",
    "not_assessed",
    "not yet assessed",
    "not_resolved",
    "review_required",
}
TRANSLATION_EVIDENCE_TOKENS = {
    "translation",
    "translator",
    "translated",
    "edition",
    "source_edition",
}
ACTUAL_TRANSFORMATION_TYPES = {
    "normalization_for_hashing",
    "redaction_for_public_metadata",
    "packet_construction",
    "provider_request_construction",
}
ISO_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def canonical_record_hash(record: dict[str, Any]) -> str:
    payload = deepcopy(record)
    payload.pop("record_hash", None)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def contains_private_text_markers(value: Any) -> bool:
    if isinstance(value, dict):
        if PRIVATE_TEXT_KEYS.intersection(value.keys()):
            return True
        return any(contains_private_text_markers(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_private_text_markers(item) for item in value)
    if isinstance(value, str):
        lower = value.lower()
        return any(pattern.lower() in lower for pattern in PRIVATE_TEXT_PATTERNS)
    return False


def non_empty_text(record: dict[str, Any], field: str) -> bool:
    return isinstance(record.get(field), str) and bool(record[field].strip())


def looks_like_blocked_placeholder(value: Any) -> bool:
    text = str(value or "").strip().lower()
    return not text or any(token in text for token in BLOCKED_PLACEHOLDER_TOKENS)


def has_documentary_evidence(record: dict[str, Any]) -> bool:
    return bool(record.get("evidence_documents")) or bool(record.get("evidence_urls_or_citations"))


def is_translation_rights_record(record: dict[str, Any]) -> bool:
    source_layer = str(record.get("source_layer", ""))
    translation_basis = str(record.get("translation_rights_basis", ""))
    return (
        "translation" in source_layer.lower()
        or record.get("status") == "RIGHTS_TRANSLATION_REVIEW_REQUIRED"
        or translation_basis.strip().lower() != "not_applicable"
    )


def has_translation_specific_evidence(record: dict[str, Any]) -> bool:
    evidence_items = list(record.get("evidence_documents") or []) + list(record.get("evidence_urls_or_citations") or [])
    joined = "\n".join(str(item).lower() for item in evidence_items)
    return any(token in joined for token in TRANSLATION_EVIDENCE_TOKENS)


def validate_rights_evidence_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    status = record.get("status")
    require(bool(record.get("case_id")), "rights evidence requires case_id", errors)
    require(status in NON_BLOCKED_RIGHTS | BLOCKED_RIGHTS, "rights evidence status is invalid", errors)
    for field in [
        "reviewer",
        "rights_basis",
        "jurisdiction_note",
        "publication_or_death_date_evidence",
        "translation_rights_basis",
        "edition_rights_basis",
        "notes",
    ]:
        require(non_empty_text(record, field), f"rights evidence requires non-empty {field}", errors)
    require(
        isinstance(record.get("record_hash"), str)
        and re.fullmatch(r"sha256:[a-f0-9]{64}", record["record_hash"]),
        "rights evidence record_hash must use sha256: convention",
        errors,
    )
    if status in NON_BLOCKED_RIGHTS:
        require(isinstance(record.get("review_date"), str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", record["review_date"]), "non-blocked rights evidence requires non-null YYYY-MM-DD review_date", errors)
        require(has_documentary_evidence(record), "non-blocked rights evidence requires documentary evidence", errors)
        require(record.get("uncertainty") != "not_assessed", "non-blocked rights evidence cannot use not_assessed uncertainty", errors)
        for field in [
            "reviewer",
            "rights_basis",
            "jurisdiction_note",
            "publication_or_death_date_evidence",
            "edition_rights_basis",
            "notes",
        ]:
            require(not looks_like_blocked_placeholder(record.get(field)), f"non-blocked rights evidence cannot use blocked placeholder for {field}", errors)
        if is_translation_rights_record(record):
            require(non_empty_text(record, "translation_rights_basis"), "translation case cannot pass without translation-specific evidence", errors)
            require(not looks_like_blocked_placeholder(record.get("translation_rights_basis")), "non-blocked translation case cannot use blocked translation_rights_basis", errors)
            require(has_translation_specific_evidence(record), "non-blocked translation case requires translation-specific evidence item or citation", errors)
    elif is_translation_rights_record(record):
        require(non_empty_text(record, "translation_rights_basis"), "blocked translation record still requires translation_rights_basis placeholder", errors)
    require(record.get("record_hash") == canonical_record_hash(record), "rights evidence record_hash mismatch", errors)
    require(not contains_private_text_markers(record), "rights evidence record must not include private source text", errors)
    return errors


def validate_access_log_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ["authorization_reference", "access_reason", "actor_id", "access_timestamp", "packet_id", "case_id", "notes"]:
        require(non_empty_text(record, field), f"access log requires non-empty {field}", errors)
    require(
        isinstance(record.get("access_timestamp"), str) and ISO_TIMESTAMP_RE.fullmatch(record["access_timestamp"]),
        "access log requires ISO-like timestamp with timezone",
        errors,
    )
    require(
        isinstance(record.get("record_hash"), str)
        and re.fullmatch(r"sha256:[a-f0-9]{64}", record["record_hash"]),
        "access log record_hash must use sha256: convention",
        errors,
    )
    require(not contains_private_text_markers(record), "access log must not include raw source text", errors)
    transformation_type = record.get("transformation_type")
    require(
        transformation_type
        in {
            "none",
            "hash_verification_only",
            "normalization_for_hashing",
            "redaction_for_public_metadata",
            "packet_construction",
            "provider_request_construction",
        },
        "access log requires valid transformation_type",
        errors,
    )
    if record.get("content_viewed"):
        require(non_empty_text(record, "authorization_reference"), "viewing packet text requires authorization_reference", errors)
    if record.get("content_exported"):
        require(record.get("rights_status_at_access") in NON_BLOCKED_RIGHTS, "export requires non-blocked rights", errors)
        require(record.get("private_packet_gate_status") == "PASSED", "export requires private-packet gate passed", errors)
        require(non_empty_text(record, "destination"), "export requires destination", errors)
        require("export" in str(record.get("notes", "")).lower(), "export requires export rationale in notes", errors)
        destination = str(record.get("destination", "")).lower()
        if destination and "local_controlled_storage" not in destination:
            require(record.get("provider_model_account_status") == "PASSED", "external export requires provider/model gate passed", errors)
            require(record.get("runtime_settings_status") == "PASSED", "external export requires runtime settings passed", errors)
    packet_hash_after = record.get("packet_hash_after")
    valid_after_hash = isinstance(packet_hash_after, str) and re.fullmatch(r"sha256:[a-f0-9]{64}", packet_hash_after)
    if record.get("content_transformed"):
        require(valid_after_hash, "content_transformed=true requires valid non-null packet_hash_after", errors)
        require(transformation_type in ACTUAL_TRANSFORMATION_TYPES, "transformed content requires actual transformation_type", errors)
        require(record.get("private_packet_gate_status") == "PASSED", "transformation requires private-packet gate passed", errors)
        require("transform" in str(record.get("notes", "")).lower() or "normalization" in str(record.get("notes", "")).lower() or "hash" in str(record.get("notes", "")).lower(), "transformation requires rationale in notes", errors)
        if transformation_type in {"packet_construction", "provider_request_construction"}:
            require(record.get("rights_status_at_access") in NON_BLOCKED_RIGHTS, "packet/provider construction requires non-blocked rights", errors)
        if transformation_type == "provider_request_construction":
            require(record.get("provider_model_account_status") == "PASSED", "provider request construction requires provider/model gate passed", errors)
            require(record.get("runtime_settings_status") == "PASSED", "provider request construction requires runtime settings passed", errors)
    else:
        require(transformation_type in {None, "none", "hash_verification_only"}, "non-transformed event cannot use transformation type requiring content change", errors)
    if transformation_type in ACTUAL_TRANSFORMATION_TYPES:
        require(record.get("content_transformed") is True, "actual transformation type requires content_transformed=true", errors)
        require(valid_after_hash, "actual transformation type requires valid packet_hash_after", errors)
    if transformation_type == "none":
        require(record.get("content_transformed") is False, "transformation_type=none requires content_transformed=false", errors)
        require(packet_hash_after is None, "transformation_type=none requires packet_hash_after=null", errors)
    if packet_hash_after is not None:
        require(
            valid_after_hash,
            "packet_hash_after must be a valid sha256 value",
            errors,
        )
        require(
            record.get("content_transformed") or transformation_type == "hash_verification_only",
            "packet_hash_after requires transformation or hash-verification event",
            errors,
        )
        require(
            "hash" in str(record.get("notes", "")).lower() or "after" in str(record.get("notes", "")).lower(),
            "packet_hash_after requires notes explaining after-hash reason",
            errors,
        )
    if record.get("content_transmitted_to_provider"):
        require(record.get("rights_status_at_access") in NON_BLOCKED_RIGHTS, "provider transmission requires non-blocked rights", errors)
        require(record.get("provider_model_account_status") == "PASSED", "provider transmission requires provider/model gate passed", errors)
        require(record.get("private_packet_gate_status") == "PASSED", "provider transmission requires private-packet gate passed", errors)
        require(record.get("runtime_settings_status") == "PASSED", "provider transmission requires runtime settings passed", errors)
        require(record.get("content_exported") is True, "provider transmission must also be classified as export", errors)
        require(non_empty_text(record, "destination"), "provider transmission requires destination", errors)
        require(non_empty_text(record, "authorization_reference"), "provider transmission requires authorization_reference", errors)
        require("provider" in str(record.get("notes", "")).lower(), "provider transmission requires provider rationale in notes", errors)
    require(record.get("record_hash") == canonical_record_hash(record), "access log record_hash mismatch", errors)
    return errors


def validate() -> list[str]:
    errors: list[str] = []
    docs = ROOT / "docs" / "studies"
    data = ROOT / "data" / "studies" / "human_llm_pilot"
    schemas = ROOT / "schemas"

    rights_doc = docs / "human_llm_rights_inventory.md"
    rights_manifest_path = data / "rights_inventory_manifest.json"
    rights_evidence_dir = data / "rights_evidence"
    protocol_path = docs / "private_packet_handling_protocol.md"
    gate_manifest_path = data / "gate_status_manifest.json"
    plan_path = docs / "human_llm_gate_resolution_plan.md"
    rights_schema_path = schemas / "human_llm_rights_evidence.schema.json"
    access_schema_path = schemas / "private_packet_access_log.schema.json"

    for path in [rights_doc, rights_manifest_path, protocol_path, gate_manifest_path, plan_path, rights_schema_path, access_schema_path]:
        require(path.exists(), f"missing required rights/private-packet gate file: {path}", errors)
    require(rights_evidence_dir.exists(), "missing rights evidence directory", errors)

    if errors:
        return errors

    rights_manifest = load_json(rights_manifest_path)
    gate_manifest = load_json(gate_manifest_path)
    rights_schema = load_json(rights_schema_path)
    access_schema = load_json(access_schema_path)
    protocol = protocol_path.read_text(encoding="utf-8")
    plan = plan_path.read_text(encoding="utf-8")
    rights_doc_text = rights_doc.read_text(encoding="utf-8")

    require(rights_manifest["source_pr18_reference"]["head_sha"] == PR18_HEAD, "rights manifest PR18 reference mismatch", errors)
    require(rights_manifest["overall_execution_status"] == OVERALL_BLOCKED_STATUS, "rights manifest overall status mismatch", errors)
    records = rights_manifest.get("records", [])
    require(len(records) == 25, "rights inventory must contain 25 selected cases", errors)
    require([record.get("case_id") for record in records] == EXPECTED_CASE_IDS, "rights inventory case order or IDs mismatch", errors)
    require(rights_manifest["selected_case_count"] == len(EXPECTED_CASE_IDS), "selected case count mismatch", errors)
    require(rights_manifest["translation_rights_unresolved_count"] == 10, "translation unresolved count mismatch", errors)
    require(rights_manifest["source_rights_unresolved_count"] == 25, "source unresolved count mismatch", errors)
    require(rights_manifest["private_packet_inspection_blocked_count"] == 25, "private packet blocked count mismatch", errors)

    evidence_records: dict[str, dict[str, Any]] = {}
    for record in records:
        evidence_path = record.get("rights_evidence_path")
        require(isinstance(evidence_path, str) and bool(evidence_path), f"{record.get('case_id')}: rights evidence path required", errors)
        evidence_file = ROOT / evidence_path if isinstance(evidence_path, str) else ROOT / "__missing__"
        require(evidence_file.exists(), f"{record.get('case_id')}: rights evidence file missing", errors)
        if evidence_file.exists():
            evidence = load_json(evidence_file)
            evidence_records[record["case_id"]] = evidence
            for evidence_error in validate_rights_evidence_record(evidence):
                errors.append(f"{record.get('case_id')}: {evidence_error}")
            require(evidence.get("case_id") == record.get("case_id"), f"{record.get('case_id')}: evidence case_id mismatch", errors)
            require(evidence.get("status") == record.get("rights_status"), f"{record.get('case_id')}: inventory/evidence status mismatch", errors)
            require(not contains_private_text_markers(evidence), f"{record.get('case_id')}: evidence contains private text marker", errors)
        require(record.get("private_packet_inspection_blocked") is True, f"{record.get('case_id')}: private inspection must be blocked", errors)
        require(record.get("private_packet_model_transmission_blocked") is True, f"{record.get('case_id')}: private provider transmission must be blocked", errors)
        require(not contains_private_text_markers(record), f"{record.get('case_id')}: rights inventory contains private text marker", errors)
    require(set(evidence_records) == set(EXPECTED_CASE_IDS), "rights evidence case set mismatch", errors)

    require(not contains_private_text_markers(rights_manifest), "rights inventory manifest contains private text markers", errors)
    require("no private source-packet text" in rights_doc_text, "rights inventory must state no private text", errors)
    require("does not approve rights" in rights_doc_text, "rights inventory must avoid rights approval", errors)
    require("must not be committed" in protocol, "private-packet protocol must prohibit committing private packets", errors)
    require("Human coding may not start until" in protocol, "protocol must block human coding", errors)
    require("Model execution may not start until" in protocol, "protocol must block model execution", errors)
    require("This PR does not authorize" in plan, "gate plan must avoid execution authorization", errors)

    schema_names = {rights_schema["title"], access_schema["title"]}
    require("Human-LLM pilot rights evidence record" in schema_names, "rights evidence schema title mismatch", errors)
    require("Human-LLM pilot private packet access log" in schema_names, "private access schema title mismatch", errors)
    require("additionalProperties" in rights_schema and rights_schema["additionalProperties"] is False, "rights schema must reject extra properties", errors)
    require("additionalProperties" in access_schema and access_schema["additionalProperties"] is False, "access schema must reject extra properties", errors)
    require("record_hash" in rights_schema["required"], "rights schema must require record_hash", errors)
    require("record_hash" in access_schema["required"], "access schema must require record_hash", errors)

    gate_status = {gate["gate"]: gate for gate in gate_manifest["gates"]}
    passed_gates = {
        "manual_compatibility",
        "prompt_assembly",
        "model_response_schema",
        "enrichment_contract",
        "condition_manipulation",
        "human_model_content_comparability",
    }
    blocked_gates = {
        "rights_evidence",
        "controlled_private_packet_handling",
        "provider_model_account",
        "runtime_settings",
        "pricing",
        "final_authorization",
        "human_coding",
        "model_execution",
    }
    require(set(gate_status) == passed_gates | blocked_gates, "gate manifest gate set mismatch", errors)
    for gate in passed_gates:
        require(gate_status[gate]["status"].startswith("PASSED"), f"{gate}: expected passed status", errors)
        require(gate_status[gate]["execution_remains_blocked"] is True, f"{gate}: execution must remain blocked", errors)
    for gate in blocked_gates:
        if gate == "rights_evidence":
            if any(record.get("rights_status") in BLOCKED_RIGHTS for record in records):
                require(gate_status[gate]["status"] == "BLOCKED", f"{gate}: expected blocked status while any rights record is unresolved", errors)
            else:
                require(gate_status[gate]["status"].startswith("PASSED"), f"{gate}: expected passed status only when every rights record is non-blocked", errors)
        else:
            require(gate_status[gate]["status"] == "BLOCKED", f"{gate}: expected blocked status", errors)
        require(gate_status[gate]["execution_remains_blocked"] is True, f"{gate}: execution must remain blocked", errors)

    require(gate_manifest["overall_execution_status"] == OVERALL_BLOCKED_STATUS, "gate manifest overall status mismatch", errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("human_llm_rights_gate_validation: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
