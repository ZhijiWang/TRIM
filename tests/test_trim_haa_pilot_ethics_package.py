import csv
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).parents[1]
ETHICS_DIR = ROOT / "ethics"
PILOT_DIR = ROOT / "pilot_protocol"
ZIP_PATH = ROOT / "artifacts" / "TRIM_HAA_pilot_ethics_package_v0_1.zip"
ZIP_SHA_PATH = ROOT / "artifacts" / "TRIM_HAA_pilot_ethics_package_v0_1.zip.sha256"
MANIFEST_PATH = PILOT_DIR / "TRIM_HAA_pilot_package_manifest.csv"

ETHICS_FILES = {
    "TRIM_HAA_participant_information_sheet.md",
    "TRIM_HAA_consent_form.md",
    "TRIM_HAA_debrief_sheet.md",
    "TRIM_HAA_data_management_plan.md",
    "TRIM_HAA_risk_assessment.md",
    "TRIM_HAA_ethics_submission_summary.md",
}

PILOT_FILES = {
    "TRIM_HAA_pilot_research_questions.md",
    "TRIM_HAA_instrumentation_pilot_protocol.md",
    "TRIM_HAA_participant_workflow.md",
    "TRIM_HAA_participant_core_guide.md",
    "TRIM_HAA_AI_exposure_instructions.md",
    "TRIM_HAA_control_condition_instructions.md",
    "TRIM_HAA_participant_background_questionnaire.md",
    "TRIM_HAA_revision_reason_instrument.md",
    "TRIM_HAA_burden_and_comprehension_questionnaire.md",
    "TRIM_HAA_researcher_session_script.md",
    "TRIM_HAA_contamination_screen.md",
    "TRIM_HAA_case_selection_criteria.md",
    "TRIM_HAA_pilot_stopping_rules.md",
    "TRIM_HAA_feasibility_analysis_plan.md",
    "TRIM_HAA_feasibility_success_criteria.md",
    "TRIM_HAA_pilot_data_dictionary.csv",
    "TRIM_HAA_pilot_package_manifest.csv",
}

PARTICIPANT_FACING = {
    ETHICS_DIR / "TRIM_HAA_participant_information_sheet.md",
    ETHICS_DIR / "TRIM_HAA_consent_form.md",
    ETHICS_DIR / "TRIM_HAA_debrief_sheet.md",
    PILOT_DIR / "TRIM_HAA_participant_workflow.md",
    PILOT_DIR / "TRIM_HAA_participant_core_guide.md",
    PILOT_DIR / "TRIM_HAA_AI_exposure_instructions.md",
    PILOT_DIR / "TRIM_HAA_control_condition_instructions.md",
    PILOT_DIR / "TRIM_HAA_participant_background_questionnaire.md",
    PILOT_DIR / "TRIM_HAA_revision_reason_instrument.md",
    PILOT_DIR / "TRIM_HAA_burden_and_comprehension_questionnaire.md",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _all_package_text() -> str:
    parts = []
    for directory, files in ((ETHICS_DIR, ETHICS_FILES), (PILOT_DIR, PILOT_FILES)):
        for name in files:
            parts.append(_read(directory / name))
    return "\n".join(parts).lower()


def test_required_ethics_and_pilot_files_exist():
    assert {path.name for path in ETHICS_DIR.glob("TRIM_HAA_*.md")} >= ETHICS_FILES
    assert {path.name for path in PILOT_DIR.glob("TRIM_HAA_*")} >= PILOT_FILES


def test_data_dictionary_covers_collected_fields():
    rows = _csv_rows(PILOT_DIR / "TRIM_HAA_pilot_data_dictionary.csv")
    fields = {row["field_name"] for row in rows}
    required = set()
    for template in (
        ROOT / "data" / "trim_haa_core_template.csv",
        ROOT / "data" / "trim_haa_assistance_provenance_template.csv",
        ROOT / "data" / "trim_haa_exposure_event_template.csv",
        ROOT / "data" / "trim_haa_lock_manifest_template.csv",
    ):
        with template.open(newline="", encoding="utf-8") as handle:
            required.update(next(csv.reader(handle)))
    required.update(
        {
            "participant_id",
            "age_18_or_older",
            "primary_language",
            "revision_reason",
            "core_instruction_clarity",
            "attention_check",
            "procedural_question_count",
            "protocol_deviation_id",
        }
    )

    assert required <= fields


def test_manifest_hashes_match_and_zip_contains_only_manifested_files():
    subprocess.run(
        [sys.executable, "scripts/build_trim_haa_pilot_ethics_package.py"],
        cwd=ROOT,
        check=True,
    )
    rows = _csv_rows(MANIFEST_PATH)
    manifest_files = {row["file_path"] for row in rows}
    for row in rows:
        assert _sha256(ROOT / row["file_path"]) == row["sha256"]

    with zipfile.ZipFile(ZIP_PATH) as archive:
        zip_files = set(archive.namelist())

    assert zip_files == manifest_files | {"pilot_protocol/TRIM_HAA_pilot_package_manifest.csv"}
    assert not any(name.startswith("dry_runs/") for name in zip_files)
    assert not any("historical" in name.lower() for name in zip_files)


def test_package_contains_no_real_participant_data_or_secrets():
    text = _all_package_text()
    forbidden = {
        "api_key",
        "secret_key",
        "bearer ",
        "sk-",
        "legal name:",
        "participant name:",
    }

    for phrase in forbidden:
        assert phrase not in text

    manifest = _csv_rows(MANIFEST_PATH)
    assert all(row["contains_personal_data"] in {"no", "template_only"} for row in manifest)


def test_no_hidden_chain_of_thought_collection_or_approval_claim():
    text = _all_package_text()
    assert "please provide hidden chain-of-thought" not in text
    assert "hidden chain-of-thought is never collected" in text
    assert "does not claim approval" in text
    assert "ethics approval granted" not in text
    assert "approved by the ethics committee" not in text
    assert "exemption granted" not in text


def test_control_instructions_contain_no_ai_output_and_ai_not_answer_key():
    control = _read(PILOT_DIR / "TRIM_HAA_control_condition_instructions.md").lower()
    ai = _read(PILOT_DIR / "TRIM_HAA_AI_exposure_instructions.md").lower()

    assert "you will not see an ai record" in control
    assert "ai label" in control
    assert "ai evidence" in control
    assert "ai rationale" in control
    assert "not an answer key" in ai


def test_consent_separates_optional_public_release():
    consent = _read(ETHICS_DIR / "TRIM_HAA_consent_form.md")

    assert "## Mandatory Consent" in consent
    assert "## Optional Consent" in consent
    assert "public research release" in consent


def test_researcher_instructions_are_non_leading_and_feasibility_focused():
    script = _read(PILOT_DIR / "TRIM_HAA_researcher_session_script.md").lower()
    analysis = _read(PILOT_DIR / "TRIM_HAA_feasibility_analysis_plan.md").lower()

    assert "may not" in script
    assert "suggest a label" in script
    assert "say the ai answer is correct" in script
    assert "no powered hypothesis test" in analysis
    assert "no accuracy claim" in analysis


def test_package_zip_is_deterministic_and_sha_recorded():
    subprocess.run(
        [sys.executable, "scripts/build_trim_haa_pilot_ethics_package.py"],
        cwd=ROOT,
        check=True,
    )
    before = _sha256(ZIP_PATH)
    subprocess.run(
        [sys.executable, "scripts/build_trim_haa_pilot_ethics_package.py"],
        cwd=ROOT,
        check=True,
    )
    after = _sha256(ZIP_PATH)

    assert after == before
    recorded = ZIP_SHA_PATH.read_text(encoding="utf-8").split()[0]
    assert recorded == after
