import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PUBLIC = ROOT / "examples" / "in_a_grove_walkthrough_public_v0_2"
AUTHOR = PUBLIC / "author_record_v0_1"
AI_RUN = PUBLIC / "ai_run_v0_1"
EXPECTED_PROMPT_SHA = "7da94b590e7fca93927a59351936a4796b9828b7d7a2e106800fc1bcc240eca5"

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
    "ai_run_v0_1",
}
EXPECTED_AI_RUN = {
    "prompt.txt",
    "prompt_manifest.csv",
    "ai_record_template.csv",
    "run_protocol.md",
    "model_run_manifest_template.csv",
    "AI_RUN_SHA256SUMS.txt",
}
FORBIDDEN_ROOT_AI = {
    "ai_independent_record.csv",
    "ai_raw_output.txt",
    "model_run_manifest.csv",
    "prompt_manifest.csv",
    "prompts",
    "outputs",
    "comparison",
    "exposure_events.csv",
    "assistance_provenance.csv",
    "frozen_packet.zip",
}
FORBIDDEN_ACTUAL_AI = FORBIDDEN_ROOT_AI - {"prompt_manifest.csv"}
FORBIDDEN_STAGES = {
    "ai_independent",
    "human_post_ai",
    "human_second_pass_control",
    "adjudicated",
}
POSITION_NOTE_HASHES = {
    "TRIM_HAA_position_note_v0_1.md": "c811ca886907050491c452fa4657102c88b863db3da9cc76b2049cca893d340d",
    "TRIM_HAA_position_note_claim_boundaries.csv": "c572304686435fa73596b136aa5cea78f28fa9f7527de64cd0295fcf99188b87",
    "TRIM_HAA_position_note_publication_blockers.md": "2649d4ca0378f37f131bf4b0539ef66c69a88d18234638f4ccc9b00cf597b8e9",
    "TRIM_HAA_position_note_v0_1_review_response.md": "2aed11ddba63d60ab51d4a5b2c0fcac0136c272ce506d392d07429396ffd65f5",
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
    assert AI_RUN.is_dir()
    assert {path.name for path in AI_RUN.iterdir()} == EXPECTED_AI_RUN
    assert not any((PUBLIC / name).exists() for name in FORBIDDEN_ROOT_AI)
    assert not [
        path
        for name in FORBIDDEN_ACTUAL_AI
        for path in PUBLIC.glob(f"**/{name}")
    ]

    for csv_path in PUBLIC.glob("**/*.csv"):
        if csv_path == AI_RUN / "ai_record_template.csv":
            continue
        for row in _rows(csv_path):
            assert row.get("annotation_stage", "") not in FORBIDDEN_STAGES


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
    segment_ids = {
        row["segment_id"] for row in _rows(PUBLIC / "source_segments_japanese.csv")
    }
    evidence_ids = record["primary_evidence_segment_ids"].split("|")

    assert record["annotation_id"] == "IAG_JP_V02_AUTHOR_PRE"
    assert record["case_id"] == "IAG_JP_PUBLIC_002"
    assert record["actor_id"] == "AUTHOR_ANALYTIC"
    assert record["actor_type"] == "human"
    assert record["annotation_stage"] == "human_pre"
    assert record["parent_annotation_id"] == ""
    assert record["status"] == "locked"
    assert record["uncertainty_flag"] == "high"
    assert record["alternative_pathway_present"] == "yes"
    assert evidence_ids == [
        "IAG-JP-FRAME-001",
        "IAG-JP-017",
        "IAG-JP-018",
        "IAG-JP-019",
        "IAG-JP-020",
    ]
    assert set(evidence_ids) == {
        "IAG-JP-FRAME-001","IAG-JP-017","IAG-JP-018","IAG-JP-019","IAG-JP-020"
    }
    assert set(evidence_ids).issubset(segment_ids)
    payload = json.dumps(
        {field: record[field].strip().replace("\r\n", "\n").replace("\r", "\n") for field in CORE_FIELDS},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=False,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    assert digest == lock["canonical_record_sha256"]
    assert digest == "6d78fd9d161d7a11c23ce962b257864eda16801793c6d87f17466e99ef269c50"
    assert lock["annotation_id"] == record["annotation_id"]
    assert lock["case_id"] == record["case_id"]
    assert lock["annotation_stage"] == record["annotation_stage"]
    assert lock["actor_id"] == record["actor_id"]
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


def test_review_status_tracks_locked_author_record_and_ai_boundary():
    status = _read(PUBLIC / "text_layer_review_status.md")

    assert "freeze_status: frozen_text_layer_v0_2" in status
    assert "author_record_status: completed_and_locked" in status
    assert "ai_prompt_run_infrastructure_frozen: yes" in status
    assert "ai_run_executed: no" in status
    assert "ready_for_ai_run: yes" in status
    assert "ready_for_new_ai_record: yes" in status
    assert "ready_for_public_release: no" in status
    assert "does not claim that an AI record exists" in status
    assert "does not claim that a comparison has been completed" in status


def test_ai_run_infrastructure_is_frozen_without_execution():
    prompt = _read(AI_RUN / "prompt.txt")
    prompt_manifest = _rows(AI_RUN / "prompt_manifest.csv")[0]
    model_template = _rows(AI_RUN / "model_run_manifest_template.csv")[0]
    ai_template = _rows(AI_RUN / "ai_record_template.csv")[0]
    protocol = _read(AI_RUN / "run_protocol.md")

    assert _sha256(AI_RUN / "prompt.txt") == EXPECTED_PROMPT_SHA
    assert prompt_manifest["prompt_sha256"] == EXPECTED_PROMPT_SHA
    assert prompt_manifest["prompt_path"] == "examples/in_a_grove_walkthrough_public_v0_2/ai_run_v0_1/prompt.txt"
    assert _sha256(ROOT / prompt_manifest["prompt_path"]) == prompt_manifest["prompt_sha256"]
    assert "Japanese text is the only canonical evidence layer" in prompt
    assert "English gloss is provided only as an accessibility aid" in prompt
    assert "You have not been given the human record" in prompt
    assert "third party contributed to or completed the death" not in prompt

    assert "The run occurs exactly once" in protocol
    assert "No retry is allowed for an uninteresting, inconvenient, malformed, or disagreeing answer" in protocol
    assert "do not ask the model to regenerate" in protocol
    assert "Preserve the raw response exactly before parsing" in protocol
    assert "Model output is not an answer key or truth verdict" in protocol

    assert model_template["human_record_exposed"] == "no"
    assert model_template["retry_count"] == "0"
    assert model_template["regenerated_output"] == "no"
    assert model_template["raw_response_preserved"] == "yes"
    assert model_template["output_file"] == ""
    assert model_template["output_sha256"] == ""

    assert ai_template["actor_type"] == "model"
    assert ai_template["annotation_stage"] == "ai_independent"
    for field in (
        "primary_evidence_segment_ids",
        "function_label",
        "rationale_mechanism",
        "uncertainty_flag",
        "rationale_note",
        "alternative_pathway_present",
        "alternative_mechanism",
        "alternative_note",
    ):
        assert ai_template[field] == ""

    assert not (AI_RUN / "ai_raw_output.txt").exists()
    assert not (AI_RUN / "ai_independent_record.csv").exists()
    assert not (AI_RUN / "model_run_manifest.csv").exists()
    assert not (AI_RUN / "comparison").exists()
    assert not (AI_RUN / "outputs").exists()


def test_ai_run_checksum_file_matches_frozen_inputs_only():
    expected = {}
    for line in _read(AI_RUN / "AI_RUN_SHA256SUMS.txt").splitlines():
        digest, filename = line.split("  ", 1)
        expected[filename] = digest

    assert set(expected) == EXPECTED_AI_RUN - {"AI_RUN_SHA256SUMS.txt"}
    assert "AI_RUN_SHA256SUMS.txt" not in expected
    for filename, digest in expected.items():
        assert _sha256(AI_RUN / filename) == digest


def test_position_note_files_remain_unchanged():
    position = ROOT / "research" / "position_note"

    for filename, digest in POSITION_NOTE_HASHES.items():
        assert _sha256(position / filename) == digest
