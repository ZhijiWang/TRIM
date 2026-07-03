import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "studies" / "human_llm_pilot"
DOCS_DIR = ROOT / "docs" / "studies"


def sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalized_text(path: Path) -> str:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n").decode("utf-8")


def condition_payload(condition: str) -> str:
    base = normalized_text(ROOT / "prompts" / "human_llm_pilot" / f"condition_{condition}.txt")
    if condition == "C":
        manual = normalized_text(ROOT / "docs" / "manuals" / "friction_locus_manual_v0_1.json")
        return base.rstrip("\n") + "\nBEGIN_FULL_MANUAL_JSON\n" + manual.rstrip("\n") + "\nEND_FULL_MANUAL_JSON\n"
    return base if base.endswith("\n") else base + "\n"


def assembled_prompt_template(condition: str) -> str:
    return "".join(
        [
            "BEGIN_SHARED_SYSTEM\n"
            + normalized_text(ROOT / "prompts" / "human_llm_pilot" / "system_prompt.txt").rstrip("\n")
            + "\nEND_SHARED_SYSTEM\n",
            f"BEGIN_CONDITION_{condition}\n"
            + condition_payload(condition).rstrip("\n")
            + f"\nEND_CONDITION_{condition}\n",
            normalized_text(ROOT / "prompts" / "human_llm_pilot" / "source_packet_envelope.txt").rstrip("\n") + "\n",
            "BEGIN_MODEL_RESPONSE_SCHEMA\n"
            + normalized_text(ROOT / "schemas" / "human_llm_model_response.schema.json").rstrip("\n")
            + "\nEND_MODEL_RESPONSE_SCHEMA\n",
            normalized_text(ROOT / "prompts" / "human_llm_pilot" / "case_and_run_context.txt").rstrip("\n") + "\n",
        ]
    )


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_freeze_validator_passes():
    result = subprocess.run(
        [sys.executable, "scripts/validate_human_llm_pilot_freeze.py"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "human_llm_pilot_freeze_validation: ok" in result.stdout


def test_sample_size_layers_and_selection_boundaries():
    sample = load_json(DATA_DIR / "sample_manifest.json")
    source_rows = read_csv(DATA_DIR / "source_manifest.csv")
    selection_rows = read_csv(DOCS_DIR / "human_llm_sample_selection_log.csv")
    reconciliation = load_json(DATA_DIR / "candidate_count_reconciliation.json")

    selected_ids = sample["selected_case_ids"]
    assert len(selected_ids) == 25
    assert len(set(selected_ids)) == 25
    assert sum(1 for layer in sample["layer_assignments"].values() if layer == "Layer 1") == 15
    assert sum(1 for layer in sample["layer_assignments"].values() if layer == "Layer 2") == 10
    assert {row["case_id"] for row in source_rows} == set(selected_ids)

    selected_rows = [row for row in selection_rows if row["terminal_category"] == "selected"]
    ineligible_rows = [row for row in selection_rows if row["terminal_category"] == "ineligible"]
    eligible_not_selected = [row for row in selection_rows if row["terminal_category"] == "eligible_not_selected"]
    assert len(selected_rows) == 25
    assert len(ineligible_rows) == 4
    assert len(eligible_not_selected) == 1
    assert reconciliation["screened_count"] == 30
    assert reconciliation["screened_count"] == reconciliation["selected_count"] + reconciliation["eligible_not_selected_count"] + reconciliation["ineligible_count"]
    assert all(row["prior_demo_use"] == "no" for row in selected_rows)
    assert all(row["prior_manual_use"] == "no" for row in selected_rows)
    assert all(row["manual_development_influence"] != "direct" for row in selected_rows)
    assert all("no friction_locus labels" in row["label_information_visible_at_selection"] for row in selected_rows)
    assert all(not row["exclusion_reason_code"] for row in eligible_not_selected)
    assert all(row["non_selection_reason_code"].startswith("NOT_SELECTED_") for row in eligible_not_selected)


def test_public_source_packets_are_redacted_and_non_empirical():
    forbidden = {
        "canonical_text",
        "expected_label",
        "friction_locus",
        "manual_hint",
        "model_output",
        "primary_label",
        "researcher_interpretation",
        "secondary_scholarship",
        "translation_or_gloss",
    }
    rights_rows = {row["case_id"]: row for row in read_csv(DATA_DIR / "source_rights_manifest.csv")}
    for packet_path in sorted((DATA_DIR / "source_packets").glob("*.json")):
        packet = load_json(packet_path)
        assert not (forbidden & set(packet)), packet_path.name
        assert packet["canonical_text_publication_status"] == "not_in_public_repository"
        assert packet["public_redistribution_status"] == "not_confirmed_pending_rights_review"
        assert packet["repository_publication_status"] == "metadata_only_text_redacted"
        assert packet["controlled_storage_reference"].startswith("controlled_private_study_storage/")
        assert packet["text_layer_visibility"]["researcher_and_model_identical"] is True
        assert packet["text_layer_visibility"]["secondary_scholarship_visible"] is False
        assert packet["text_layer_visibility"]["model_facing_instructions_included"] is False
        assert packet["segments"]
        assert all(segment["text_status"] == "redacted_from_public_pr_pending_rights_review" for segment in packet["segments"])
        rights = rights_rows[packet["case_id"]]
        assert rights["repository_publication_status"] == "metadata_only_text_redacted"
        assert rights["public_redistribution_status"] == "not_confirmed_pending_rights_review"


def test_manual_prompt_and_schema_hashes_match_blocked_files():
    manual = load_json(DATA_DIR / "manual_freeze_manifest.json")
    prompts = load_json(DATA_DIR / "prompt_bundle_manifest.json")
    manual_ref = load_json(DATA_DIR / "authoritative_manual_reference.json")

    assert manual_ref["manual_merge_commit"] == "6364add9a89f3fe6d26043727b9d44cb21a76db0"
    assert manual_ref["manual_status"] == "AUTHORITATIVE_FOR_PROTOCOL_REVIEW"
    assert manual["repository_commit"] == "6364add9a89f3fe6d26043727b9d44cb21a76db0"
    assert manual["manual_path"] == "docs/manuals/friction_locus_manual_v0_1.md"
    assert manual["manual_file_hash"] == "f26f5de05819c4fd36c0d88e7d86320d7374c27185c36575b18b584fc5d9b426"
    assert manual["manual_json_hash"] == "797d79fcdb29fc32850c3778c6afb029ac0768207ea33f66d714fe8fa8cb591a"
    assert manual["manual_manifest_hash"] == "1b80c0931a0ed8159aaeeb6e7b348331beb33130776469f223ae2a8cfe89d8de"
    assert manual["manual_freeze_status"] == "MANUAL_COMPATIBILITY_PASSED_AUTHORITATIVE_FOR_PROTOCOL_REVIEW"
    assert manual["schema_hash"] == "2abdf5f5690aada67f1694f8d83dfe95236fbcba46c1bbcfca169567dbda7b12"
    assert manual["schema_compatibility"] == "compatible"
    assert sha256(ROOT / manual["predicted_confusions_path"]) == manual["predicted_confusions_hash"]
    assert sha256(ROOT / manual["category_definitions_path"]) == manual["category_definitions_hash"]
    assert sha256(ROOT / manual["schema_path"]) == manual["schema_hash"]

    for key in [
        "system_prompt",
        "user_prompt_template",
        "condition_A",
        "condition_B",
        "condition_C",
        "human_researcher_instructions",
        "output_schema",
        "model_response_schema",
        "model_response_template",
        "source_packet_envelope",
    ]:
        assert sha256(ROOT / prompts[f"{key}_path"]) == prompts[f"{key}_hash"]


def test_prompts_are_blocked_scaffolds_not_execution_ready():
    prompt_audit = load_json(DATA_DIR / "prompt_condition_difference_audit.json")
    prompts = load_json(DATA_DIR / "prompt_bundle_manifest.json")
    system_prompt = (ROOT / "prompts" / "human_llm_pilot" / "system_prompt.txt").read_text(encoding="utf-8")
    user_template = (ROOT / "prompts" / "human_llm_pilot" / "user_prompt_template.txt").read_text(encoding="utf-8")
    condition_a = (ROOT / "prompts" / "human_llm_pilot" / "condition_A.txt").read_text(encoding="utf-8")
    condition_b = (ROOT / "prompts" / "human_llm_pilot" / "condition_B.txt").read_text(encoding="utf-8")
    condition_c = (ROOT / "prompts" / "human_llm_pilot" / "condition_C.txt").read_text(encoding="utf-8")

    assert prompts["prompt_bundle_status"] == "BLOCKED_NOT_EXECUTION_READY"
    assert prompts["manual_compatibility_status"] == "PASSED_AUTHORITATIVE_MANUAL_REFERENCE_VERIFIED"
    assert prompts["static_prompt_schema_status"] == "PASSED_MODEL_RESPONSE_SCHEMA_COMPATIBILITY_EXECUTION_BLOCKED"
    assert prompts["prompt_assembly_status"] == "PASSED_PROMPT_ASSEMBLY_SPECIFIED_EXECUTION_BLOCKED"
    assert prompts["model_response_enrichment_status"] == "PASSED_CONTRACT_SPECIFIED_EXECUTION_BLOCKED"
    assert prompts["condition_manipulation_status"] == "PASSED_SHARED_BASELINE_WITH_DECLARED_INSTRUCTION_DEPTH_INCREMENTS_EXECUTION_BLOCKED"
    assert prompts["prompt_compatibility_status"].startswith("BLOCKED")
    assert prompt_audit["audit_status"] == "PASSED_STATIC_PROMPT_SCHEMA_AND_ASSEMBLY_COMPATIBILITY_EXECUTION_BLOCKED"
    assert "not a truth verdict" in system_prompt
    assert "Do not browse, use tools" in system_prompt
    assert "model-authored annotation payload only" in system_prompt
    assert "Do not include record_type" in system_prompt
    assert "raw_output_hash" in system_prompt
    assert "{{CASE_ID}}" in user_template
    assert "{{SOURCE_PACKET}}" in user_template
    assert "{{MODEL_RESPONSE_SCHEMA}}" in user_template
    assert "short definitions only" in condition_a
    assert "concise decision rules" in condition_b
    assert "manual_merge_commit: 6364add9a89f3fe6d26043727b9d44cb21a76db0" in condition_c
    assert "exactly eight structured candidate_loci entries" in condition_c
    assert "BEGIN_FULL_MANUAL_JSON" in condition_c
    assert "cue_function requires positive cue-family substitution evidence" in condition_c
    assert "context_inference requires a named, documented, protocol-permitted contextual bridge" in condition_c


def test_prompt_assembly_injects_full_manual_and_is_hashable():
    assembly = load_json(DATA_DIR / "prompt_assembly_manifest.json")
    manual_hash = "797d79fcdb29fc32850c3778c6afb029ac0768207ea33f66d714fe8fa8cb591a"

    assert assembly["assembly_order"] == [
        "SYSTEM_PROMPT",
        "CONDITION_PAYLOAD",
        "SOURCE_PACKET_ENVELOPE",
        "MODEL_RESPONSE_SCHEMA",
        "CASE_AND_RUN_CONTEXT",
    ]
    assert assembly["condition_C_manual_injection"]["source_sha256"] == manual_hash
    assert assembly["condition_C_manual_injection"]["repository_or_tool_access_required_by_model"] is False
    assert "BEGIN_FULL_MANUAL_JSON" in condition_payload("C")
    assert '"manual_version": "friction_locus_manual_v0_1"' in condition_payload("C")
    assert assembly["condition_payload_hashes"]["C"] == sha_text(condition_payload("C"))
    for condition in ["A", "B", "C"]:
        assert assembly["assembled_prompt_template_hashes"][condition] == sha_text(assembled_prompt_template(condition))
    assert len(set(assembly["assembled_prompt_template_hashes"].values())) == 3


def test_model_response_schema_excludes_runtime_metadata_and_enrichment_adds_it():
    response_schema = load_json(ROOT / "schemas" / "human_llm_model_response.schema.json")
    response_template = load_json(ROOT / "templates" / "model_response_payload.json")
    final_template = load_json(ROOT / "templates" / "model_coder_record.json")
    contract = (DOCS_DIR / "model_record_enrichment_contract.md").read_text(encoding="utf-8")

    forbidden = {
        "record_type",
        "actor_type",
        "record_id",
        "timestamp",
        "record_hash",
        "run_id",
        "provider",
        "model",
        "model_version_if_known",
        "prompt_version",
        "instruction_condition",
        "source_packet_hash",
        "raw_output_hash",
        "parse_status",
        "retry_count",
        "technical_failure_status",
        "review_of_record_id",
        "review_of_record_hash",
    }
    assert response_schema["additionalProperties"] is False
    assert not (forbidden & set(response_schema["properties"]))
    assert not (forbidden & set(response_template))
    assert set(response_schema["required"]).issubset(response_template)
    assert "record_hash" not in response_template
    assert "raw_output_hash" in final_template
    assert "record_hash" in final_template
    assert final_template["review_of_record_id"] is None
    assert final_template["review_of_record_hash"] is None
    assert "preserve exact raw response bytes/text" in contract
    assert "final `record_hash` is computed only after enrichment" in contract
    assert "parse failure is represented in the run manifest or failure record without inventing annotation values" in contract


def test_human_model_content_comparability_and_condition_manipulation_are_documented():
    parity = (DOCS_DIR / "pr18_prompt_parity_audit.md").read_text(encoding="utf-8")
    manipulation = (DOCS_DIR / "pr18_condition_manipulation_audit.md").read_text(encoding="utf-8")
    access = (DOCS_DIR / "human_coder_access_and_record_spec.md").read_text(encoding="utf-8")

    assert "full authoritative JSON manual" in parity
    assert "Unresolved substantive asymmetries: none" in parity
    assert "human may search within the supplied manual" in parity
    assert "shared structured annotation baseline with increasing levels of interpretive guidance" in manipulation
    assert "Condition A adds" in manipulation
    assert "Condition B adds" in manipulation
    assert "Condition C adds" in manipulation
    assert "Condition B does not contain the full manual" in manipulation
    assert "Search within the supplied manual is allowed" in access
    assert "The human coder does not manually calculate cryptographic hashes" in access


def test_allocation_governance_and_non_execution_status():
    allocation = load_json(DATA_DIR / "allocation_manifest.json")
    governance = load_json(DATA_DIR / "governance_status.json")
    model_spec = load_json(DATA_DIR / "model_execution_spec.json")
    cost = load_json(DATA_DIR / "cost_ceiling.json")
    freeze_status = load_json(DATA_DIR / "freeze_status.json")
    report = (DOCS_DIR / "human_llm_pilot_freeze_report.md").read_text(encoding="utf-8")
    checklist = (DOCS_DIR / "human_llm_protocol_freeze_checklist.md").read_text(encoding="utf-8")

    assert allocation["second_human_component"] == "not_in_current_protocol"
    assert "No model execution before human lock" in allocation["condition_assignment"]["visibility_constraints"]
    assert allocation["model_stability_run_count"] == 3
    assert allocation["planned_model_run_counts"]["stability_runs_additional_beyond_primary"] == 75
    assert allocation["planned_model_run_counts"]["primary_run_double_counted_in_stability_runs"] is False
    assert allocation["planned_model_run_counts"]["total_planned_model_runs_after_human_lock"] == 118
    assert len(allocation["ablation_subset"]) == 6
    assert governance["protocol_design"] == "Design B"
    assert governance["external_human_recruitment"] == "prohibited"
    assert governance["participant_data_collection"] == "none"
    assert governance["formal_ethics_exemption_claimed"] is False
    assert governance["overall_execution_readiness"] == "BLOCKED"
    assert model_spec["provider"] == "OpenAI"
    assert model_spec["original_unverified_model_id"] == "gpt-5.4-mini"
    assert model_spec["model"] == "UNRESOLVED_PENDING_OFFICIAL_VERIFICATION"
    assert model_spec["account_availability_verified"] is False
    assert model_spec["model_called"] is False
    assert model_spec["browsing"] == "disabled"
    assert model_spec["tools"] == "disabled"
    assert cost["estimated_upper_bound_cost_status"] == "not_final"
    assert freeze_status["manual_compatibility_status"] == "PASSED_AUTHORITATIVE_MANUAL_REFERENCE_VERIFIED"
    assert freeze_status["static_prompt_schema_status"] == "PASSED_MODEL_RESPONSE_SCHEMA_COMPATIBILITY_EXECUTION_BLOCKED"
    assert freeze_status["prompt_assembly_status"] == "PASSED_PROMPT_ASSEMBLY_SPECIFIED_EXECUTION_BLOCKED"
    assert freeze_status["model_response_enrichment_status"] == "PASSED_CONTRACT_SPECIFIED_EXECUTION_BLOCKED"
    assert freeze_status["human_model_content_comparability_status"] == "PASSED_WITH_DOCUMENTED_INTERFACE_AND_METADATA_ASYMMETRIES_EXECUTION_BLOCKED"
    assert freeze_status["condition_manipulation_status"] == "PASSED_SHARED_BASELINE_WITH_DECLARED_INSTRUCTION_DEPTH_INCREMENTS_EXECUTION_BLOCKED"
    assert freeze_status["prompt_compatibility_status"].startswith("BLOCKED")
    assert freeze_status["rights_freeze_status"] == "BLOCKED_RIGHTS_REVIEW_REQUIRED"
    assert freeze_status["private_packet_status"].startswith("BLOCKED")
    assert freeze_status["model_account_status"].startswith("BLOCKED")
    assert freeze_status["runtime_settings_status"] == "BLOCKED_PENDING_PROVIDER_ACCOUNT_VERIFICATION"
    assert freeze_status["execution_authorization_status"].startswith("BLOCKED")
    assert freeze_status["overall_execution_readiness"].startswith("BLOCKED")

    for phrase in [
        "Human coding occurred: no.",
        "Model called: no.",
        "Model outputs created: no.",
        "Findings generated: no.",
        "Released walkthrough artifacts modified: no.",
    ]:
        assert phrase in report

    assert "- [ ] Researcher records completed." in checklist
    assert "- [x] Authoritative current Design B friction_locus manual referenced for protocol review." in checklist
    assert "- [x] Prompt bundle rebuilt for static schema compatibility and deterministic assembly." in checklist
    assert "- [x] Deterministic prompt assembly specified." in checklist
    assert "- [x] Model-authored payload separated from harness metadata." in checklist
    assert "- [ ] Prompts A/B/C frozen as executable." in checklist
    assert "- [ ] Account-verified model and decoding parameters frozen." in checklist
    assert "- [ ] Runtime settings frozen against verified provider/account behavior." in checklist
    assert "- [ ] Run manifests populated." in checklist
