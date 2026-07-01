"""Build deterministic TRIM-HAA synthetic dry-run packages."""

from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
DRY_RUN_ROOT = PROJECT_ROOT / "dry_runs" / "trim_haa_synthetic_v0_1"
INVALID_ROOT = PROJECT_ROOT / "dry_runs" / "trim_haa_synthetic_v0_1_invalid"


def main() -> int:
    build_valid_package(DRY_RUN_ROOT)
    build_invalid_package(DRY_RUN_ROOT, INVALID_ROOT)
    return 0


def build_valid_package(root: Path) -> None:
    from trim_haa.locking import create_lock_record
    from trim_haa.schema import TrimHAAAnnotation

    if root.exists():
        shutil.rmtree(root)
    (root / "outputs").mkdir(parents=True)

    cases = _case_rows()
    participants = _participant_rows()
    assignments = _assignment_rows()
    ai_specs = _ai_specs()

    core_rows: list[dict[str, str]] = []
    provenance_rows: list[dict[str, str]] = []
    exposure_rows: list[dict[str, str]] = []
    lock_rows: list[dict[str, str]] = []
    revision_rows: list[dict[str, str]] = []

    for case_id, spec in ai_specs.items():
        ai_id = f"AI_{case_id}"
        core_rows.append(_core_row(ai_id, case_id, "", "AI_SYNTH", "model", "ai_independent", **spec))
        provenance_rows.append(_ai_provenance(ai_id, case_id))

    for assignment in assignments:
        participant_id = assignment["participant_id"]
        case_id = assignment["case_id"]
        condition = assignment["condition"]
        scenario = assignment["scenario_id"]
        pre_id = f"{participant_id}_{case_id}_PRE"
        pre_spec, second_spec, reason, reason_note = _scenario_specs(scenario, ai_specs[case_id])
        core_rows.append(_core_row(pre_id, case_id, "", participant_id, "human", "human_pre", **pre_spec))
        provenance_rows.append(_pre_provenance(pre_id, case_id, participant_id))
        lock = create_lock_record(
            TrimHAAAnnotation.from_record(core_rows[-1]),
            lock_manifest_id=f"LOCK_{pre_id}",
            locked_at="2026-07-01T00:00:00+00:00",
            locked_by="synthetic_builder",
        )
        lock_rows.append(lock.to_record())

        if condition == "ai_exposure":
            post_id = f"{participant_id}_{case_id}_POST"
            core_rows.append(
                _core_row(
                    post_id,
                    case_id,
                    pre_id,
                    participant_id,
                    "human",
                    "human_post_ai",
                    **second_spec,
                )
            )
            provenance_rows.append(
                _post_provenance(
                    post_id,
                    pre_id,
                    case_id,
                    participant_id,
                    f"AI_{case_id}",
                    f"RUN_{case_id}",
                    pre_spec,
                    second_spec,
                    reason,
                    reason_note,
                )
            )
            exposure_rows.append(
                _exposure_event(
                    f"EXP_{post_id}_001",
                    post_id,
                    pre_id,
                    f"AI_{case_id}",
                    f"RUN_{case_id}",
                    case_id,
                    "1",
                )
            )
            if scenario == "S19":
                exposure_rows.append(
                    _exposure_event(
                        f"EXP_{post_id}_002",
                        post_id,
                        pre_id,
                        f"AI_{case_id}",
                        f"RUN_{case_id}",
                        case_id,
                        "2",
                    )
                )
        else:
            control_id = f"{participant_id}_{case_id}_CONTROL"
            core_rows.append(
                _core_row(
                    control_id,
                    case_id,
                    pre_id,
                    participant_id,
                    "human",
                    "human_second_pass_control",
                    **second_spec,
                )
            )
            provenance_rows.append(
                _control_provenance(
                    control_id,
                    pre_id,
                    case_id,
                    participant_id,
                    pre_spec,
                    second_spec,
                    reason,
                    reason_note,
                )
            )

        revision_rows.append(
            {
                "participant_id": participant_id,
                "case_id": case_id,
                "condition": condition,
                "scenario_id": scenario,
                "self_reported_revision_reason": reason,
                "self_reported_revision_note": reason_note,
            }
        )

    _write_csv(root / "cases.csv", cases)
    _write_csv(root / "participant_metadata.csv", participants)
    _write_csv(root / "case_assignments.csv", assignments)
    _write_csv(root / "core_annotations.csv", core_rows)
    _write_csv(root / "assistance_provenance.csv", provenance_rows)
    _write_csv(root / "exposure_events.csv", exposure_rows)
    _write_csv(root / "lock_manifest.csv", lock_rows)
    _write_csv(root / "model_run_manifest.csv", _model_run_rows())
    _write_csv(root / "prompt_manifest.csv", _prompt_rows())
    _write_csv(root / "revision_reasons.csv", revision_rows)
    (root / "README.md").write_text(_readme_text(), encoding="utf-8")


def build_invalid_package(valid_root: Path, invalid_root: Path) -> None:
    if invalid_root.exists():
        shutil.rmtree(invalid_root)
    shutil.copytree(valid_root, invalid_root)
    core = _read_csv(invalid_root / "core_annotations.csv")
    provenance = _read_csv(invalid_root / "assistance_provenance.csv")
    exposures = _read_csv(invalid_root / "exposure_events.csv")
    locks = _read_csv(invalid_root / "lock_manifest.csv")

    # 1. Tamper locked pre record after hash generation.
    _find(core, "annotation_id", "P01_C01_PRE")["rationale_note"] = "Tampered after lock."
    # 2. Missing exposed AI annotation.
    _find(provenance, "annotation_id", "P01_C03_POST")["exposed_ai_annotation_id"] = "AI_MISSING"
    # 3. Wrong-case AI exposure.
    _find(provenance, "annotation_id", "P01_C04_POST")["exposed_ai_annotation_id"] = "AI_C05"
    # 4. Model-run mismatch.
    _find(provenance, "annotation_id", "P02_C02_POST")["exposed_model_run_id"] = "RUN_WRONG"
    # 5. human-post with no AI exposure.
    row = _find(provenance, "annotation_id", "P02_C03_POST")
    row["ai_output_exposed"] = "none"
    # 6. control with AI exposure.
    _find(provenance, "annotation_id", "P01_C05_CONTROL")["ai_output_exposed"] = "label_only"
    # 7. Core/provenance lock mismatch.
    _find(provenance, "annotation_id", "P01_C02_PRE")["lock_status"] = "draft"
    # 8. Duplicate exposure-event ID.
    exposures.append({**exposures[0]})
    # 9. Invalid stage-condition combination.
    _find(provenance, "annotation_id", "AI_C06")["interface_condition"] = "ai_review"
    # 10. Missing alternative note when alternative=yes.
    _find(core, "annotation_id", "P03_C05_POST")["alternative_note"] = ""
    # Also ensure a lock row still exists but no longer verifies for tampered pre.
    _find(locks, "annotation_id", "P01_C01_PRE")["notes"] = "Intentional invalid tamper test."

    _write_csv(invalid_root / "core_annotations.csv", core)
    _write_csv(invalid_root / "assistance_provenance.csv", provenance)
    _write_csv(invalid_root / "exposure_events.csv", exposures)
    _write_csv(invalid_root / "lock_manifest.csv", locks)


def _case_rows() -> list[dict[str, str]]:
    rows = []
    for number in range(1, 7):
        case_id = f"C{number:02d}"
        rows.append(
            {
                "case_id": case_id,
                "case_title": f"Synthetic interpretive case {number}",
                "segment_ids": "|".join(f"{case_id}_S{i}" for i in range(1, 7)),
                "notes": "Synthetic case; no historical coder answer reused.",
            }
        )
    return rows


def _participant_rows() -> list[dict[str, str]]:
    return [
        {
            "participant_id": f"P{i:02d}",
            "participant_type": "synthetic_human",
            "notes": "Synthetic participant; no real person.",
        }
        for i in range(1, 5)
    ]


def _assignment_rows() -> list[dict[str, str]]:
    mapping = {
        "P01": [
            ("C01", "ai_exposure", "S01"),
            ("C02", "ai_exposure", "S02"),
            ("C03", "ai_exposure", "S03"),
            ("C04", "ai_exposure", "S04"),
            ("C05", "control", "S16"),
            ("C06", "control", "S20"),
        ],
        "P02": [
            ("C01", "control", "S20"),
            ("C02", "ai_exposure", "S05"),
            ("C03", "ai_exposure", "S06"),
            ("C04", "ai_exposure", "S07"),
            ("C05", "ai_exposure", "S08"),
            ("C06", "control", "S16"),
        ],
        "P03": [
            ("C01", "control", "S16"),
            ("C02", "control", "S20"),
            ("C03", "ai_exposure", "S09"),
            ("C04", "ai_exposure", "S10"),
            ("C05", "ai_exposure", "S11"),
            ("C06", "ai_exposure", "S12"),
        ],
        "P04": [
            ("C01", "ai_exposure", "S14"),
            ("C02", "ai_exposure", "S15"),
            ("C03", "control", "S16"),
            ("C04", "control", "S20"),
            ("C05", "ai_exposure", "S17"),
            ("C06", "ai_exposure", "S19"),
        ],
    }
    rows = []
    for participant_id, assignments in mapping.items():
        for order, (case_id, condition, scenario_id) in enumerate(assignments, start=1):
            rows.append(
                {
                    "participant_id": participant_id,
                    "case_id": case_id,
                    "condition": condition,
                    "scenario_id": scenario_id,
                    "assignment_order": str(order),
                }
            )
    return rows


def _ai_specs() -> dict[str, dict[str, str]]:
    return {
        "C01": _spec("C01_S1|C01_S2", "label_a", "supports", "medium", "AI_C01 rationale identifies the same evidence.", "no"),
        "C02": _spec("C02_S2|C02_S3", "label_b", "qualifies", "medium", "AI_C02 rationale uses a different evidence pair.", "no"),
        "C03": _spec("C03_S2", "label_b", "supports", "medium", "AI_C03 rationale supports label_b.", "no"),
        "C04": _spec("C04_S3|C04_S4", "label_a", "reframes", "medium", "AI_C04 rationale reframes the evidence.", "no"),
        "C05": _spec("C05_S2", "label_a", "supports", "low", "AI_C05 repeated phrase exact copied wording appears here.", "no"),
        "C06": _spec("C06_S2", "label_b", "qualifies", "medium", "AI_C06 rationale and full core are copied.", "yes", "qualifies", "AI_C06 alternative note."),
    }


def _scenario_specs(scenario_id: str, ai: dict[str, str]) -> tuple[dict[str, str], dict[str, str], str, str]:
    if scenario_id == "S01":
        return ai | {"rationale_note": "Human independently reached same core pathway."}, ai | {"rationale_note": "Human independently reached same core pathway."}, "ai_confirmed_original_judgment", ""
    if scenario_id == "S02":
        pre = _spec("C02_S1", "label_b", "qualifies", "medium", "Human keeps same label with different evidence.", "no")
        return pre, pre, "rejected_ai_output", ""
    if scenario_id == "S03":
        pre = _spec("C03_S1", "label_a", "supports", "high", "Human pre label differs from AI.", "no")
        post = pre | {"function_label": "label_b", "uncertainty_flag": "medium", "rationale_note": "Human changes label to match AI."}
        return pre, post, "ai_persuaded_interpretive_change", ""
    if scenario_id == "S04":
        pre = _spec("C04_S1|C04_S3", "label_a", "supports", "medium", "Human pre already overlaps the AI evidence set.", "no")
        post = pre | {"primary_evidence_segment_ids": "C04_S1|C04_S2|C04_S3|C04_S4|C04_S5|C04_S6", "rationale_note": "Human adds AI and non-AI evidence without greater convergence."}
        return pre, post, "ai_identified_missed_evidence", ""
    if scenario_id == "S05":
        pre = _spec("C02_S2", "label_b", "qualifies", "medium", "Human pre has one AI-overlap segment.", "no")
        post = pre | {"primary_evidence_segment_ids": "C02_S2|C02_S3", "rationale_note": "Human adds AI evidence while retaining pre evidence."}
        return pre, post, "ai_identified_missed_evidence", ""
    if scenario_id == "S06":
        pre = _spec("C03_S1", "label_b", "supports", "medium", "Human pre evidence is displaced.", "no")
        post = pre | {"primary_evidence_segment_ids": "C03_S2", "rationale_note": "Human replaces pre evidence with AI evidence."}
        return pre, post, "ai_identified_missed_evidence", ""
    if scenario_id == "S07":
        pre = _spec("C04_S3|C04_S4", "label_a", "supports", "medium", "Human pre mechanism differs.", "no")
        post = pre | {"rationale_mechanism": "reframes", "rationale_note": "Human adopts the AI rationale mechanism."}
        return pre, post, "ai_clarified_category_boundary", ""
    if scenario_id == "S08":
        pre = _spec("C05_S2", "label_a", "supports", "high", "Human pre uncertainty is high.", "no")
        post = pre | {"uncertainty_flag": "low", "rationale_note": "Human post uncertainty decreases."}
        return pre, post, "ai_confirmed_original_judgment", ""
    if scenario_id == "S09":
        pre = _spec("C03_S2", "label_b", "supports", "low", "Human pre uncertainty is low.", "no")
        post = pre | {"uncertainty_flag": "high", "rationale_note": "Human becomes more uncertain after review."}
        return pre, post, "mixed_or_unclear", ""
    if scenario_id == "S10":
        pre = _spec("C04_S3", "label_a", "reframes", "medium", "Human pre retains an alternative.", "yes", "qualifies", "Original alternative note.")
        post = pre | {"alternative_pathway_present": "no", "alternative_mechanism": "", "alternative_note": "", "rationale_note": "Human removes alternative after review."}
        return pre, post, "ai_clarified_category_boundary", ""
    if scenario_id == "S11":
        pre = _spec("C05_S2", "label_a", "supports", "low", "Human pre has no alternative.", "no")
        post = pre | {"alternative_pathway_present": "yes", "alternative_mechanism": "qualifies", "alternative_note": "New alternative after review.", "uncertainty_flag": "medium"}
        return pre, post, "ai_persuaded_interpretive_change", ""
    if scenario_id in {"S12", "S13"}:
        pre = _spec("C06_S2", "label_b", "qualifies", "medium", "Human pre alternative remains present.", "yes", "supports", "Original alternative note.")
        post = pre | {"alternative_mechanism": "qualifies", "alternative_note": "AI_C06 alternative note.", "rationale_note": "Human modifies the retained alternative."}
        return pre, post, "ai_clarified_category_boundary", ""
    if scenario_id == "S14":
        pre = _spec("C01_S3", "label_c", "contradicts", "high", "Human rejects AI despite disagreement.", "no")
        return pre, pre, "rejected_ai_output", ""
    if scenario_id == "S15":
        pre = _spec("C02_S1", "label_a", "supports", "medium", "Human changes after rereading.", "no")
        post = pre | {"function_label": "label_c", "primary_evidence_segment_ids": "C02_S1|C02_S4", "rationale_note": "Human reports rereading drove the change."}
        return pre, post, "changed_after_rereading_not_ai", ""
    if scenario_id == "S16":
        pre = _spec("C05_S1", "label_a", "supports", "medium", "Control pre record changes on second pass.", "no")
        post = pre | {"function_label": "label_b", "primary_evidence_segment_ids": "C05_S1|C05_S3", "rationale_mechanism": "qualifies", "uncertainty_flag": "high", "rationale_note": "Control changed after rereading without AI."}
        return pre, post, "changed_after_rereading_not_ai", ""
    if scenario_id == "S17":
        pre = _spec("C05_S1", "label_a", "supports", "medium", "Human pre rationale differs.", "no")
        post = pre | {"primary_evidence_segment_ids": "C05_S1|C05_S2", "rationale_note": "AI_C05 repeated phrase exact copied wording appears here with human additions."}
        return pre, post, "mixed_or_unclear", ""
    if scenario_id == "S19":
        post = ai.copy()
        return _spec("C06_S1", "label_a", "supports", "high", "Human pre differs before identical AI-like post.", "no"), post, "ai_persuaded_interpretive_change", ""
    if scenario_id == "S20":
        pre = _spec("C06_S1", "label_a", "supports", "medium", "No change control record.", "no")
        return pre, pre, "not_applicable", ""
    raise ValueError(f"Unknown scenario_id {scenario_id}")


def _spec(
    evidence: str,
    label: str,
    mechanism: str,
    uncertainty: str,
    note: str,
    alternative_present: str,
    alternative_mechanism: str = "",
    alternative_note: str = "",
) -> dict[str, str]:
    return {
        "primary_evidence_segment_ids": evidence,
        "function_label": label,
        "rationale_mechanism": mechanism,
        "uncertainty_flag": uncertainty,
        "rationale_note": note,
        "alternative_pathway_present": alternative_present,
        "alternative_mechanism": alternative_mechanism,
        "alternative_note": alternative_note,
        "status": "locked",
    }


def _core_row(annotation_id: str, case_id: str, parent_id: str, actor_id: str, actor_type: str, stage: str, **spec: str) -> dict[str, str]:
    return {
        "annotation_id": annotation_id,
        "case_id": case_id,
        "parent_annotation_id": parent_id,
        "actor_id": actor_id,
        "actor_type": actor_type,
        "annotation_stage": stage,
        **spec,
    }


def _pre_provenance(annotation_id: str, case_id: str, participant_id: str) -> dict[str, str]:
    return _prov_base(annotation_id, "", case_id, participant_id, "human", "human_pre", lock_status="locked")


def _ai_provenance(annotation_id: str, case_id: str) -> dict[str, str]:
    row = _prov_base(annotation_id, "", case_id, "AI_SYNTH", "model", "ai_independent", lock_status="locked")
    row.update(
        {
            "model_provider": "synthetic_provider",
            "model_name": "synthetic_trim_haa_model",
            "model_version_or_date": "synthetic-v1",
            "prompt_template_id": "PROMPT_SYNTH_V1",
            "prompt_hash": "a" * 64,
            "model_run_id": f"RUN_{case_id}",
            "temperature_or_sampling": "temperature=0",
            "output_components_shown": "full_core_record",
        }
    )
    return row


def _post_provenance(annotation_id: str, parent_id: str, case_id: str, participant_id: str, ai_id: str, run_id: str, pre: dict[str, str], post: dict[str, str], reason: str, reason_note: str) -> dict[str, str]:
    row = _prov_base(annotation_id, parent_id, case_id, participant_id, "human", "human_post_ai", lock_status="locked")
    row.update(
        {
            "pre_ai_annotation_locked": "yes",
            "ai_output_exposed": "full_core_record",
            "exposure_order": "human_first",
            "interface_condition": "ai_review",
            "output_components_shown": "label evidence mechanism uncertainty rationale alternative",
            "exposure_timestamp": "2026-07-01T01:00:00+00:00",
            "post_edit_timestamp": "2026-07-01T01:10:00+00:00",
            "exposed_ai_annotation_id": ai_id,
            "exposed_model_run_id": run_id,
            "self_reported_revision_reason": reason,
            "self_reported_revision_note": reason_note,
            "changed_label": _changed(pre["function_label"], post["function_label"]),
            "changed_primary_evidence": _changed(pre["primary_evidence_segment_ids"], post["primary_evidence_segment_ids"]),
            "changed_rationale_mechanism": _changed(pre["rationale_mechanism"], post["rationale_mechanism"]),
            "changed_uncertainty": _changed(pre["uncertainty_flag"], post["uncertainty_flag"]),
            "changed_alternative": _changed(pre["alternative_pathway_present"], post["alternative_pathway_present"]),
        }
    )
    return row


def _control_provenance(annotation_id: str, parent_id: str, case_id: str, participant_id: str, pre: dict[str, str], post: dict[str, str], reason: str, reason_note: str) -> dict[str, str]:
    row = _prov_base(annotation_id, parent_id, case_id, participant_id, "human", "human_second_pass_control", lock_status="locked")
    row.update(
        {
            "pre_ai_annotation_locked": "yes",
            "exposure_order": "control_second_pass",
            "interface_condition": "control_review",
            "post_edit_timestamp": "2026-07-01T01:10:00+00:00",
            "self_reported_revision_reason": reason,
            "self_reported_revision_note": reason_note,
            "changed_label": _changed(pre["function_label"], post["function_label"]),
            "changed_primary_evidence": _changed(pre["primary_evidence_segment_ids"], post["primary_evidence_segment_ids"]),
            "changed_rationale_mechanism": _changed(pre["rationale_mechanism"], post["rationale_mechanism"]),
            "changed_uncertainty": _changed(pre["uncertainty_flag"], post["uncertainty_flag"]),
            "changed_alternative": _changed(pre["alternative_pathway_present"], post["alternative_pathway_present"]),
        }
    )
    return row


def _prov_base(annotation_id: str, parent_id: str, case_id: str, actor_id: str, actor_type: str, stage: str, *, lock_status: str) -> dict[str, str]:
    return {
        "annotation_id": annotation_id,
        "parent_annotation_id": parent_id,
        "case_id": case_id,
        "actor_id": actor_id,
        "actor_type": actor_type,
        "annotation_stage": stage,
        "pre_ai_annotation_locked": "not_applicable",
        "ai_output_exposed": "none",
        "exposure_order": "none",
        "interface_condition": "independent",
        "model_provider": "",
        "model_name": "",
        "model_version_or_date": "",
        "prompt_template_id": "",
        "prompt_hash": "",
        "system_prompt_hash": "",
        "model_run_id": "",
        "retry_count": "0",
        "regenerated_output": "no",
        "temperature_or_sampling": "",
        "output_components_shown": "",
        "exposure_timestamp": "",
        "post_edit_timestamp": "",
        "changed_label": "not_applicable",
        "changed_primary_evidence": "not_applicable",
        "changed_rationale_mechanism": "not_applicable",
        "changed_uncertainty": "not_applicable",
        "changed_alternative": "not_applicable",
        "exposed_ai_annotation_id": "",
        "exposed_model_run_id": "",
        "self_reported_revision_reason": "not_applicable",
        "self_reported_revision_note": "",
        "prior_access_to_other_annotations": "none",
        "lock_status": lock_status,
    }


def _exposure_event(event_id: str, post_id: str, pre_id: str, ai_id: str, run_id: str, case_id: str, sequence: str) -> dict[str, str]:
    return {
        "exposure_event_id": event_id,
        "human_post_annotation_id": post_id,
        "human_pre_annotation_id": pre_id,
        "ai_annotation_id": ai_id,
        "model_run_id": run_id,
        "case_id": case_id,
        "exposure_sequence": sequence,
        "output_components_shown": "label evidence mechanism uncertainty rationale alternative",
        "exposure_timestamp": "2026-07-01T01:00:00+00:00",
        "interface_condition": "ai_review",
        "notes": "Synthetic exposure event.",
    }


def _model_run_rows() -> list[dict[str, str]]:
    return [
        {
            "model_run_id": f"RUN_C{i:02d}",
            "provider": "synthetic_provider",
            "model_name": "synthetic_trim_haa_model",
            "model_version_or_date": "synthetic-v1",
            "run_timestamp": "2026-07-01T00:30:00+00:00",
            "prompt_template_id": "PROMPT_SYNTH_V1",
            "prompt_hash": "a" * 64,
            "system_prompt_hash": "",
            "temperature_or_sampling": "temperature=0",
            "retry_count": "0",
            "regenerated_output": "no",
            "tool_access": "none",
            "conversation_context_description": "Synthetic source packet only.",
            "output_file": f"synthetic_outputs/AI_C{i:02d}.json",
            "output_sha256": "b" * 64,
            "notes": "Synthetic model run; no live API call.",
        }
        for i in range(1, 7)
    ]


def _prompt_rows() -> list[dict[str, str]]:
    return [
        {
            "prompt_template_id": "PROMPT_SYNTH_V1",
            "prompt_version": "v1",
            "prompt_purpose": "Synthetic TRIM-HAA Core AI record generation.",
            "prompt_text_path": "prompts/synthetic_trim_haa_core_v1.txt",
            "prompt_sha256": "a" * 64,
            "created_at": "2026-07-01T00:00:00+00:00",
            "frozen": "yes",
            "notes": "Synthetic manifest only; no secret prompt.",
        }
    ]


def _changed(left: str, right: str) -> str:
    return "yes" if left != right else "no"


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _find(rows: list[dict[str, str]], field: str, value: str) -> dict[str, str]:
    for row in rows:
        if row[field] == value:
            return row
    raise ValueError(f"Missing {field}={value}")


def _readme_text() -> str:
    return """# TRIM-HAA synthetic dry run v0.1

This package is entirely synthetic. It contains no historical human coder
answers and no live model output.

Expected design:

- 4 synthetic participants;
- 6 synthetic cases;
- 24 human-pre records;
- 6 AI records;
- 16 human-post-AI records;
- 8 human second-pass control records.

The package is designed to test representation, validation, comparison,
reporting, cryptographic pre-lock verification, explicit exposed-AI linkage,
and cautionary warnings before any human pilot.
"""


if __name__ == "__main__":
    raise SystemExit(main())
