from pathlib import Path
import subprocess
import sys

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SEGMENTS_PATH = REPO_ROOT / "data" / "source_segments_demo.csv"
ANNOTATIONS_PATH = REPO_ROOT / "data" / "demo_annotations.csv"
EXAMPLE_PATH = REPO_ROOT / "examples" / "run_trim_with_source_segments.py"

REQUIRED_SEGMENT_FIELDS = {
    "segment_id",
    "case_id",
    "source",
    "language",
    "segment_order",
    "original_text",
    "translation_or_paraphrase",
    "location_note",
    "segment_note",
}


def test_source_segments_demo_exists():
    assert SEGMENTS_PATH.exists()


def test_source_segments_required_fields_present():
    segments = pd.read_csv(SEGMENTS_PATH, dtype=str, keep_default_na=False)
    assert REQUIRED_SEGMENT_FIELDS.issubset(segments.columns)


def test_source_segment_ids_are_unique():
    segments = pd.read_csv(SEGMENTS_PATH, dtype=str, keep_default_na=False)
    assert segments["segment_id"].is_unique


def test_source_segment_case_ids_match_demo_annotations():
    segments = pd.read_csv(SEGMENTS_PATH, dtype=str, keep_default_na=False)
    annotations = pd.read_csv(ANNOTATIONS_PATH, dtype=str, keep_default_na=False)
    assert set(segments["case_id"]).issubset(set(annotations["case_id"]))


def test_source_segment_example_script_exists():
    assert EXAMPLE_PATH.exists()


def test_source_segment_example_runs_directly(tmp_path):
    result = subprocess.run(
        [sys.executable, str(EXAMPLE_PATH)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "linked_annotations:" in result.stdout


def test_source_segment_linking_helper_updates_evidence_anchor():
    from examples.run_trim_with_source_segments import load_and_link_segments

    linked = load_and_link_segments(ANNOTATIONS_PATH, SEGMENTS_PATH)
    anchors = dict(zip(linked["case_id"], linked["evidence_anchor"]))
    assert anchors["GROVE_TAJOMARU"].startswith("GROVE_TAJOMARU_01:")
