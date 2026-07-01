import csv
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).parents[1]
ETHICS_DIR = ROOT / "ethics"
PILOT_DIR = ROOT / "pilot_protocol"
ZIP_PATH = ROOT / "artifacts" / "TRIM_HAA_pilot_ethics_package_v0_2.zip"
ZIP_SHA_PATH = ROOT / "artifacts" / "TRIM_HAA_pilot_ethics_package_v0_2.zip.sha256"
V01_ZIP_PATH = ROOT / "artifacts" / "TRIM_HAA_pilot_ethics_package_v0_1.zip"
V01_ZIP_SHA_PATH = ROOT / "artifacts" / "TRIM_HAA_pilot_ethics_package_v0_1.zip.sha256"
V01_SHA = "d09edd46b3c463f8c8c163058d6cbe084691bb044113efff7bb3d35e8c72bb69"
MANIFEST_PATH = PILOT_DIR / "TRIM_HAA_pilot_package_manifest.csv"
DURATION = "approximately 60-90 minutes"

ETHICS_FILES = {
    "TRIM_HAA_participant_information_sheet.md",
    "TRIM_HAA_consent_form.md",
    "TRIM_HAA_debrief_sheet.md",
    "TRIM_HAA_data_management_plan.md",
    "TRIM_HAA_risk_assessment.md",
    "TRIM_HAA_ethics_submission_summary.md",
    "TRIM_HAA_pre_submission_blockers.md",
}

PILOT_FILES = {
    "TRIM_HAA_pilot_research_questions.md",
    "TRIM_HAA_instrumentation_pilot_protocol.md",
    "TRIM_HAA_interface_specification.md",
    "TRIM_HAA_participant_workflow.md",
    "TRIM_HAA_participant_core_guide.md",
    "TRIM_HAA_participant_label_guide.md",
    "TRIM_HAA_participant_mechanism_guide.md",
    "TRIM_HAA_practice_case_protocol.md",
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
    "TRIM_HAA_participant_language_review_checklist.md",
    "TRIM_HAA_pilot_data_dictionary.csv",
    "TRIM_HAA_pilot_package_manifest.csv",
}

PARTICIPANT_FACING = {
    ETHICS_DIR / "TRIM_HAA_participant_information_sheet.md",
    ETHICS_DIR / "TRIM_HAA_consent_form.md",
    ETHICS_DIR / "TRIM_HAA_debrief_sheet.md",
    PILOT_DIR / "TRIM_HAA_participant_workflow.md",
    PILOT_DIR / "TRIM_HAA_participant_core_guide.md",
    PILOT_DIR / "TRIM_HAA_participant_label_guide.md",
    PILOT_DIR / "TRIM_HAA_participant_mechanism_guide.md",
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


def test_participant_information_sheet_is_plain_language_and_non_evaluative():
    sheet = _read(ETHICS_DIR / "TRIM_HAA_participant_information_sheet.md")

    assert "structured text-annotation task is understandable and manageable" in sheet
    assert "evaluates the annotation workflow, not your intelligence" in sheet
    assert "The task is not an examination" in sheet
    assert "not expected to agree with AI" in sheet


def test_duration_range_is_present_consistently_in_participant_facing_docs():
    for path in PARTICIPANT_FACING:
        assert DURATION in _read(path), path


def test_second_pass_interface_shows_own_locked_prior_response_in_both_conditions():
    spec = _read(PILOT_DIR / "TRIM_HAA_interface_specification.md").lower()
    control = _read(PILOT_DIR / "TRIM_HAA_control_condition_instructions.md").lower()
    ai = _read(PILOT_DIR / "TRIM_HAA_AI_exposure_instructions.md").lower()

    assert "your earlier response" in spec
    assert "ai-review condition: frozen ai-response panel present" in spec
    assert "control condition: ai-response panel absent" in spec
    assert "the only intended difference" in spec
    assert "your own locked earlier response" in control
    assert "your earlier locked response" in ai
    assert "must never complete a second-pass record without access" in spec


def test_control_instructions_contain_no_ai_output_and_ai_not_answer_key():
    control = _read(PILOT_DIR / "TRIM_HAA_control_condition_instructions.md").lower()
    ai = _read(PILOT_DIR / "TRIM_HAA_AI_exposure_instructions.md").lower()

    assert "no ai-generated material" in control
    assert "ai output" in control
    assert "ai label" in control
    assert "ai evidence" in control
    assert "ai rationale" in control
    assert "not an answer key" in ai
    assert "one possible annotation" in ai


def test_label_and_mechanism_guides_are_templates_with_blocker_notes():
    label = _read(PILOT_DIR / "TRIM_HAA_participant_label_guide.md")
    mechanism = _read(PILOT_DIR / "TRIM_HAA_participant_mechanism_guide.md")

    assert "final study label set is not frozen" in label
    assert "Ethics-submission blocker" in label
    assert "Synthetic Demonstration Label Set" in label
    assert "How does the selected evidence support your function label?" in mechanism
    assert "final study mechanism vocabulary is not frozen" in mechanism
    assert "Ethics-submission blocker" in mechanism


def test_practice_case_protocol_and_outcomes_exist():
    practice = _read(PILOT_DIR / "TRIM_HAA_practice_case_protocol.md")

    assert "not scored for interpretive correctness" in practice
    assert "Select at least one primary-evidence segment" in practice
    assert "ready_for_formal_pilot" in practice
    assert "ready_with_documented_support" in practice
    assert "usability_feedback_only" in practice
    assert "stop_session" in practice
    assert "instrument failure, not participant failure" in practice


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
            "procedural_question_count",
            "protocol_deviation_id",
            "task_timing",
            "practice_case_outcome",
            "researcher_intervention_time",
            "comprehension_check_result",
            "ai_panel_viewed",
            "quotation_consent",
            "public_release_consent",
        }
    )

    assert required <= fields


def test_consent_covers_pilot_data_and_optional_yes_no_release():
    consent = _read(ETHICS_DIR / "TRIM_HAA_consent_form.md")

    assert "## Mandatory Consent" in consent
    assert "background questionnaire" in consent
    assert "revision-reason responses" in consent
    assert "burden and comprehension responses" in consent
    assert "task timing and timestamps" in consent
    assert "procedural-question logging" in consent
    assert "AI-review and no-AI second-pass conditions" in consent
    assert "workflow rather than my intelligence" in consent
    assert "incomplete required task fields" in consent
    assert "## Optional Consent" in consent
    assert "Yes / No — I agree to de-identified rationale excerpts being quoted." in consent
    assert "Yes / No — I agree to de-identified structured annotations" in consent


def test_burden_questionnaire_uses_non_accusatory_wording_and_real_comprehension_check():
    questionnaire = _read(PILOT_DIR / "TRIM_HAA_burden_and_comprehension_questionnaire.md")

    assert 'Select "Agree" for this item' not in questionnaire
    assert "Some wording in my final rationale was taken from or adapted" in questionnaire
    assert "The AI-generated annotation was presented as:" in questionnaire
    assert "One possible annotation" in questionnaire
    assert "do not combine all items into one total score" in questionnaire.lower()
    assert "function label from the rationale mechanism" in questionnaire
    assert "leaving my earlier answer unchanged was acceptable" in questionnaire


def test_researcher_script_prohibits_case_specific_interpretive_help():
    script = _read(PILOT_DIR / "TRIM_HAA_researcher_session_script.md")

    assert "workflow, not your intelligence" in script
    assert "Create new case-specific examples" in script
    assert "Say whether a mechanism applies to the current case" in script
    assert "Compare participant quality with AI quality" in script
    assert "Praise agreement with AI" in script
    assert "I cannot tell you whether it applies to this case" in script
    assert "Procedural questions" in script
    assert "Researcher intervention time" in script


def test_blockers_document_exists_and_marks_final_submission_blockers():
    blockers = _read(ETHICS_DIR / "TRIM_HAA_pre_submission_blockers.md")

    assert "not final-submission-ready" in blockers
    assert "Final participant label guide" in blockers
    assert "Final mechanism guide" in blockers
    assert "Source-text copyright/legal review" in blockers
    assert "Participant-language review" in blockers


def test_quality_check_for_disallowed_language_and_claims():
    text = _all_package_text()
    forbidden = {
        "if the interface design permits",
        "willing to defend",
        'select "agree" for this item',
        "justificatory",
        "ai is correct",
        "agreement means quality",
        "participant is being assessed",
        "ethics approval granted",
        "approved by the ethics committee",
        "exemption granted",
        "please provide hidden chain-of-thought",
    }

    for phrase in forbidden:
        assert phrase not in text

    assert "hidden chain-of-thought is never collected" in text


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


def test_package_zip_v02_is_deterministic_and_v01_remains_unchanged():
    assert V01_ZIP_PATH.exists()
    assert V01_ZIP_SHA_PATH.exists()
    assert _sha256(V01_ZIP_PATH) == V01_SHA
    assert V01_ZIP_SHA_PATH.read_text(encoding="utf-8").split()[0] == V01_SHA

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
