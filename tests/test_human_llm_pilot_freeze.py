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

    assert manual["repository_commit"] == "6998175eeca5d349072bf31012c69f2d568f28ec"
    assert manual["manual_path"] is None
    assert manual["manual_file_hash"] is None
    assert manual["manual_freeze_status"] == "BLOCKED_INCOMPLETE_AUTHORITATIVE_MANUAL"
    assert sha256(ROOT / manual["predicted_confusions_path"]) == manual["predicted_confusions_hash"]
    assert sha256(ROOT / manual["category_definitions_path"]) == manual["category_definitions_hash"]
    assert sha256(ROOT / manual["schema_path"]) == manual["schema_hash"]

    for key in [
        "system_prompt",
        "user_prompt_template",
        "condition_A",
        "condition_B",
        "condition_C",
        "output_schema",
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
    assert prompt_audit["audit_status"] == "BLOCKED"
    assert "not a truth verdict" in system_prompt
    assert "Do not browse, use tools" in system_prompt
    assert "{{CASE_ID}}" in user_template
    assert "{{SOURCE_PACKET}}" in user_template
    assert "{{OUTPUT_SCHEMA}}" in user_template
    assert "short definitions only" in condition_a
    assert "concise decision rules" in condition_b
    assert "no complete authoritative current Design B friction_locus manual" in condition_c


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
    assert freeze_status["overall_execution_readiness"] == "BLOCKED"

    for phrase in [
        "Human coding occurred: no.",
        "Model called: no.",
        "Model outputs created: no.",
        "Findings generated: no.",
        "Released walkthrough artifacts modified: no.",
    ]:
        assert phrase in report

    assert "- [ ] Researcher records completed." in checklist
    assert "- [ ] Authoritative current Design B friction_locus manual frozen." in checklist
    assert "- [ ] Account-verified model and decoding parameters frozen." in checklist
    assert "- [ ] Run manifests populated." in checklist
