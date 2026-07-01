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
WALK = ROOT / "walkthrough" / "in_a_grove_v0_1"
OUTPUTS = WALK / "outputs"
POSITION = ROOT / "position_note"
PACKAGE = ROOT / "artifacts" / "TRIM_HAA_position_note_v0_1.zip"
PACKAGE_SHA = ROOT / "artifacts" / "TRIM_HAA_position_note_v0_1.zip.sha256"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _run_walkthrough_and_package():
    subprocess.run([sys.executable, "scripts/run_in_a_grove_walkthrough.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/build_trim_haa_position_note_package.py"], cwd=ROOT, check=True)


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
    assert model_run["prompt_hash"] == prompt_manifest["prompt_sha256"]
    assert _sha256(WALK / model_run["output_file"]) == model_run["output_sha256"]
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
    assert "Display status: `candidate_visible`" in candidate
    assert "not an empirical classification or truth verdict" in candidate
    assert "truth_verdict" not in candidate
    assert "without deciding which interpretation is correct" in candidate


def test_position_note_layers_limitations_and_prohibited_wording():
    note = _read(POSITION / "TRIM_HAA_position_note_v0_1.md")
    lowered = note.lower()

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
    }
    for phrase in prohibited:
        assert phrase not in lowered


def test_claim_boundary_table_and_publication_blockers_exist():
    claims = _rows(POSITION / "TRIM_HAA_position_note_claim_boundaries.csv")
    blockers = _read(POSITION / "TRIM_HAA_position_note_publication_blockers.md")

    claim_names = {row["claim"] for row in claims}
    assert "Candidate mismatch can be displayed" in claim_names
    assert "Model is wrong" in claim_names
    assert "AI changes human judgment" in claim_names
    assert "copyright and translation review" in blockers.lower()
    assert "not publication-ready" in blockers


def test_position_note_package_builds_deterministically_and_contains_expected_files():
    _run_walkthrough_and_package()
    before = _sha256(PACKAGE)
    subprocess.run([sys.executable, "scripts/build_trim_haa_position_note_package.py"], cwd=ROOT, check=True)
    after = _sha256(PACKAGE)

    assert after == before
    assert PACKAGE_SHA.read_text(encoding="utf-8").split()[0] == after

    manifest = _rows(POSITION / "TRIM_HAA_position_note_v0_1_manifest.csv")
    for row in manifest:
        assert _sha256(ROOT / row["artifact"]) == row["sha256"]

    with zipfile.ZipFile(PACKAGE) as archive:
        names = set(archive.namelist())

    assert "position_note/TRIM_HAA_position_note_v0_1.md" in names
    assert "walkthrough/in_a_grove_v0_1/source_segments.csv" in names
    assert "walkthrough/in_a_grove_v0_1/ai_raw_output.txt" in names
    assert not any(name.startswith("dry_runs/") for name in names)
