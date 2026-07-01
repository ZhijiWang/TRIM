import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PUBLIC = ROOT / "examples" / "in_a_grove_walkthrough_public_v0_2"
AUTHOR = PUBLIC / "author_record_v0_1"
AI_RUN = PUBLIC / "ai_run_v0_1"
COMPARISON = PUBLIC / "comparison_v0_1"
EXPECTED_PROMPT_SHA = "7da94b590e7fca93927a59351936a4796b9828b7d7a2e106800fc1bcc240eca5"
EXPECTED_AUTHOR_SHA = "6d78fd9d161d7a11c23ce962b257864eda16801793c6d87f17466e99ef269c50"
EXPECTED_AI_SHA = "e9684ca9e776826f20647a59592caa9f6502dd471d87849b1fa76f4915e8338d"
EXPECTED_RAW_AI_SHA = "40c9eaf10bccf9d78b77bed96f7d424e10903a53f5577d3db676d709ec8f7e73"

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
    "comparison_v0_1",
}
EXPECTED_AI_RUN = {
    "prompt.txt",
    "prompt_manifest.csv",
    "ai_record_template.csv",
    "run_protocol.md",
    "model_run_manifest_template.csv",
    "AI_RUN_SHA256SUMS.txt",
    "ai_raw_output.txt",
    "ai_independent_record.csv",
    "ai_external_knowledge_note.txt",
    "ai_lock_manifest.csv",
    "model_run_manifest.csv",
    "ai_parse_log.md",
    "ai_record_validation_report.md",
}
EXPECTED_COMPARISON = {
    "comparison_manifest.csv",
    "field_comparison.csv",
    "evidence_comparison.csv",
    "alternative_pathway_comparison.csv",
    "comparison_summary.md",
    "claim_boundaries.md",
    "COMPARISON_SHA256SUMS.txt",
}
FROZEN_AI_RUN_INPUTS = {
    "prompt.txt",
    "prompt_manifest.csv",
    "ai_record_template.csv",
    "run_protocol.md",
    "model_run_manifest_template.csv",
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
FORBIDDEN_OUTPUT_DIRS = {
    "comparison",
    "outputs",
}
FORBIDDEN_COMPARISON_ARTIFACTS = {
    "adjudicated_record.csv",
    "human_post_ai_record.csv",
    "revised_author_record.csv",
    "revised_ai_record.csv",
    "truth_verdict.md",
    "winner.txt",
}
FORBIDDEN_STAGES = {
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
    assert COMPARISON.is_dir()
    assert {path.name for path in COMPARISON.iterdir()} == EXPECTED_COMPARISON
    assert not any((COMPARISON / name).exists() for name in FORBIDDEN_COMPARISON_ARTIFACTS)
    assert not any((PUBLIC / name).exists() for name in FORBIDDEN_ROOT_AI)
    assert not [
        path
        for name in FORBIDDEN_OUTPUT_DIRS
        for path in PUBLIC.glob(f"**/{name}")
    ]

    ai_stage_files = {
        AI_RUN / "ai_record_template.csv",
        AI_RUN / "ai_independent_record.csv",
        AI_RUN / "ai_lock_manifest.csv",
    }
    for csv_path in PUBLIC.glob("**/*.csv"):
        for row in _rows(csv_path):
            stage = row.get("annotation_stage", "")
            assert stage not in FORBIDDEN_STAGES
            if stage == "ai_independent":
                assert csv_path in ai_stage_files


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
    assert digest == EXPECTED_AUTHOR_SHA
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
    assert "ai_run_executed_once: yes" in status
    assert "raw_response_preserved: yes" in status
    assert "ai_record_validated_and_locked: yes" in status
    assert "ai_record_locked: yes" in status
    assert "descriptive_comparison_completed_and_frozen: yes" in status
    assert "adjudication_performed: no" in status
    assert "truth_verdict_assigned: no" in status
    assert "ready_for_ai_run: no" in status
    assert "ready_for_comparison: no" in status
    assert "ready_for_position_note_review: yes" in status
    assert "ready_for_new_ai_record: no" in status
    assert "ready_for_public_release: no" in status
    assert "without changing the position note" in status


def test_ai_run_infrastructure_and_templates_are_frozen():
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

    assert not (AI_RUN / "comparison").exists()
    assert not (AI_RUN / "outputs").exists()


def test_ai_run_checksum_file_matches_frozen_inputs_only():
    expected = {}
    for line in _read(AI_RUN / "AI_RUN_SHA256SUMS.txt").splitlines():
        digest, filename = line.split("  ", 1)
        expected[filename] = digest

    assert set(expected) == FROZEN_AI_RUN_INPUTS
    assert "AI_RUN_SHA256SUMS.txt" not in expected
    for filename, digest in expected.items():
        assert _sha256(AI_RUN / filename) == digest


def test_completed_ai_run_is_preserved_validated_and_locked():
    from trim_haa.locking import annotation_sha256, verify_locked_annotation
    from trim_haa.schema import TrimHAAAnnotation
    from trim_haa.validator import validate_core_record

    raw_path = AI_RUN / "ai_raw_output.txt"
    ai_rows = _rows(AI_RUN / "ai_independent_record.csv")
    lock = _rows(AI_RUN / "ai_lock_manifest.csv")[0]
    model_run = _rows(AI_RUN / "model_run_manifest.csv")[0]
    parse_log = _read(AI_RUN / "ai_parse_log.md")
    validation_report = _read(AI_RUN / "ai_record_validation_report.md")
    external_note = _read(AI_RUN / "ai_external_knowledge_note.txt")
    source_ids = {
        row["segment_id"] for row in _rows(PUBLIC / "source_segments_japanese.csv")
    }

    assert raw_path.exists()
    assert _sha256(raw_path) == EXPECTED_RAW_AI_SHA
    assert _sha256(raw_path) == model_run["output_sha256"]
    assert model_run["human_record_exposed"] == "no"
    assert model_run["retry_count"] == "0"
    assert model_run["regenerated_output"] == "no"
    assert model_run["raw_response_preserved"] == "yes"
    assert len(ai_rows) == 1

    record = ai_rows[0]
    assert record["annotation_id"] == "IAG_JP_V02_AI_INDEPENDENT"
    assert record["case_id"] == "IAG_JP_PUBLIC_002"
    assert record["parent_annotation_id"] == ""
    assert record["actor_id"] == "MODEL_INDEPENDENT"
    assert record["actor_type"] == "model"
    assert record["annotation_stage"] == "ai_independent"
    assert record["status"] == "locked"

    evidence_ids = record["primary_evidence_segment_ids"].split("|")
    assert evidence_ids
    assert set(evidence_ids).issubset(source_ids)

    annotation = TrimHAAAnnotation.from_record(record)
    assert validate_core_record(annotation) == []
    assert verify_locked_annotation(annotation, lock)
    assert annotation_sha256(annotation) == lock["canonical_record_sha256"]
    assert annotation_sha256(annotation) == EXPECTED_AI_SHA
    assert lock["lock_status"] == "locked"

    assert external_note == ""
    assert "raw_output_valid_json: yes" in parse_log
    assert "code_fences_removed: no" in parse_log
    assert "surrounding_text_removed: no" in parse_log
    assert "substantive_rewriting_occurred: no" in parse_log
    assert "external_knowledge_note_separated: yes" in parse_log
    assert "final_validation_status: passed" in parse_log

    assert "validation_status: `passed`" in validation_report
    assert "evidence_id_validity: `passed`" in validation_report
    assert "lock_verification_result: `passed`" in validation_report
    assert "comparison_performed: `no`" in validation_report
    assert not (AI_RUN / "comparison").exists()
    assert not (AI_RUN / "outputs").exists()


def test_public_v02_comparison_manifest_references_locked_records():
    from trim_haa.locking import annotation_sha256, verify_locked_annotation
    from trim_haa.schema import TrimHAAAnnotation

    author_record = TrimHAAAnnotation.from_record(
        _rows(AUTHOR / "author_analytic_record.csv")[0]
    )
    ai_record = TrimHAAAnnotation.from_record(
        _rows(AI_RUN / "ai_independent_record.csv")[0]
    )
    author_lock = _rows(AUTHOR / "author_lock_manifest.csv")[0]
    ai_lock = _rows(AI_RUN / "ai_lock_manifest.csv")[0]
    manifest = _rows(COMPARISON / "comparison_manifest.csv")[0]

    assert verify_locked_annotation(author_record, author_lock)
    assert verify_locked_annotation(ai_record, ai_lock)
    assert annotation_sha256(author_record) == EXPECTED_AUTHOR_SHA
    assert annotation_sha256(ai_record) == EXPECTED_AI_SHA
    assert _sha256(AI_RUN / "prompt.txt") == EXPECTED_PROMPT_SHA
    assert _sha256(AI_RUN / "ai_raw_output.txt") == EXPECTED_RAW_AI_SHA

    assert manifest["comparison_id"] == "IAG_JP_V02_COMPARISON_001"
    assert manifest["case_id"] == "IAG_JP_PUBLIC_002"
    assert manifest["author_annotation_id"] == "IAG_JP_V02_AUTHOR_PRE"
    assert manifest["author_record_sha256"] == EXPECTED_AUTHOR_SHA
    assert manifest["ai_annotation_id"] == "IAG_JP_V02_AI_INDEPENDENT"
    assert manifest["ai_record_sha256"] == EXPECTED_AI_SHA
    assert manifest["comparison_status"] == "frozen"
    assert manifest["comparison_type"] == "descriptive_locked_record_comparison"
    assert manifest["adjudication_performed"] == "no"
    assert manifest["truth_verdict_assigned"] == "no"
    assert "neither record was revised" in manifest["notes"]


def test_public_v02_evidence_comparison_metrics_are_descriptive():
    rows = _rows(COMPARISON / "evidence_comparison.csv")
    source_ids = {
        row["segment_id"] for row in _rows(PUBLIC / "source_segments_japanese.csv")
    }
    required = {
        "IAG-JP-FRAME-001",
        "IAG-JP-010",
        "IAG-JP-011",
        "IAG-JP-017",
        "IAG-JP-018",
        "IAG-JP-019",
        "IAG-JP-020",
        "IAG-JP-021",
    }
    assert {row["segment_id"] for row in rows} == required
    assert {row["segment_id"] for row in rows}.issubset(source_ids)

    author_set = {row["segment_id"] for row in rows if row["author_selected"] == "yes"}
    ai_set = {row["segment_id"] for row in rows if row["ai_selected"] == "yes"}
    shared = author_set & ai_set
    union = author_set | ai_set
    author_only = author_set - ai_set
    ai_only = ai_set - author_set

    assert len(author_set) == 5
    assert len(ai_set) == 7
    assert len(shared) == 4
    assert len(union) == 8
    assert len(author_only) == 1
    assert len(ai_only) == 3
    assert round(len(shared) / len(union), 4) == 0.5000
    assert round(len(shared) / len(author_set), 4) == 0.8000
    assert round(len(shared) / len(ai_set), 4) == 0.5714
    assert {row["selection_relation"] for row in rows} <= {
        "shared",
        "author_only",
        "ai_only",
    }


def test_public_v02_field_and_alternative_comparison_contracts():
    field_rows = _rows(COMPARISON / "field_comparison.csv")
    alt_rows = _rows(COMPARISON / "alternative_pathway_comparison.csv")

    assert [row["field"] for row in field_rows] == [
        "function_label",
        "primary_evidence_segment_ids",
        "rationale_mechanism",
        "uncertainty_flag",
        "rationale_note",
        "alternative_pathway_present",
        "alternative_mechanism",
        "alternative_note",
        "overall_interpretive_structure",
    ]
    assert {row["comparison_type"] for row in field_rows} <= {
        "exact_match",
        "different_value",
        "partial_overlap",
        "shared_structure_different_emphasis",
        "primary_alternative_inversion",
        "uncertainty_difference",
        "not_comparable_as_exact_text",
    }
    by_field = {row["field"]: row for row in field_rows}
    assert by_field["function_label"]["exact_match"] == "no"
    assert by_field["uncertainty_flag"]["comparison_type"] == "uncertainty_difference"
    assert by_field["alternative_pathway_present"]["exact_match"] == "yes"
    assert by_field["overall_interpretive_structure"]["comparison_type"] == (
        "primary_alternative_inversion"
    )
    assert "substantially the same two pathways with different prioritisation" in (
        by_field["overall_interpretive_structure"]["descriptive_note"]
    )

    assert [row["dimension"] for row in alt_rows] == [
        "self_inflicted_pathway",
        "third_party_intervention_pathway",
        "mediation_or_testimony_frame",
        "causal_completion",
    ]
    assert any(
        row["comparison_type"] == "primary_alternative_inversion" for row in alt_rows
    )


def test_public_v02_comparison_summary_and_boundaries_are_non_adjudicative():
    summary = _read(COMPARISON / "comparison_summary.md")
    boundaries = _read(COMPARISON / "claim_boundaries.md")

    for heading in [
        "# Author–AI Comparison: IAG_JP_PUBLIC_002",
        "## Record integrity",
        "## Final-label relation",
        "## Evidence selection",
        "## Rationale mechanisms",
        "## Uncertainty",
        "## Alternative-pathway handling",
        "## Shared interpretive structure",
        "## Unresolved differences",
        "## What this comparison supports",
        "## What this comparison does not support",
    ]:
        assert heading in summary
    assert "Jaccard overlap 0.5000" in summary
    assert "author coverage by AI 0.8000" in summary
    assert "AI coverage by author 0.5714" in summary
    assert "primary-alternative inversion is identified" in summary
    for phrase in (
        "correct",
        "incorrect",
        "better",
        "worse",
        "model failure",
        "hallucination",
        "overconfident",
        "underconfident",
        "actual killer",
        "proves suicide",
        "proves homicide",
        "author was right",
        "model was right",
    ):
        assert phrase not in summary.lower()

    assert "# Claim Boundaries" in boundaries
    assert "## Supported by this comparison" in boundaries
    assert "## Not supported by this comparison" in boundaries
    assert "## Requires additional cases or human evaluation" in boundaries
    for unsupported in (
        "One interpretation is correct.",
        "One annotator is superior.",
        "The model misunderstood the text.",
        "The author identified the true killer.",
        "The medium deliberately deceived anyone.",
        "Third-party homicide is established.",
        "Self-inflicted death is established as the complete causal account.",
        "AI assistance changed human judgment.",
        "TRIM-HAA is empirically validated.",
        "Evidence overlap proves semantic agreement.",
        "Label disagreement proves completely different interpretations.",
    ):
        assert unsupported in boundaries


def test_public_v02_comparison_checksums_match_frozen_outputs():
    expected = {}
    for line in _read(COMPARISON / "COMPARISON_SHA256SUMS.txt").splitlines():
        digest, filename = line.split("  ", 1)
        expected[filename] = digest

    assert set(expected) == EXPECTED_COMPARISON - {"COMPARISON_SHA256SUMS.txt"}
    assert "COMPARISON_SHA256SUMS.txt" not in expected
    for filename, digest in expected.items():
        assert _sha256(COMPARISON / filename) == digest


def test_public_v02_no_post_ai_or_adjudicated_records_exist():
    forbidden = {
        "human_post_ai_record.csv",
        "adjudicated_record.csv",
        "revised_author_record.csv",
        "revised_ai_record.csv",
        "truth_verdict.md",
        "winner.txt",
    }
    assert not [path for path in PUBLIC.glob("**/*") if path.name in forbidden]

    for csv_path in PUBLIC.glob("**/*.csv"):
        for row in _rows(csv_path):
            assert row.get("annotation_stage", "") not in FORBIDDEN_STAGES


def test_public_v02_schema_files_remain_unchanged():
    assert _sha256(ROOT / "src" / "trim_haa" / "schema.py") == (
        "bf0540c2c34e02e93f19f2559d5794f6fc59579a363e29a7858e478bb88a4264"
    )
    assert _sha256(ROOT / "src" / "trim_haa" / "provenance.py") == (
        "92e075aa74afd0661fb6446c1253863883b651df735aaec0ec073638af0fdd14"
    )
    assert _sha256(ROOT / "docs" / "core_schema.md") == (
        "e2ee7e73bfc4239a69b3d3534af508525775a3840aa228cbcbe24389fcb0d6e4"
    )
    assert _sha256(ROOT / "docs" / "provenance.md") == (
        "66fbd4c679650797e8d4194c52527075c77b90734963389ce9226c9271774e74"
    )


def test_position_note_files_remain_unchanged():
    position = ROOT / "research" / "position_note"

    for filename, digest in POSITION_NOTE_HASHES.items():
        assert _sha256(position / filename) == digest
