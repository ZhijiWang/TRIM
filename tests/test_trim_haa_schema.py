import csv
from pathlib import Path

from trim_haa.depth import TrimHAADepth
from trim_haa.schema import TrimHAAAnnotation
from trim_haa.validator import validate_core_record


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "trim_haa"


def test_core_schema_creation():
    record = TrimHAAAnnotation(
        annotation_id="H01_CASE01_PRE",
        case_id="CASE01",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_pre",
        primary_evidence_segment_ids="S1|S2",
        function_label="label_a",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="Submitted human justification.",
        alternative_pathway_present="no",
        status="locked",
    )

    assert record.primary_evidence_segment_ids == ("S1", "S2")
    assert record.is_independent is True
    assert record.to_csv_record()["primary_evidence_segment_ids"] == "S1|S2"


def test_core_required_fields():
    issues = validate_core_record(TrimHAAAnnotation(annotation_id="missing"))

    assert any(issue.field == "case_id" for issue in issues)
    assert any(issue.field == "primary_evidence_segment_ids" for issue in issues)


def test_alternative_requirements():
    issues = validate_core_record(
        TrimHAAAnnotation(
            annotation_id="ALT",
            case_id="C1",
            actor_id="H01",
            actor_type="human",
            annotation_stage="human_pre",
            primary_evidence_segment_ids="S1",
            function_label="label_a",
            rationale_mechanism="supports",
            uncertainty_flag="medium",
            rationale_note="Alternative exists but details are missing.",
            alternative_pathway_present="yes",
            status="locked",
        )
    )

    fields = {issue.field for issue in issues}
    assert "alternative_mechanism" in fields
    assert "alternative_note" in fields


def test_depth_module_is_optional_and_linked_by_annotation_id():
    depth = TrimHAADepth(
        annotation_id="H01_CASE01_PRE",
        context_segment_ids="S2|S3",
        friction_locus="boundary_setting",
    )

    assert depth.annotation_id == "H01_CASE01_PRE"
    assert depth.context_segment_ids == ("S2", "S3")


def test_fixture_core_csv_loads():
    with (FIXTURE_DIR / "core_valid.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) >= 30
    assert TrimHAAAnnotation.from_record(rows[0]).annotation_id == "H01_C01_PRE"

