"""Build the deterministic TRIM-HAA pilot ethics package."""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_VERSION = "v0_2"
ZIP_PATH = ROOT / "artifacts" / f"TRIM_HAA_pilot_ethics_package_{PACKAGE_VERSION}.zip"
ZIP_SHA_PATH = ROOT / "artifacts" / f"TRIM_HAA_pilot_ethics_package_{PACKAGE_VERSION}.zip.sha256"
MANIFEST_PATH = ROOT / "pilot_protocol" / "TRIM_HAA_pilot_package_manifest.csv"
FIXED_ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


PACKAGE_FILES: tuple[dict[str, str], ...] = (
    {
        "file_path": "ethics/TRIM_HAA_participant_information_sheet.md",
        "purpose": "Participant-facing information sheet",
        "contains_personal_data": "no",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "Contains contact and withdrawal placeholders only",
    },
    {
        "file_path": "ethics/TRIM_HAA_consent_form.md",
        "purpose": "Consent form with mandatory and optional items",
        "contains_personal_data": "no",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "Template only; no completed consent records",
    },
    {
        "file_path": "ethics/TRIM_HAA_debrief_sheet.md",
        "purpose": "Participant debrief sheet",
        "contains_personal_data": "no",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "Explains locked pre records and control condition",
    },
    {
        "file_path": "ethics/TRIM_HAA_data_management_plan.md",
        "purpose": "Data management and retention plan",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Contains institutional placeholders",
    },
    {
        "file_path": "ethics/TRIM_HAA_risk_assessment.md",
        "purpose": "Risk assessment with mitigations and stopping criteria",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Draft for review",
    },
    {
        "file_path": "ethics/TRIM_HAA_ethics_submission_summary.md",
        "purpose": "Ethics submission summary",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Does not claim approval",
    },
    {
        "file_path": "ethics/TRIM_HAA_pre_submission_blockers.md",
        "purpose": "Pre-submission blocker list",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Lists unresolved institutional and design blockers",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_pilot_research_questions.md",
        "purpose": "Frozen feasibility research questions",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "No causal analysis claim",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_instrumentation_pilot_protocol.md",
        "purpose": "Instrumentation pilot protocol",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Feasibility pilot only",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_interface_specification.md",
        "purpose": "Fixed second-pass interface specification",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Own-pre response shown in both second-pass conditions",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_participant_workflow.md",
        "purpose": "Participant workflow sequence",
        "contains_personal_data": "no",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "No hidden reasoning collection",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_participant_label_guide.md",
        "purpose": "Participant-facing label-guide template and synthetic demo",
        "contains_personal_data": "no",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "Final study label guide remains a blocker",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_participant_mechanism_guide.md",
        "purpose": "Participant-facing mechanism-guide template and synthetic demo",
        "contains_personal_data": "no",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "Final mechanism vocabulary remains a blocker",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_participant_core_guide.md",
        "purpose": "Plain-language Core instructions",
        "contains_personal_data": "no",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "Uses synthetic examples only",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_practice_case_protocol.md",
        "purpose": "Practice-case comprehension standard",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Defines formal-pilot readiness outcomes",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_participant_language_review_checklist.md",
        "purpose": "Participant-language review checklist",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Required before final submission",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_AI_exposure_instructions.md",
        "purpose": "AI exposure instructions",
        "contains_personal_data": "no",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "States AI is not an answer key",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_control_condition_instructions.md",
        "purpose": "No-AI control condition instructions",
        "contains_personal_data": "no",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "Contains no AI-output exposure",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_participant_background_questionnaire.md",
        "purpose": "Minimal background questionnaire",
        "contains_personal_data": "template_only",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "No legal name field",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_revision_reason_instrument.md",
        "purpose": "Post-case revision-reason instrument",
        "contains_personal_data": "template_only",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "Self-report not proof of adoption",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_burden_and_comprehension_questionnaire.md",
        "purpose": "Burden and comprehension questionnaire",
        "contains_personal_data": "template_only",
        "participant_facing": "yes",
        "ethics_facing": "yes",
        "notes": "Includes attention/comprehension item",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_researcher_session_script.md",
        "purpose": "Non-leading researcher script",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Restricts interpretive coaching",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_contamination_screen.md",
        "purpose": "Contamination screening procedure",
        "contains_personal_data": "template_only",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Does not reuse historical submissions",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_case_selection_criteria.md",
        "purpose": "Case-selection criteria",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Requires separate legal review",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_pilot_stopping_rules.md",
        "purpose": "Stopping and pause rules",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Includes threshold placeholders",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_feasibility_analysis_plan.md",
        "purpose": "Feasibility analysis plan",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Descriptive only",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_feasibility_success_criteria.md",
        "purpose": "Provisional success criteria",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Numerical thresholds need approval",
    },
    {
        "file_path": "pilot_protocol/TRIM_HAA_pilot_data_dictionary.csv",
        "purpose": "Frozen pilot data dictionary",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Covers collected fields without changing Core schema",
    },
    {
        "file_path": "data/trim_haa_core_template.csv",
        "purpose": "Frozen Core record template",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Template only",
    },
    {
        "file_path": "data/trim_haa_assistance_provenance_template.csv",
        "purpose": "Assistance provenance template",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Template only",
    },
    {
        "file_path": "data/trim_haa_exposure_event_template.csv",
        "purpose": "Exposure-event template",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Template only",
    },
    {
        "file_path": "data/trim_haa_lock_manifest_template.csv",
        "purpose": "Cryptographic lock-manifest template",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Template only",
    },
    {
        "file_path": "data/trim_haa_model_run_manifest_template.csv",
        "purpose": "Model-run manifest template",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Template only",
    },
    {
        "file_path": "data/trim_haa_prompt_manifest_template.csv",
        "purpose": "Prompt manifest template",
        "contains_personal_data": "no",
        "participant_facing": "no",
        "ethics_facing": "yes",
        "notes": "Template only; no hidden prompts",
    },
)

MANIFEST_FIELDS = (
    "file_path",
    "purpose",
    "sha256",
    "status",
    "contains_personal_data",
    "participant_facing",
    "ethics_facing",
    "version",
    "notes",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_manifest() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for entry in sorted(PACKAGE_FILES, key=lambda item: item["file_path"]):
        path = ROOT / entry["file_path"]
        if not path.exists():
            raise FileNotFoundError(path)
        rows.append(
            {
                "file_path": entry["file_path"],
                "purpose": entry["purpose"],
                "sha256": sha256_file(path),
                "status": "frozen_for_ethics_package",
                "contains_personal_data": entry["contains_personal_data"],
                "participant_facing": entry["participant_facing"],
                "ethics_facing": entry["ethics_facing"],
                "version": PACKAGE_VERSION,
                "notes": entry["notes"],
            }
        )
    return rows


def write_manifest(rows: list[dict[str, str]]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_zip(rows: list[dict[str, str]]) -> str:
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    files = [row["file_path"] for row in rows] + [str(MANIFEST_PATH.relative_to(ROOT))]
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative_path in sorted(files):
            path = ROOT / relative_path
            info = zipfile.ZipInfo(relative_path, date_time=FIXED_ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    digest = sha256_file(ZIP_PATH)
    ZIP_SHA_PATH.write_text(f"{digest}  {ZIP_PATH.name}\n", encoding="utf-8")
    return digest


def main() -> int:
    rows = build_manifest()
    write_manifest(rows)
    digest = write_zip(rows)
    print(f"{ZIP_PATH.relative_to(ROOT)} {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
