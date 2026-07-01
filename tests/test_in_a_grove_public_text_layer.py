import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).parents[1]
PUBLIC = ROOT / "examples" / "in_a_grove_walkthrough_public_v0_2"

EXPECTED_FILES = {
    "canonical_japanese_source.md",
    "source_segments_japanese.csv",
    "english_gloss.csv",
    "gloss_protocol.md",
    "source_provenance.md",
    "text_layer_review_status.md",
    "canonical_text_exactness_audit.md",
    "aozora_usage_guidance_record.md",
    "source_manifest.csv",
    "gloss_manifest.csv",
    "SHA256SUMS.txt",
}

FORBIDDEN = {
    "author_analytic_record.csv",
    "author_lock_manifest.csv",
    "ai_independent_record.csv",
    "ai_raw_output.txt",
    "model_run_manifest.csv",
    "prompt_manifest.csv",
    "outputs",
    "frozen_packet.zip",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_frozen_text_layer_structure():
    assert PUBLIC.is_dir()
    assert {path.name for path in PUBLIC.iterdir()} == EXPECTED_FILES
    assert not any((PUBLIC / name).exists() for name in FORBIDDEN)

    status = _read(PUBLIC / "text_layer_review_status.md")
    assert "review_status: author_review_completed" in status
    assert "freeze_status: frozen_text_layer_v0_2" in status
    assert "annotation_status: ready_for_new_author_record_only" in status
    assert "ready_for_new_ai_record: no" in status
    assert "ready_for_public_release: no" in status


def test_segments_and_glosses_match_one_to_one():
    segments = _rows(PUBLIC / "source_segments_japanese.csv")
    glosses = _rows(PUBLIC / "english_gloss.csv")
    segment_ids = [row["segment_id"] for row in segments]
    gloss_ids = [row["segment_id"] for row in glosses]

    assert segment_ids[0] == "IAG-JP-FRAME-001"
    assert segment_ids[1:] == [f"IAG-JP-{index:03d}" for index in range(1, 22)]
    assert len(segment_ids) == len(set(segment_ids)) == 22
    assert set(segment_ids) == set(gloss_ids)
    assert len(gloss_ids) == len(set(gloss_ids))
    assert all(row["canonical_japanese_text"].strip() for row in segments)
    assert all(row["gloss_status"] == "non_authoritative" for row in glosses)
    assert all(row["english_gloss"].strip() for row in glosses)
    assert all(row["translation_note"].strip() for row in glosses)


def test_protocol_and_rights_boundary():
    protocol = _read(PUBLIC / "gloss_protocol.md")
    provenance = _read(PUBLIC / "source_provenance.md")
    rights = _read(PUBLIC / "aozora_usage_guidance_record.md")

    assert "Japanese text is the only canonical evidence layer" in protocol
    assert "English gloss is an accessibility aid" in protocol
    assert "Annotation records must cite Japanese segment IDs" in protocol
    assert "A new author analytic record may now be created" in protocol
    assert "A new AI record may not be created until the author record has been completed and locked" in protocol

    assert "access_date: 2026-07-01" in provenance
    assert "official_usage_guidance_reviewed_and_recorded" in provenance
    assert "does not redistribute the Takashi Kojima translation" in provenance
    assert "does not claim that GitHub hosting itself proves copyright permission" in provenance
    assert "Access date: 2026-07-01" in rights
    assert "not legal advice" in rights


def test_exactness_audit_is_frozen():
    audit = _read(PUBLIC / "canonical_text_exactness_audit.md")
    assert "segments_checked: 22" in audit
    assert "exact_match_status: passed_author_reviewed_check" in audit
    assert "corrections_made: none" in audit
    assert "remaining_manual_check: none_for_text_layer_v0_2" in audit


def test_manifests_and_sha256s_match():
    manifest_rows = _rows(PUBLIC / "source_manifest.csv") + _rows(PUBLIC / "gloss_manifest.csv")
    expected = {row["file"]: row["sha256"] for row in manifest_rows}

    assert len(expected) == 8
    assert all(row["freeze_version"] == "text_layer_v0_2" for row in manifest_rows)
    assert all(row["freeze_date"] == "2026-07-01" for row in manifest_rows)
    assert all(row["status"] == "frozen" for row in manifest_rows)

    for filename, digest in expected.items():
        assert _sha256(PUBLIC / filename) == digest

    sums = {}
    for line in _read(PUBLIC / "SHA256SUMS.txt").splitlines():
        digest, filename = line.split("  ", 1)
        sums[filename] = digest
    assert sums == expected
