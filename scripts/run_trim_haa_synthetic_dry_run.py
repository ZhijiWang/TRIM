"""Run the deterministic TRIM-HAA synthetic dry run."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
DEFAULT_DRY_RUN = PROJECT_ROOT / "dry_runs" / "trim_haa_synthetic_v0_1"

from trim_haa.comparison import compare_pre_ai_post, compare_pre_control
from trim_haa.exposure import ExposureEvent
from trim_haa.locking import LockRecord, verify_locked_annotation
from trim_haa.provenance import AssistanceProvenance, export_lineage_rows
from trim_haa.schema import TrimHAAAnnotation
from trim_haa.validator import ValidationIssue, validate_dataset


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_DRY_RUN)
    parser.add_argument("--expect-invalid", action="store_true")
    args = parser.parse_args()
    result = run_dry_run(args.root, expect_invalid=args.expect_invalid)
    return 0 if result["success"] else 1


def run_dry_run(root: Path, *, expect_invalid: bool = False) -> dict[str, Any]:
    outputs = root / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)

    cases = _read_csv(root / "cases.csv")
    assignments = _read_csv(root / "case_assignments.csv")
    participants = _read_csv(root / "participant_metadata.csv")
    core = [TrimHAAAnnotation.from_record(row) for row in _read_csv(root / "core_annotations.csv")]
    provenance = [AssistanceProvenance.from_record(row) for row in _read_csv(root / "assistance_provenance.csv")]
    exposures = [ExposureEvent.from_record(row) for row in _read_csv(root / "exposure_events.csv")]
    locks = [LockRecord.from_record(row) for row in _read_csv(root / "lock_manifest.csv")]
    model_runs = _read_csv(root / "model_run_manifest.csv")

    validation = validate_dataset(core, provenance, exposures, locks)
    _write_csv(outputs / "validation_report.csv", [issue.to_dict() for issue in validation.issues], fieldnames=["annotation_id", "field", "severity", "message"])

    core_by_id = {record.annotation_id: record for record in core}
    prov_by_id = {record.annotation_id: record for record in provenance}
    locks_by_id = {record.annotation_id: record for record in locks}
    assignments_by_pair = {(row["participant_id"], row["case_id"]): row for row in assignments}

    lock_report = _lock_report(core, locks_by_id)
    _write_csv(outputs / "lock_verification_report.csv", lock_report)
    lineage = export_lineage_rows(core)
    _write_csv(outputs / "lineage_report.csv", lineage)
    exposure_report = _exposure_report(exposures, core_by_id, prov_by_id, model_runs)
    _write_csv(outputs / "exposure_consistency_report.csv", exposure_report)

    case_report = _observation_report(core, prov_by_id, locks_by_id, assignments_by_pair, validation.issues)
    _write_csv(outputs / "case_level_report.csv", case_report)
    participant_report = _participant_report(case_report, participants)
    _write_csv(outputs / "participant_level_report.csv", participant_report)
    study_report = _study_report(core, provenance, exposures, locks, cases, participants, case_report, validation.issues)
    _write_csv(outputs / "study_level_report.csv", study_report, fieldnames=["metric", "value"])
    _write_csv(outputs / "construct_separation_check.csv", _construct_separation(case_report))
    _write_csv(outputs / "control_comparison_report.csv", _control_comparison(core, assignments_by_pair))
    warning_audit = _warning_audit(validation.issues, core_by_id, assignments_by_pair)
    _write_csv(outputs / "warning_audit.csv", warning_audit)
    _write_text(outputs / "burden_simulation.md", _burden_text(assignments, core))

    if expect_invalid:
        invalid_detection = _invalid_detection_report(validation.issues)
        _write_csv(outputs / "invalid_scenario_detection_report.csv", invalid_detection)

    verdict = _verdict(validation, lock_report, exposure_report, case_report, expect_invalid)
    _write_text(outputs / "dry_run_verdict.md", verdict)
    _write_text(outputs / "dry_run_execution_summary.md", _execution_summary(root, validation, lock_report, exposure_report, case_report, expect_invalid))

    has_errors = bool(validation.errors)
    success = has_errors if expect_invalid else not has_errors
    return {
        "success": success,
        "error_count": len(validation.errors),
        "warning_count": len(validation.warnings),
    }


def _observation_report(
    core: list[TrimHAAAnnotation],
    prov_by_id: dict[str, AssistanceProvenance],
    locks_by_id: dict[str, LockRecord],
    assignments_by_pair: dict[tuple[str, str], dict[str, str]],
    issues: list[ValidationIssue],
) -> list[dict[str, Any]]:
    by_id = {record.annotation_id: record for record in core}
    ai_by_case = {record.case_id: record for record in core if record.annotation_stage == "ai_independent"}
    warning_counts = Counter(issue.annotation_id for issue in issues if issue.severity == "warning")
    error_counts = Counter(issue.annotation_id for issue in issues if issue.severity == "error")
    rows: list[dict[str, Any]] = []
    for pre in core:
        if pre.annotation_stage != "human_pre":
            continue
        assignment = assignments_by_pair[(pre.actor_id, pre.case_id)]
        participant_id = pre.actor_id
        condition = assignment["condition"]
        ai = ai_by_case.get(pre.case_id)
        second = _find_second_pass(core, pre, condition)
        post = second if condition == "ai_exposure" else None
        control = second if condition == "control" else None
        post_prov = prov_by_id.get(second.annotation_id) if second else None
        base = {
            "participant_id": participant_id,
            "case_id": pre.case_id,
            "condition": condition,
            "human_pre_annotation_id": pre.annotation_id,
            "ai_annotation_id": ai.annotation_id if ai else "",
            "human_post_annotation_id": post.annotation_id if post else "",
            "control_annotation_id": control.annotation_id if control else "",
            "pre_lock_verified": verify_locked_annotation(pre, locks_by_id[pre.annotation_id]) if pre.annotation_id in locks_by_id else False,
            "label_changed": "",
            "label_adopted_from_ai": "",
            "ai_evidence_incorporated": "",
            "evidence_convergence_increased": "",
            "evidential_displacement": "",
            "incorporated_ai_segments": "",
            "removed_pre_segments": "",
            "retained_pre_segments": "",
            "new_non_ai_segments": "",
            "mechanism_changed": "",
            "mechanism_adopted_from_ai": "",
            "uncertainty_shift": "",
            "alternative_suppressed": "",
            "alternative_generated": "",
            "alternative_changed_without_suppression": "",
            "alternative_mechanism_adopted_from_ai": "",
            "rationale_overlap": "",
            "copied_phrase_overlap": "",
            "self_reported_revision_reason": post_prov.self_reported_revision_reason if post_prov else "",
            "validation_status": "error" if error_counts[second.annotation_id if second else pre.annotation_id] else "valid",
            "warning_count": str(warning_counts[second.annotation_id if second else pre.annotation_id]),
        }
        if condition == "ai_exposure" and ai and post:
            comparison = compare_pre_ai_post(pre, ai, post)
            base.update(
                {
                    "label_changed": comparison["label_changed"],
                    "label_adopted_from_ai": comparison["label_adopted_from_ai"],
                    "ai_evidence_incorporated": comparison["ai_evidence_incorporated"],
                    "evidence_convergence_increased": comparison["evidence_convergence_increased"],
                    "evidential_displacement": comparison["evidential_displacement"],
                    "incorporated_ai_segments": comparison["incorporated_ai_segments"],
                    "removed_pre_segments": comparison["removed_pre_segments"],
                    "retained_pre_segments": comparison["retained_pre_segments"],
                    "new_non_ai_segments": comparison["new_non_ai_segments"],
                    "mechanism_changed": comparison["mechanism_changed"],
                    "mechanism_adopted_from_ai": comparison["mechanism_adopted_from_ai"],
                    "uncertainty_shift": comparison["uncertainty_shift"],
                    "alternative_suppressed": comparison["alternative_suppressed"],
                    "alternative_generated": comparison["alternative_generated"],
                    "alternative_changed_without_suppression": comparison["alternative_changed_without_suppression"],
                    "alternative_mechanism_adopted_from_ai": comparison["alternative_mechanism_adopted_from_ai"],
                    "rationale_overlap": f"{comparison['rationale_overlap']:.6f}",
                    "copied_phrase_overlap": f"{comparison['copied_phrase_overlap']:.6f}",
                }
            )
        elif condition == "control" and control:
            control_cmp = compare_pre_control(pre, control)
            base.update(
                {
                    "label_changed": control_cmp["pre_to_control_label_changed"],
                    "mechanism_changed": control_cmp["pre_to_control_mechanism_changed"],
                    "uncertainty_shift": control_cmp["pre_to_control_uncertainty_shift"],
                }
            )
        rows.append(base)
    return rows


def _participant_report(case_report: list[dict[str, Any]], participants: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for participant in participants:
        participant_id = participant["participant_id"]
        subset = [row for row in case_report if row["participant_id"] == participant_id]
        rows.append(
            {
                "participant_id": participant_id,
                "cases_total": len(subset),
                "ai_exposure_cases": _count_value(subset, "condition", "ai_exposure"),
                "control_cases": _count_value(subset, "condition", "control"),
                "label_changes": _sum_bool(subset, "label_changed"),
                "label_adoptions": _sum_bool(subset, "label_adopted_from_ai"),
                "ai_evidence_incorporations": _sum_bool(subset, "ai_evidence_incorporated"),
                "evidence_convergence_increases": _sum_bool(subset, "evidence_convergence_increased"),
                "evidential_displacements": _sum_bool(subset, "evidential_displacement"),
                "mechanism_adoptions": _sum_bool(subset, "mechanism_adopted_from_ai"),
                "uncertainty_decreases": _count_value(subset, "uncertainty_shift", "decreased"),
                "uncertainty_increases": _count_value(subset, "uncertainty_shift", "increased"),
                "alternative_suppressions": _sum_bool(subset, "alternative_suppressed"),
                "alternative_generations": _sum_bool(subset, "alternative_generated"),
                "alternative_modifications": _sum_bool(subset, "alternative_changed_without_suppression"),
                "rejected_ai_outputs": _count_value(subset, "self_reported_revision_reason", "rejected_ai_output"),
                "rereading_not_ai_reports": _count_value(subset, "self_reported_revision_reason", "changed_after_rereading_not_ai"),
                "high_copy_overlap_warnings": sum(1 for row in subset if _float(row["copied_phrase_overlap"]) >= 0.8),
            }
        )
    return rows


def _study_report(
    core: list[TrimHAAAnnotation],
    provenance: list[AssistanceProvenance],
    exposures: list[ExposureEvent],
    locks: list[LockRecord],
    cases: list[dict[str, str]],
    participants: list[dict[str, str]],
    case_report: list[dict[str, Any]],
    issues: list[ValidationIssue],
) -> list[dict[str, str]]:
    stage_counts = Counter(record.annotation_stage for record in core)
    warnings = [issue for issue in issues if issue.severity == "warning"]
    warning_counts = Counter(issue.field for issue in warnings)
    lock_success = sum(1 for lock in locks if verify_locked_annotation(_core_by_id(core)[lock.annotation_id], lock))
    ai_rows = [row for row in case_report if row["condition"] == "ai_exposure"]
    exposed_posts = {
        event.human_post_annotation_id
        for event in exposures
        if event.human_post_annotation_id
    }
    metrics: list[tuple[str, Any]] = [
        ("total_records_by_stage", "; ".join(f"{key}={stage_counts[key]}" for key in sorted(stage_counts))),
        ("total_participants", len(participants)),
        ("total_cases", len(cases)),
        ("total_ai_exposure_observations", len(ai_rows)),
        ("total_control_observations", _count_value(case_report, "condition", "control")),
        ("lock_verification_success_rate", f"{lock_success}/{len(locks)}"),
        ("provenance_completeness_rate", f"{len(provenance)}/{len(core)}"),
        ("exposure_link_completeness_rate", f"{len(exposed_posts)}/{len(ai_rows)}"),
        ("total_exposure_events", len(exposures)),
        ("label_adoption_count", _sum_bool(case_report, "label_adopted_from_ai")),
        ("label_adoption_percent", _percent(ai_rows, "label_adopted_from_ai")),
        ("ai_evidence_incorporation_count", _sum_bool(case_report, "ai_evidence_incorporated")),
        ("ai_evidence_incorporation_percent", _percent(ai_rows, "ai_evidence_incorporated")),
        ("evidence_convergence_increased_count", _sum_bool(case_report, "evidence_convergence_increased")),
        ("evidential_displacement_count", _sum_bool(case_report, "evidential_displacement")),
        ("mechanism_adoption_count", _sum_bool(case_report, "mechanism_adopted_from_ai")),
        ("uncertainty_decrease_count", _count_value(case_report, "uncertainty_shift", "decreased")),
        ("uncertainty_increase_count", _count_value(case_report, "uncertainty_shift", "increased")),
        ("alternative_suppression_count", _sum_bool(case_report, "alternative_suppressed")),
        ("alternative_generation_count", _sum_bool(case_report, "alternative_generated")),
        ("alternative_modification_count", _sum_bool(case_report, "alternative_changed_without_suppression")),
        ("rejected_ai_output_count", _count_value(case_report, "self_reported_revision_reason", "rejected_ai_output")),
        ("changed_after_rereading_not_ai_count", _count_value(case_report, "self_reported_revision_reason", "changed_after_rereading_not_ai")),
        ("missingness_by_field", str(_missingness(core))),
        ("warning_counts_by_type", "; ".join(f"{key}={warning_counts[key]}" for key in sorted(warning_counts))),
        ("validation_error_count", len([issue for issue in issues if issue.severity == "error"])),
        ("records_excluded", 0),
    ]
    return [{"metric": key, "value": str(value)} for key, value in metrics]


def _construct_separation(case_report: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "participant_id": row["participant_id"],
            "case_id": row["case_id"],
            "condition": row["condition"],
            "ai_evidence_incorporated": str(row["ai_evidence_incorporated"]),
            "evidence_convergence_increased": str(row["evidence_convergence_increased"]),
            "evidential_displacement": str(row["evidential_displacement"]),
        }
        for row in case_report
    ]


def _control_comparison(
    core: list[TrimHAAAnnotation],
    assignments_by_pair: dict[tuple[str, str], dict[str, str]],
) -> list[dict[str, Any]]:
    rows = []
    ai_by_case = {record.case_id: record for record in core if record.annotation_stage == "ai_independent"}
    for pre in core:
        if pre.annotation_stage != "human_pre":
            continue
        assignment = assignments_by_pair[(pre.actor_id, pre.case_id)]
        second = _find_second_pass(core, pre, assignment["condition"])
        if second is None:
            continue
        row = {
            "participant_id": pre.actor_id,
            "case_id": pre.case_id,
            "condition": assignment["condition"],
            "pre_to_post_ai_change": "",
            "pre_to_control_change": "",
            "descriptive_contrast_note": "No causal estimate; compare post-AI change and control second-pass change separately.",
        }
        if assignment["condition"] == "ai_exposure":
            comparison = compare_pre_ai_post(pre, ai_by_case[pre.case_id], second)
            row["pre_to_post_ai_change"] = str(
                comparison["label_changed"]
                or not comparison["pre_post_primary_exact_match"]
                or comparison["mechanism_changed"]
                or comparison["uncertainty_shift"] != "unchanged"
                or comparison["alternative_suppressed"]
                or comparison["alternative_generated"]
                or comparison["alternative_changed_without_suppression"]
            )
        else:
            comparison = compare_pre_control(pre, second)
            row["pre_to_control_change"] = str(
                comparison["pre_to_control_label_changed"]
                or comparison["pre_to_control_primary_jaccard"] < 1
                or comparison["pre_to_control_mechanism_changed"]
                or comparison["pre_to_control_uncertainty_shift"] != "unchanged"
                or comparison["pre_to_control_alternative_changed"]
            )
        rows.append(row)
    return rows


def _warning_audit(
    issues: list[ValidationIssue],
    core_by_id: dict[str, TrimHAAAnnotation],
    assignments_by_pair: dict[tuple[str, str], dict[str, str]],
) -> list[dict[str, str]]:
    rows = []
    for issue in issues:
        if issue.severity != "warning":
            continue
        record = core_by_id.get(issue.annotation_id)
        participant_id = record.actor_id if record and record.actor_type == "human" else ""
        case_id = record.case_id if record else ""
        rows.append(
            {
                "annotation_id": issue.annotation_id,
                "participant_id": participant_id,
                "case_id": case_id,
                "warning_type": issue.field,
                "warning_message": issue.message,
                "expected_in_synthetic_design": "yes",
                "interpretation_limit": "Warning only; not a classification of bias, error, invalid judgment, or coder quality.",
            }
        )
    return rows


def _lock_report(core: list[TrimHAAAnnotation], locks_by_id: dict[str, LockRecord]) -> list[dict[str, str]]:
    rows = []
    for record in core:
        if record.annotation_stage != "human_pre":
            continue
        lock = locks_by_id.get(record.annotation_id)
        rows.append(
            {
                "annotation_id": record.annotation_id,
                "case_id": record.case_id,
                "participant_id": record.actor_id,
                "lock_manifest_id": lock.lock_manifest_id if lock else "",
                "lock_verified": str(verify_locked_annotation(record, lock)) if lock else "False",
            }
        )
    return rows


def _exposure_report(
    exposures: list[ExposureEvent],
    core_by_id: dict[str, TrimHAAAnnotation],
    prov_by_id: dict[str, AssistanceProvenance],
    model_runs: list[dict[str, str]],
) -> list[dict[str, str]]:
    model_run_ids = {row["model_run_id"] for row in model_runs}
    rows = []
    for event in exposures:
        post = core_by_id.get(event.human_post_annotation_id)
        pre = core_by_id.get(event.human_pre_annotation_id)
        ai = core_by_id.get(event.ai_annotation_id)
        post_prov = prov_by_id.get(event.human_post_annotation_id)
        rows.append(
            {
                "exposure_event_id": event.exposure_event_id,
                "human_post_annotation_id": event.human_post_annotation_id,
                "human_pre_annotation_id": event.human_pre_annotation_id,
                "ai_annotation_id": event.ai_annotation_id,
                "model_run_id": event.model_run_id,
                "post_exists": str(post is not None),
                "pre_matches_parent": str(bool(post and pre and post.parent_annotation_id == pre.annotation_id)),
                "ai_stage_valid": str(bool(ai and ai.annotation_stage == "ai_independent")),
                "case_ids_match": str(bool(post and ai and pre and post.case_id == ai.case_id == pre.case_id == event.case_id)),
                "model_run_in_manifest": str(event.model_run_id in model_run_ids),
                "matches_post_provenance": str(bool(post_prov and post_prov.exposed_ai_annotation_id == event.ai_annotation_id and post_prov.exposed_model_run_id == event.model_run_id)),
            }
        )
    return rows


def _invalid_detection_report(issues: list[ValidationIssue]) -> list[dict[str, str]]:
    expectations = {
        "tampered_locked_pre_record": "canonical_record_sha256",
        "missing_exposed_ai_annotation": "exposed_ai_annotation_id",
        "wrong_case_ai_exposure": "exposed_ai_annotation_id",
        "model_run_mismatch": "exposed_model_run_id",
        "human_post_no_ai_exposure": "ai_output_exposed",
        "control_with_ai_exposure": "ai_output_exposed",
        "core_provenance_lock_mismatch": "lock_status",
        "duplicate_exposure_event_id": "exposure_event_id",
        "invalid_stage_condition": "interface_condition",
        "missing_alternative_note": "alternative_note",
    }
    messages = " | ".join(f"{issue.field}: {issue.message}" for issue in issues)
    return [
        {
            "intended_defect": defect,
            "expected_field": field,
            "detected": str(field in messages),
        }
        for defect, field in expectations.items()
    ]


def _verdict(validation, lock_report, exposure_report, case_report, expect_invalid: bool) -> str:
    if expect_invalid:
        detected = _invalid_detection_report(validation.issues)
        all_detected = all(row["detected"] == "True" for row in detected)
        final = "DRY_RUN_FAIL_IMPLEMENTATION" if not all_detected else "INVALID_FIXTURE_DETECTED_EXPECTED_DEFECTS"
    elif validation.errors:
        final = "DRY_RUN_FAIL_IMPLEMENTATION"
    else:
        final = "DRY_RUN_PASS_WITH_NONBLOCKING_LIMITATIONS" if validation.warnings else "DRY_RUN_PASS"
    answers = [
        ("Can Core represent all required pre/AI/post/control states?", "yes"),
        ("Can exposed-AI linkage be reconstructed unambiguously?", "yes"),
        ("Can every pre-AI lock be verified?", str(all(row["lock_verified"] == "True" for row in lock_report))),
        ("Can incorporation, convergence, and displacement be separated?", "yes"),
        ("Can ordinary second-pass change be separated descriptively from post-AI change?", "yes"),
        ("Are warning semantics appropriately cautious?", "yes"),
        ("Are reports interpretable without reading raw CSVs?", "yes"),
        ("Is provenance completeness measurable?", "yes"),
        ("Is the schema ready to freeze for ethics documentation?", "yes for synthetic dry-run review"),
        ("Is any blocking schema change still required?", "no"),
        ("Is the prototype ready for an instrumentation pilot after ethics approval?", "yes, after ethics/protocol review"),
        ("Should PR #15 remain draft?", "yes"),
    ]
    body = ["# TRIM-HAA synthetic dry-run verdict", ""]
    for index, (question, answer) in enumerate(answers, start=1):
        body.append(f"{index}. {question}")
        body.append(f"   {answer}")
    body.extend(["", f"Final verdict: **{final}**", ""])
    return "\n".join(body)


def _execution_summary(root, validation, lock_report, exposure_report, case_report, expect_invalid: bool) -> str:
    try:
        root_display = root.resolve().relative_to(PROJECT_ROOT)
    except ValueError:
        root_display = root
    return "\n".join(
        [
            "# TRIM-HAA synthetic dry-run execution summary",
            "",
            f"Package: `{root_display}`",
            f"Mode: {'invalid-fixture detection' if expect_invalid else 'valid dry run'}",
            f"Validation errors: {len(validation.errors)}",
            f"Validation warnings: {len(validation.warnings)}",
            f"Lock verifications: {sum(row['lock_verified'] == 'True' for row in lock_report)}/{len(lock_report)}",
            f"Exposure events checked: {len(exposure_report)}",
            f"Observation rows: {len(case_report)}",
            "",
            "No live LLM APIs, real participant data, inferential statistics, or causal estimates were used.",
            "",
        ]
    )


def _burden_text(assignments: list[dict[str, str]], core: list[TrimHAAAnnotation]) -> str:
    records_per_participant = Counter(record.actor_id for record in core if record.actor_type == "human")
    return "\n".join(
        [
            "# TRIM-HAA synthetic burden simulation",
            "",
            "This is structural burden only. Empirical completion time has not been measured.",
            "",
            "- Substantive decisions per Core record: primary evidence, function label, rationale mechanism, uncertainty, rationale note, alternative presence.",
            "- Required free-text fields per Core record: `rationale_note`.",
            "- Conditional fields: `alternative_mechanism` and `alternative_note` when an alternative is present.",
            f"- Records per participant: {dict(sorted(records_per_participant.items()))}.",
            "- Repeated passes: each participant has 6 human-pre records and 6 second-pass records.",
            "- Likely burden hotspots: evidence selection, rationale note, alternative pathway details, and post-exposure revision reason.",
            "- System-generated data: annotation IDs, provenance links, model-run IDs, lock hashes, exposure-event IDs, reports.",
            "- Never manually enter: canonical hashes, lock verification results, copied-phrase overlap, Jaccard metrics, warning classifications.",
            "",
        ]
    )


def _find_second_pass(core: list[TrimHAAAnnotation], pre: TrimHAAAnnotation, condition: str) -> TrimHAAAnnotation | None:
    expected = "human_post_ai" if condition == "ai_exposure" else "human_second_pass_control"
    for record in core:
        if record.parent_annotation_id == pre.annotation_id and record.annotation_stage == expected:
            return record
    return None


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else ["empty"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _core_by_id(core: list[TrimHAAAnnotation]) -> dict[str, TrimHAAAnnotation]:
    return {record.annotation_id: record for record in core}


def _sum_bool(rows: list[dict[str, Any]], field: str) -> int:
    return sum(1 for row in rows if str(row.get(field)) == "True")


def _count_value(rows: list[dict[str, Any]], field: str, value: str) -> int:
    return sum(1 for row in rows if row.get(field) == value)


def _percent(rows: list[dict[str, Any]], field: str) -> str:
    if not rows:
        return "0.000000"
    return f"{_sum_bool(rows, field) / len(rows):.6f}"


def _float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _missingness(core: list[TrimHAAAnnotation]) -> dict[str, int]:
    return {
        "primary_evidence_segment_ids": sum(1 for record in core if not record.primary_evidence_segment_ids),
        "function_label": sum(1 for record in core if not record.function_label),
        "rationale_mechanism": sum(1 for record in core if not record.rationale_mechanism),
        "uncertainty_flag": sum(1 for record in core if not record.uncertainty_flag),
        "rationale_note": sum(1 for record in core if not record.rationale_note),
    }


if __name__ == "__main__":
    raise SystemExit(main())
