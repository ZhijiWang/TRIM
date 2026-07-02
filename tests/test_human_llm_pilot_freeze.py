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

    selected_ids = sample["selected_case_ids"]
    assert len(selected_ids) == 25
    assert len(set(selected_ids)) == 25
    assert sum(1 for layer in sample["layer_assignments"].values() if layer == "Layer 1") == 15
    assert sum(1 for layer in sample["layer_assignments"].values() if layer == "Layer 2") == 10
    assert {row["case_id"] for row in source_rows} == set(selected_ids)

    selected_rows = [row for row in selection_rows if row["inclusion_status"] == "selected"]
    assert len(selected_rows) == 25
    assert all(row["prior_demo_use"] == "no" for row in selected_rows)
    assert all(row["prior_manual_use"] == "no" for row in selected_rows)
    assert all(row["manual_development_influence"] != "direct" for row in selected_rows)
    assert all("no friction_locus labels" in row["label_information_visible_at_selection"] for row in selected_rows)
    assert all("unclear" not in row["rights_status"] for row in selected_rows)


def test_source_packets_are_non_empirical_and_identical_for_human_and_model():
    forbidden = {
        "expected_label",
        "friction_locus",
        "manual_hint",
        "model_output",
        "primary_label",
        "researcher_interpretation",
        "secondary_scholarship",
    }
    for packet_path in sorted((DATA_DIR / "source_packets").glob("*.json")):
        packet = load_json(packet_path)
        assert not (forbidden & set(packet)), packet_path.name
        assert packet["text_layer_visibility"]["researcher_and_model_identical"] is True
        assert packet["text_layer_visibility"]["secondary_scholarship_visible"] is False
        assert packet["text_layer_visibility"]["model_facing_instructions_included"] is False
        assert packet["segments"]
        assert all(segment["evidence_id"] for segment in packet["segments"])


def test_manual_prompt_and_schema_hashes_match_frozen_files():
    manual = load_json(DATA_DIR / "manual_freeze_manifest.json")
    prompts = load_json(DATA_DIR / "prompt_bundle_manifest.json")

    assert manual["repository_commit"] == "6998175eeca5d349072bf31012c69f2d568f28ec"
    assert sha256(ROOT / manual["manual_path"]) == manual["manual_file_hash"]
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


def test_prompts_freeze_only_instruction_exposure_difference():
    system_prompt = (ROOT / "prompts" / "human_llm_pilot" / "system_prompt.txt").read_text(encoding="utf-8")
    user_template = (ROOT / "prompts" / "human_llm_pilot" / "user_prompt_template.txt").read_text(encoding="utf-8")
    condition_a = (ROOT / "prompts" / "human_llm_pilot" / "condition_A.txt").read_text(encoding="utf-8")
    condition_b = (ROOT / "prompts" / "human_llm_pilot" / "condition_B.txt").read_text(encoding="utf-8")
    condition_c = (ROOT / "prompts" / "human_llm_pilot" / "condition_C.txt").read_text(encoding="utf-8")

    assert "not a truth verdict" in system_prompt
    assert "Do not browse, use tools" in system_prompt
    assert "{{CASE_ID}}" in user_template
    assert "{{SOURCE_PACKET}}" in user_template
    assert "{{OUTPUT_SCHEMA}}" in user_template
    assert "label names and short definitions only" in condition_a
    assert "concise decision rules" in condition_b
    assert "full manual condition" in condition_c
    assert "Frozen counterfactual-test and confusable-with guidance" in condition_c
    assert "cue_function -> operation_function" in condition_c


def test_allocation_governance_and_non_execution_status():
    allocation = load_json(DATA_DIR / "allocation_manifest.json")
    governance = load_json(DATA_DIR / "governance_status.json")
    model_spec = load_json(DATA_DIR / "model_execution_spec.json")
    report = (DOCS_DIR / "human_llm_pilot_freeze_report.md").read_text(encoding="utf-8")
    checklist = (DOCS_DIR / "human_llm_protocol_freeze_checklist.md").read_text(encoding="utf-8")

    assert allocation["second_human_component"] == "not_in_current_protocol"
    assert "No model execution before human lock" in allocation["condition_assignment"]["visibility_constraints"]
    assert allocation["model_stability_run_count"] == 3
    assert len(allocation["ablation_subset"]) == 6
    assert governance["protocol_design"] == "Design B"
    assert governance["external_human_recruitment"] == "prohibited"
    assert governance["participant_data_collection"] == "none"
    assert governance["formal_ethics_exemption_claimed"] is False
    assert model_spec["provider"] == "OpenAI"
    assert model_spec["model"] == "gpt-5.4-mini"
    assert model_spec["browsing"] == "disabled"
    assert model_spec["tools"] == "disabled"

    for phrase in [
        "Human coding occurred: no.",
        "Model called: no.",
        "Model outputs created: no.",
        "Findings generated: no.",
        "Released walkthrough artifacts modified: no.",
    ]:
        assert phrase in report

    assert "- [ ] Researcher records completed." in checklist
    assert "- [ ] Run manifests populated." in checklist
    assert "- [ ] Raw-output hashes computed immediately after receipt." in checklist
