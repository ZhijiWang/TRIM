import csv
import hashlib
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

from trim_haa.locking import verify_locked_annotation
from trim_haa.schema import TrimHAAAnnotation
from trim_haa.validator import validate_core_record


ROOT = Path(__file__).parents[1]
WALK = ROOT / "examples" / "in_a_grove_walkthrough"
OUTPUTS = WALK / "outputs"
POSITION = ROOT / "research" / "position_note"
PACKAGE = ROOT / "artifacts" / "position_note" / "TRIM_HAA_position_note_v0_1.zip"
PACKAGE_SHA = ROOT / "artifacts" / "position_note" / "TRIM_HAA_position_note_v0_1.zip.sha256"
PACKAGE_V02 = ROOT / "artifacts" / "position_note" / "TRIM_HAA_position_note_v0_2.zip"
PACKAGE_V02_SHA = ROOT / "artifacts" / "position_note" / "TRIM_HAA_position_note_v0_2.zip.sha256"
EXPECTED_V01_PACKAGE_SHA = "eae1c50f329a70fba02640aa07475b2fd985eaafaf2ac17bbe69630427c83433"
EXPECTED_V02_PACKAGE_SHA = "cc734bff299a3193f6467c494b560a87ae35c5ed3de25a26457de878e1d4d94e"
EXPECTED_AUTHOR_RECORD_SHA = "8155a280880f9fda1035f1b3790f7dbd2932db0b07de940bf9c023cb3ab86871"
EXPECTED_AI_RAW_OUTPUT_SHA = "343b9858e3fc9c89840be68542e2ad1aa8b389f8841a86db9c9ceaec48a149a2"
EXPECTED_PROMPT_SHA = "74af647ec15697e99bd87ee4c4fdbfecfd402ff09cc76dc8acf55e3bf856e8f5"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _run_walkthrough_and_package():
    subprocess.run([sys.executable, "scripts/run_in_a_grove_walkthrough.py"], cwd=ROOT, check=True)


def test_source_packet_provenance_and_legal_review_exist():
    assert (WALK / "source_packet.md").exists()
    assert (WALK / "source_provenance.md").exists()
    assert (WALK / "legal_and_translation_review.md").exists()

    provenance = _read(WALK / "source_provenance.md")
    legal = _read(WALK / "legal_and_translation_review.md")

    assert "Takashi Kojima" in provenance
    assert "https://en.wikisource.org/wiki/Rashomon_and_Other_Stories/In_a_Grove" in provenance
    assert "not publication-ready" in legal
    assert "translation" in legal.lower()


def test_source_segments_have_stable_ids_and_no_interpretive_stage_records():
    rows = _rows(WALK / "source_segments.csv")
    ids = [row["segment_id"] for row in rows]

    assert len(rows) >= 10
    assert len(ids) == len(set(ids))
    assert ids[0] == "IAG-MED-001"
    assert all(segment_id.startswith("IAG-") for segment_id in ids)
    assert all(row["case_id"] == "IAG_MEDIUM_001" for row in rows)


def test_author_record_is_locked_before_ai_record_timestamp_and_verifies():
    _run_walkthrough_and_package()
    author = TrimHAAAnnotation.from_record(_rows(WALK / "author_analytic_record.csv")[0])
    lock = _rows(WALK / "author_lock_manifest.csv")[0]
    model_run = _rows(WALK / "model_run_manifest.csv")[0]

    assert author.annotation_stage == "human_pre"
    assert author.actor_id == "AUTHOR_ANALYTIC"
    assert verify_locked_annotation(author, lock)
    assert "researcher-produced analytic demonstration; not human-subject data and not a gold standard" in lock["notes"]

    locked_at = datetime.fromisoformat(lock["locked_at"])
    run_timestamp = datetime.fromisoformat(model_run["run_timestamp"])
    assert locked_at < run_timestamp


def test_prompt_and_ai_output_hashes_match_manifests_and_ai_record_validates():
    _run_walkthrough_and_package()
    prompt_manifest = _rows(WALK / "prompt_manifest.csv")[0]
    model_run = _rows(WALK / "model_run_manifest.csv")[0]
    ai_record = TrimHAAAnnotation.from_record(_rows(WALK / "ai_independent_record.csv")[0])

    assert _sha256(WALK / prompt_manifest["prompt_text_path"]) == prompt_manifest["prompt_sha256"]
    assert prompt_manifest["prompt_sha256"] == EXPECTED_PROMPT_SHA
    assert model_run["prompt_hash"] == prompt_manifest["prompt_sha256"]
    assert _sha256(WALK / model_run["output_file"]) == model_run["output_sha256"]
    assert model_run["output_sha256"] == EXPECTED_AI_RAW_OUTPUT_SHA
    assert model_run["system_prompt_hash"] == "unavailable"
    assert model_run["temperature_or_sampling"] == "unavailable"
    assert model_run["provider"] == "OpenAI"
    assert model_run["model_name"] == "Codex session model"
    assert model_run["model_version_or_date"] == "2026-07-01"
    assert "locally auditable but not externally reproducible" in model_run["notes"]
    assert model_run["retry_count"] == "0"
    assert ai_record.annotation_stage == "ai_independent"
    assert ai_record.actor_type == "model"
    assert not validate_core_record(ai_record)


def test_no_human_post_control_or_participant_records_exist():
    records = []
    for path in (WALK / "author_analytic_record.csv", WALK / "ai_independent_record.csv"):
        records.extend(_rows(path))

    stages = {row["annotation_stage"] for row in records}
    actor_ids = {row["actor_id"] for row in records}

    assert "human_post_ai" not in stages
    assert "human_second_pass_control" not in stages
    assert "adjudicated" not in stages
    assert not any(actor_id.startswith(("P", "H01", "H02")) for actor_id in actor_ids)


def test_comparison_outputs_are_deterministic_and_candidate_has_no_truth_verdict():
    _run_walkthrough_and_package()
    before = {
        path.name: _sha256(path)
        for path in sorted(OUTPUTS.glob("*"))
        if path.is_file()
    }
    subprocess.run([sys.executable, "scripts/run_in_a_grove_walkthrough.py"], cwd=ROOT, check=True)
    after = {
        path.name: _sha256(path)
        for path in sorted(OUTPUTS.glob("*"))
        if path.is_file()
    }

    assert after == before
    candidate = _read(OUTPUTS / "candidate_certainty_alternative_mismatch.md")
    summary = _read(OUTPUTS / "execution_summary.md")
    field_rows = _rows(OUTPUTS / "field_comparison.csv")

    assert "# Review Question Generated: Candidate Certainty-Closure Tension" in candidate
    assert "Display status: `candidate_visible`" in candidate
    assert "configured author-defined review condition was satisfied" in candidate
    assert "not an adjudicated property of the model record" in candidate
    assert "does not prove that an alternative interpretation is required" in candidate
    assert "does not prove that low uncertainty is inappropriate" in candidate
    assert "does not prove model error" in candidate
    assert "does not prove overconfidence" in candidate
    assert "It generates a review question" in candidate
    assert "cannot be attributed to missing input or a missing response field" in candidate
    assert "whether IAG-SAM-012 warranted retaining an alternative remains open" in candidate
    assert "does not automatically establish that someone else caused the death" in candidate
    assert "self-inflicted death and unresolved later intervention may coexist" in candidate
    assert "truth_verdict" not in candidate
    assert "without deciding which interpretation is correct" in candidate

    assert "structured disagreement across final label, selected evidence, mechanism, uncertainty, and alternative handling" in summary
    assert "author-defined review rule was triggered; it is not an independently validated mismatch" in summary
    claim_rows = {row["field"]: row for row in field_rows}
    assert claim_rows["walkthrough_result"]["same"] == "False"
    assert "structured disagreement" in claim_rows["walkthrough_result"]["author_value"]
    assert "author-defined review-rule trigger" in claim_rows["candidate_status_interpretation"]["ai_value"]


def test_position_note_claim_hardening_and_design_dependence():
    note = _read(POSITION / "TRIM_HAA_position_note_v0_1.md")
    lowered = note.lower()

    assert "Final labels flatten the structure of both agreement and disagreement" in note
    assert "A final-label comparison identifies disagreement but does not preserve its structure" in note
    assert "current walkthrough directly demonstrates disagreement flattening" in lowered
    assert "does not empirically demonstrate same-label hidden divergence" in lowered
    assert "same-label divergence remains a general motivation" in lowered
    assert "Design Dependence of the Walkthrough" in note
    assert "source packet was selected by the author" in note
    assert "Segmentation was author-designed" in note
    assert "case-specific label vocabulary was author-designed" in note
    assert "mechanism vocabulary was author-designed" in note
    assert "packet and codebook were theory-informed" in note
    assert "does not show that the instrument independently discovered a naturally given mismatch" in note
    assert "Representation Is Not Detection" in note
    assert "does not establish a validated detection rule" in note
    assert "An author-defined flag is not an adjudication" in note
    assert "candidate_visible` is a walkthrough display status" in note
    assert "configured review condition was satisfied" in note
    assert "does not establish that the packet objectively contains a competing causal account" in note
    assert "does not automatically establish that someone else caused the death" in note
    assert "Self-inflicted death and unresolved later intervention may coexist" in note
    assert "breadth and closure of the submitted record" in note
    assert "Segment `IAG-SAM-012` was present in the packet" in note
    assert "cannot be attributed to missing input or a missing response field" in note
    assert "Whether that segment warranted retaining an alternative remains open" in note
    assert "locally auditable but not externally reproducible" in note
    assert "Wikisource hosting is not proof" in note
    assert "same-label/different-pathway case would directly demonstrate agreement flattening" in note

    assert "independent record audit" in note
    assert "exposure audit" in note
    assert "demonstrates only the independent-record layer" in note
    assert "no human-subject evidence" in lowered
    assert "no reliability estimate" in lowered
    assert "researcher-produced analytic demonstration; not human-subject data and not a gold standard" in note
    assert "copyright and translation review" in lowered
    assert "prompt hash" in lowered
    assert "model-run manifest" in lowered

    prohibited = {
        "fluent-but-wrong",
        "model failure",
        "ai improved annotation",
        "agreement proves quality",
        "trım-haa is validated",
        "trim-haa is validated",
        "causal exposure result is shown",
        "human record is the gold standard",
        "collaborative annotation optimisation",
        "true certainty-alternative mismatch was detected",
        "true mismatch was established",
        "model ignored decisive evidence",
        "model suppressed a valid alternative",
    }
    for phrase in prohibited:
        assert phrase not in lowered


def test_claim_boundary_table_and_publication_blockers_exist():
    claims = _rows(POSITION / "TRIM_HAA_position_note_claim_boundaries.csv")
    blockers = _read(POSITION / "TRIM_HAA_position_note_publication_blockers.md")

    claim_names = {row["claim"] for row in claims}
    claim_map = {row["claim"]: row for row in claims}
    assert "The walkthrough demonstrates structured disagreement" in claim_names
    assert claim_map["The walkthrough demonstrates structured disagreement"]["supported_by_walkthrough"] == "supported"
    assert claim_map["The walkthrough demonstrates same-label hidden divergence"]["supported_by_walkthrough"] == "not demonstrated by this case"
    assert claim_map["The review rule was triggered"]["supported_by_walkthrough"] == "supported"
    assert claim_map["A true certainty-alternative mismatch was established"]["supported_by_walkthrough"] == "unsupported"
    assert claim_map["The model omitted an alternative despite receiving the relevant segment and field"]["supported_by_walkthrough"] == "supported"
    assert claim_map["The segment objectively required an alternative"]["supported_by_walkthrough"] == "requires independent evaluation"
    assert claim_map["The model artifact is locally auditable"]["supported_by_walkthrough"] == "supported"
    assert claim_map["The model run is externally reproducible"]["supported_by_walkthrough"] == "unsupported"
    assert claim_map["The walkthrough validates a detector"]["supported_by_walkthrough"] == "unsupported"
    assert claim_map["The walkthrough demonstrates representational feasibility"]["supported_by_walkthrough"] == "supported"
    assert "Model is wrong" in claim_names
    assert "AI changes human judgment" in claim_names
    assert "copyright and translation review" in blockers.lower()
    assert "not publication-ready" in blockers
    assert "non-reproducible development demonstration" in blockers
    assert "same-label/different-pathway case would directly demonstrate agreement flattening" in blockers


def test_raw_records_prompt_and_v01_package_remain_unchanged():
    assert _sha256(WALK / "author_analytic_record.csv") == EXPECTED_AUTHOR_RECORD_SHA
    assert _sha256(WALK / "ai_raw_output.txt") == EXPECTED_AI_RAW_OUTPUT_SHA
    assert _sha256(WALK / "prompts" / "in_a_grove_trim_haa_v0_1.txt") == EXPECTED_PROMPT_SHA
    assert _sha256(PACKAGE) == EXPECTED_V01_PACKAGE_SHA
    assert PACKAGE_SHA.read_text(encoding="utf-8").split()[0] == EXPECTED_V01_PACKAGE_SHA


def test_no_new_walkthrough_case_or_exposure_records_added():
    walkthrough_dirs = [
        path
        for path in (ROOT / "examples").iterdir()
        if path.is_dir() and path.name.startswith("in_a_grove")
    ]
    assert {path.name for path in walkthrough_dirs} == {
        "in_a_grove_walkthrough",
        "in_a_grove_walkthrough_public_v0_2",
    }

    public_text_layer = ROOT / "examples" / "in_a_grove_walkthrough_public_v0_2"
    forbidden_public_artifacts = {
        "author_analytic_record.csv",
        "author_lock_manifest.csv",
        "ai_independent_record.csv",
        "ai_raw_output.txt",
        "model_run_manifest.csv",
        "prompt_manifest.csv",
        "outputs",
    }
    assert not any((public_text_layer / name).exists() for name in forbidden_public_artifacts)

    all_csv_rows = []
    for path in WALK.glob("*.csv"):
        all_csv_rows.extend(_rows(path))
    stages = {row.get("annotation_stage", "") for row in all_csv_rows}
    assert "human_post_ai" not in stages
    assert "human_second_pass_control" not in stages
    assert "control" not in stages


def test_python_311_and_312_ci_matrix_is_declared():
    workflow = _read(ROOT / ".github" / "workflows" / "tests.yml")
    pyproject = _read(ROOT / "pyproject.toml")

    assert 'python-version: ["3.11", "3.12"]' in workflow
    assert 'requires-python = ">=3.11"' in pyproject


def test_review_response_memo_exists():
    memo = _read(POSITION / "TRIM_HAA_position_note_v0_1_review_response.md")

    assert "Concern 1: The case does not demonstrate same-label flattening" in memo
    assert "current walkthrough demonstrates disagreement flattening" in memo
    assert "No post hoc case was added" in memo
    assert "Concern 2: The candidate alternative is theory-led" in memo
    assert "Concern 3: Representability is not detection" in memo
    assert "Concern 4: IAG-SAM-012 may not reopen cause of death" in memo
    assert "Concern 5: Model provenance is insufficient for external reproduction" in memo


def test_position_note_package_v02_is_preserved_and_contains_expected_files():
    assert _sha256(PACKAGE) == EXPECTED_V01_PACKAGE_SHA
    assert PACKAGE_SHA.read_text(encoding="utf-8").split()[0] == EXPECTED_V01_PACKAGE_SHA
    assert _sha256(PACKAGE_V02) == EXPECTED_V02_PACKAGE_SHA
    assert PACKAGE_V02_SHA.read_text(encoding="utf-8").split()[0] == EXPECTED_V02_PACKAGE_SHA

    with zipfile.ZipFile(PACKAGE_V02) as archive:
        names = set(archive.namelist())

    assert "position_note/TRIM_HAA_position_note_v0_1.md" in names
    assert "position_note/TRIM_HAA_position_note_v0_1_review_response.md" in names
    assert "position_note/TRIM_HAA_position_note_v0_2_manifest.csv" in names
    assert "walkthrough/in_a_grove_v0_1/source_segments.csv" in names
    assert "walkthrough/in_a_grove_v0_1/author_analytic_record.csv" in names
    assert "walkthrough/in_a_grove_v0_1/author_lock_manifest.csv" in names
    assert "walkthrough/in_a_grove_v0_1/ai_raw_output.txt" in names
    assert "walkthrough/in_a_grove_v0_1/ai_independent_record.csv" in names
    assert "walkthrough/in_a_grove_v0_1/outputs/candidate_certainty_alternative_mismatch.md" in names
    assert "walkthrough/in_a_grove_v0_1/outputs/field_comparison.csv" in names
    assert not any(name.startswith("dry_runs/") for name in names)
