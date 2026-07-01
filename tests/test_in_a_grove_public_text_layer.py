import csv
import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
PUBLIC = ROOT / "examples" / "in_a_grove_walkthrough_public_v0_2"
SEGMENTS = PUBLIC / "source_segments_japanese.csv"
GLOSS = PUBLIC / "english_gloss.csv"


EXPECTED_FILES = {
    "canonical_japanese_source.md",
    "source_segments_japanese.csv",
    "english_gloss.csv",
    "gloss_protocol.md",
    "source_provenance.md",
    "text_layer_review_status.md",
    "canonical_text_exactness_audit.md",
}

FORBIDDEN_ANNOTATION_ARTIFACTS = {
    "author_analytic_record.csv",
    "author_lock_manifest.csv",
    "ai_independent_record.csv",
    "ai_raw_output.txt",
    "model_run_manifest.csv",
    "prompt_manifest.csv",
    "outputs",
}

KOJIMA_ENGLISH_MARKERS = {
    "must look to myself",
    "grove",
    "robber",
    "dagger",
    "long sword",
    "blood",
    "afterlife",
}


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _segment_rows() -> list[dict[str, str]]:
    return _rows(SEGMENTS)


def _gloss_rows() -> list[dict[str, str]]:
    return _rows(GLOSS)


def _by_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["segment_id"]: row for row in rows}


def test_public_text_layer_structure_and_draft_boundary():
    assert PUBLIC.is_dir()
    assert {path.name for path in PUBLIC.iterdir()} == EXPECTED_FILES
    assert not any((PUBLIC / name).exists() for name in FORBIDDEN_ANNOTATION_ARTIFACTS)

    combined_status_text = "\n".join(
        _read(PUBLIC / name)
        for name in (
            "canonical_japanese_source.md",
            "gloss_protocol.md",
            "source_provenance.md",
            "text_layer_review_status.md",
        )
    )
    assert "draft_for_author_review" in combined_status_text
    assert "draft_text_layer_only" in combined_status_text
    assert "not_frozen" in combined_status_text
    assert "no_new_records_authorised" in combined_status_text


def test_canonical_japanese_segments_are_structural_and_canonical():
    rows = _segment_rows()
    ids = [row["segment_id"] for row in rows]
    orders = [int(row["segment_order"]) for row in rows]
    by_id = _by_id(rows)

    assert len(ids) == len(set(ids))
    assert ids.count("IAG-JP-FRAME-001") == 1
    assert [row["segment_id"] for row in rows if row["speaker"] != "source_heading"] == [
        f"IAG-JP-{index:03d}" for index in range(1, 22)
    ]
    assert len(orders) == len(set(orders))
    assert orders == sorted(orders)
    assert all(row["speaker"] == "dead_samurai_via_medium" for row in rows if row["segment_id"].startswith("IAG-JP-0"))
    assert by_id["IAG-JP-FRAME-001"]["speaker"] == "source_heading"
    assert all(row["included_in_packet"] == "yes" for row in rows)
    assert all("canonical evidence" in row["source_note"] for row in rows)
    assert all(row["canonical_japanese_text"].strip() for row in rows)
    assert not any(
        marker in row["canonical_japanese_text"].lower()
        for row in rows
        for marker in KOJIMA_ENGLISH_MARKERS
    )


def test_required_canonical_japanese_anchors_are_present():
    by_id = _by_id(_segment_rows())

    assert "巫女の口を借りたる死霊の物語" in by_id["IAG-JP-FRAME-001"]["canonical_japanese_text"]
    assert "らしい" in by_id["IAG-JP-002"]["canonical_japanese_text"]
    assert "いや" in by_id["IAG-JP-006"]["canonical_japanese_text"]
    assert "一突きにおれの胸へ刺した" in by_id["IAG-JP-011"]["canonical_japanese_text"]
    assert "腥い塊" in by_id["IAG-JP-012"]["canonical_japanese_text"]
    assert "誰か忍び足に" in by_id["IAG-JP-017"]["canonical_japanese_text"]
    assert "見えない手" in by_id["IAG-JP-019"]["canonical_japanese_text"]
    assert "もう一度血潮" in by_id["IAG-JP-020"]["canonical_japanese_text"]
    assert "中有の闇" in by_id["IAG-JP-021"]["canonical_japanese_text"]


def test_english_glosses_are_one_to_one_and_non_authoritative():
    segment_ids = {row["segment_id"] for row in _segment_rows()}
    glosses = _gloss_rows()
    gloss_ids = [row["segment_id"] for row in glosses]

    assert len(gloss_ids) == len(set(gloss_ids))
    assert set(gloss_ids) == segment_ids
    assert all(row["gloss_status"] == "non_authoritative" for row in glosses)
    assert all(row["english_gloss"].strip() for row in glosses)
    assert all(row["translation_note"].strip() for row in glosses)


def test_english_gloss_translation_decisions_remain_stable():
    by_id = _by_id(_gloss_rows())
    all_gloss_text = "\n".join(row["english_gloss"] for row in by_id.values())
    all_note_text = "\n".join(row["translation_note"] for row in by_id.values())

    assert "long sword" in by_id["IAG-JP-004"]["english_gloss"]
    assert "dagger" in by_id["IAG-JP-010"]["english_gloss"]
    assert "Now it is my turn." in by_id["IAG-JP-005"]["english_gloss"]
    assert "must look to myself" not in all_gloss_text
    assert "Some raw-smelling mass" in by_id["IAG-JP-012"]["english_gloss"]
    assert "raw smell of blood" not in by_id["IAG-JP-012"]["english_gloss"].lower()
    assert "Now I could no longer see" in by_id["IAG-JP-015"]["english_gloss"]
    assert re.search(r"\bsomeone\b", by_id["IAG-JP-017"]["english_gloss"], re.IGNORECASE)
    assert "a hand I could not see" in by_id["IAG-JP-019"]["english_gloss"]
    assert "supernatural" not in all_note_text.lower().replace("not necessarily supernatural", "")
    assert "chūu" in by_id["IAG-JP-021"]["english_gloss"]
    assert not by_id["IAG-JP-021"]["english_gloss"].strip().lower().endswith(
        ("death.", "afterlife.", "darkness.")
    )


def test_protocol_governance_for_future_records_and_review_boundary():
    protocol = _read(PUBLIC / "gloss_protocol.md")
    review = _read(PUBLIC / "text_layer_review_status.md")
    combined = protocol + "\n" + review

    assert "Japanese text is the only canonical evidence layer" in protocol
    assert "English gloss is an accessibility aid" in protocol
    assert "Annotation records must cite Japanese segment IDs" in protocol
    assert "segmentation was completed before any new author or model record" in protocol
    assert "must not be adjusted to reproduce an earlier disagreement" in protocol
    assert "distinguish `太刀` from `小刀`" in protocol
    assert "AI-assisted" in protocol
    assert "Zhiji Wang remains responsible" in protocol
    assert "does not authorise creation of a new author analytic record or AI record" in protocol
    assert "annotation_status: no_new_records_authorised" in review
    assert "ready_for_annotation: no" in combined


def test_source_provenance_and_rights_boundary_are_documented():
    provenance = _read(PUBLIC / "source_provenance.md")

    assert "Akutagawa Ryūnosuke" in provenance
    assert "Aozora Bunko" in provenance
    assert "https://www.aozora.gr.jp/cards/000879/files/179_15255.html" in provenance
    assert "First publication: *Shinchō*, January 1922" in provenance
    assert "Aozora base edition" in provenance
    assert "Takashi Kojima translation" in provenance
    assert "restricted development artifact" in provenance
    assert "access_date: pending_author_confirmation" in provenance
    assert "rights_evidence_status: usage_guidance_copy_required_before_public_release" in provenance
    assert "does not claim that GitHub hosting itself proves copyright permission" in provenance


def test_exactness_audit_records_passed_draft_check_without_freezing():
    audit = _read(PUBLIC / "canonical_text_exactness_audit.md")

    assert "exact_match_status: passed_draft_check" in audit
    assert "segments_checked: 22" in audit
    assert "corrections_made: none" in audit
    assert "remaining_manual_check: author_final_review_required_before_freeze" in audit
    assert not (PUBLIC / "source_manifest.csv").exists()
    assert not (PUBLIC / "gloss_manifest.csv").exists()
    assert not (PUBLIC / "SHA256SUMS.txt").exists()
    assert not (PUBLIC / "frozen_packet.zip").exists()
