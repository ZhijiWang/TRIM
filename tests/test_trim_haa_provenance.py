import csv
from pathlib import Path

from trim_haa.hashing import looks_like_sha256, sha256_text
from trim_haa.provenance import AssistanceProvenance, lineage_for, prompt_hash
from trim_haa.schema import TrimHAAAnnotation
from trim_haa.validator import validate_dataset, validate_provenance_record


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "trim_haa"


def _load_core(name):
    with (FIXTURE_DIR / name).open(newline="", encoding="utf-8") as handle:
        return [TrimHAAAnnotation.from_record(row) for row in csv.DictReader(handle)]


def _load_provenance(name):
    with (FIXTURE_DIR / name).open(newline="", encoding="utf-8") as handle:
        return [AssistanceProvenance.from_record(row) for row in csv.DictReader(handle)]


def test_parent_child_validity_and_lineage():
    records = _load_core("core_valid.csv")

    assert lineage_for("H01_C03_POST", records) == ["H01_C03_PRE", "H01_C03_POST"]
    assert validate_dataset(records).valid


def test_invalid_missing_parent_cycle_and_unlocked_parent():
    report = validate_dataset(_load_core("core_invalid.csv"))
    messages = [issue.message for issue in report.errors]

    assert "Parent annotation does not exist." in messages
    assert "Cycles are forbidden." in messages
    assert "human_post_ai parent must be locked." in messages


def test_ai_metadata_requirements():
    issues = validate_provenance_record(_load_provenance("provenance_invalid_ai_metadata.csv")[0])
    fields = {issue.field for issue in issues}

    assert {"model_provider", "model_name", "prompt_template_id", "prompt_hash", "model_run_id"} <= fields


def test_prompt_hashing():
    digest = prompt_hash("exact prompt text")

    assert digest == sha256_text("exact prompt text")
    assert looks_like_sha256(digest)


def test_model_run_manifest_template_headers():
    path = Path(__file__).parents[1] / "data" / "trim_haa_model_run_manifest_template.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        headers = next(csv.reader(handle))

    assert "model_run_id" in headers
    assert "output_sha256" in headers
    assert "conversation_context_description" in headers


def test_provenance_completeness_valid_fixture_subset():
    records = [row for row in _load_core("core_valid.csv") if row.case_id == "C01"]
    provenance = _load_provenance("provenance_valid.csv")
    report = validate_dataset(records, provenance)

    assert report.valid
    assert not [issue for issue in report.warnings if issue.field == "provenance"]

