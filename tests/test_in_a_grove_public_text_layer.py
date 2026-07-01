import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PUBLIC = ROOT / "examples" / "in_a_grove_walkthrough_public_v0_2"
AUTHOR = PUBLIC / "author_record_v0_1"

EXPECTED_ROOT = {
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
    "author_record_validation_report.md",
    "author_record_v0_1",
}
FORBIDDEN_AI = {
    "ai_independent_record.csv",
    "ai_raw_output.txt",
    "model_run_manifest.csv",
    "prompt_manifest.csv",
    "outputs",
}
CORE_FIELDS = [
    "annotation_id","case_id","parent_annotation_id","actor_id","actor_type",
    "annotation_stage","primary_evidence_segment_ids","function_label",
    "rationale_mechanism","uncertainty_flag","rationale_note",
    "alternative_pathway_present","alternative_mechanism","alternative_note","status",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_public_v02_structure_and_ai_boundary():
    assert {path.name for path in PUBLIC.iterdir()} == EXPECTED_ROOT
    assert AUTHOR.is_dir()
    assert {path.name for path in AUTHOR.iterdir()} == {
        "author_analytic_record.csv",
        "author_lock_manifest.csv",
    }
    assert not any((PUBLIC / name).exists() for name in FORBIDDEN_AI)


def test_segments_and_glosses_match_one_to_one():
    segments = _rows(PUBLIC / "source_segments_japanese.csv")
    glosses = _rows(PUBLIC / "english_gloss.csv")
    segment_ids = [row["segment_id"] for row in segments]
    gloss_ids = [row["segment_id"] for row in glosses]
    assert segment_ids[0] == "IAG-JP-FRAME-001"
    assert segment_ids[1:] == [f"IAG-JP-{index:03d}" for index in range(1, 22)]
    assert len(segment_ids) == len(set(segment_ids)) == 22
    assert set(segment_ids) == set(gloss_ids)
    assert all(row["gloss_status"] == "non_authoritative" for row in glosses)


def test_locked_author_record_verifies():
    record = _rows(AUTHOR / "author_analytic_record.csv")[0]
    lock = _rows(AUTHOR / "author_lock_manifest.csv")[0]
    assert record["annotation_id"] == "IAG_JP_V02_AUTHOR_PRE"
    assert record["case_id"] == "IAG_JP_PUBLIC_002"
    assert record["actor_type"] == "human"
    assert record["annotation_stage"] == "human_pre"
    assert record["parent_annotation_id"] == ""
    assert record["status"] == "locked"
    assert record["uncertainty_flag"] == "high"
    assert record["alternative_pathway_present"] == "yes"
    assert set(record["primary_evidence_segment_ids"].split("|")) == {
        "IAG-JP-FRAME-001","IAG-JP-017","IAG-JP-018","IAG-JP-019","IAG-JP-020"
    }
    payload = json.dumps(
        {field: record[field].strip().replace("\r\n", "\n").replace("\r", "\n") for field in CORE_FIELDS},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=False,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    assert digest == lock["canonical_record_sha256"]
    assert digest == "6d78fd9d161d7a11c23ce962b257864eda16801793c6d87f17466e99ef269c50"
    assert lock["lock_status"] == "locked"


def test_author_claim_boundary():
    record = _rows(AUTHOR / "author_analytic_record.csv")[0]
    assert "third party contributed to or completed the death" in record["rationale_note"]
    assert "does not establish the medium's motive" in record["rationale_note"]
    assert "not treated as a supported conclusion" in record["rationale_note"]
    assert record["alternative_mechanism"] == "self_inflicted_injury_with_post_injury_intervention"


def test_text_layer_manifests_remain_valid():
    rows = _rows(PUBLIC / "source_manifest.csv") + _rows(PUBLIC / "gloss_manifest.csv")
    expected = {row["file"]: row["sha256"] for row in rows}
    for filename, digest in expected.items():
        assert _sha256(PUBLIC / filename) == digest
    sums = {}
    for line in _read(PUBLIC / "SHA256SUMS.txt").splitlines():
        digest, filename = line.split("  ", 1)
        sums[filename] = digest
    assert sums == expected
