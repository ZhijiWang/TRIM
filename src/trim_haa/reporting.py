"""Descriptive TRIM-HAA reports."""

from __future__ import annotations

from statistics import mean, median
from typing import TYPE_CHECKING, Any, Iterable, Mapping

if TYPE_CHECKING:
    import pandas as pd

from trim_haa.comparison import compare_pre_ai_post
from trim_haa.locking import LockRecord, verify_locked_annotation
from trim_haa.provenance import AssistanceProvenance
from trim_haa.schema import TrimHAAAnnotation
from trim_haa.validator import validate_dataset


def case_level_report(
    annotations: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
    provenance_records: Iterable[AssistanceProvenance | Mapping[str, Any]] = (),
    lock_records: Iterable[LockRecord | Mapping[str, Any]] = (),
) -> pd.DataFrame:
    pd = _pandas()
    rows: list[dict[str, Any]] = []
    prepared = [_coerce(record) for record in annotations]
    by_case = _by_case(prepared)
    prov_by_id = _provenance_by_id(provenance_records)
    lock_by_id = _lock_by_annotation(lock_records)
    for case_id, records in by_case.items():
        human_pre = _first_stage(records, "human_pre")
        ai = _first_stage(records, "ai_independent")
        post = _first_stage(records, "human_post_ai")
        control = _first_stage(records, "human_second_pass_control")
        post_prov = prov_by_id.get(post.annotation_id) if post else None
        row = {
            "case_id": case_id,
            "human_pre_annotation_id": _id(human_pre),
            "ai_annotation_id": _id(ai),
            "human_post_annotation_id": _id(post),
            "control_annotation_id": _id(control),
            "exposed_ai_annotation_id": post_prov.exposed_ai_annotation_id if post_prov else "",
            "exposed_model_run_id": post_prov.exposed_model_run_id if post_prov else "",
            "pre_lock_verified": (
                verify_locked_annotation(human_pre, lock_by_id[human_pre.annotation_id])
                if human_pre and human_pre.annotation_id in lock_by_id
                else False
            ),
            "self_reported_revision_reason": (
                post_prov.self_reported_revision_reason if post_prov else ""
            ),
        }
        if human_pre and ai and post:
            comparison = compare_pre_ai_post(human_pre, ai, post)
            row.update(
                {
                    "pre_label": comparison["pre_label"],
                    "ai_label": comparison["ai_label"],
                    "post_label": comparison["post_label"],
                    "label_changed": comparison["label_changed"],
                    "label_adoption": comparison["label_adopted_from_ai"],
                    "pre_ai_primary_jaccard": comparison["pre_ai_primary_jaccard"],
                    "pre_post_primary_jaccard": comparison["pre_post_primary_jaccard"],
                    "post_ai_primary_jaccard": comparison["post_ai_primary_jaccard"],
                    "ai_evidence_incorporated": comparison["ai_evidence_incorporated"],
                    "evidence_convergence_increased": comparison[
                        "evidence_convergence_increased"
                    ],
                    "evidential_displacement": comparison["evidential_displacement"],
                    "mechanism_adoption": comparison["mechanism_adopted_from_ai"],
                    "uncertainty_shift": comparison["uncertainty_shift"],
                    "alternative_suppression": comparison["alternative_suppressed"],
                    "alternative_generation": comparison["alternative_generated"],
                    "alternative_changed_without_suppression": comparison[
                        "alternative_changed_without_suppression"
                    ],
                    "alternative_mechanism_adopted_from_ai": comparison[
                        "alternative_mechanism_adopted_from_ai"
                    ],
                    "rationale_overlap": comparison["rationale_overlap"],
                    "copied_phrase_overlap": comparison["copied_phrase_overlap"],
                }
            )
        rows.append(row)
    return pd.DataFrame(rows, columns=CASE_LEVEL_COLUMNS)


def participant_level_report(
    annotations: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
    case_report: pd.DataFrame | None = None,
) -> pd.DataFrame:
    pd = _pandas()
    prepared = [_coerce(record) for record in annotations]
    case_report = case_report if case_report is not None else case_level_report(prepared)
    rows: list[dict[str, Any]] = []
    participant_ids = sorted(
        {
            record.actor_id
            for record in prepared
            if record.actor_type == "human" and record.annotation_stage == "human_pre"
        }
    )
    for participant_id in participant_ids:
        participant_pre = [
            record
            for record in prepared
            if record.actor_id == participant_id and record.annotation_stage == "human_pre"
        ]
        case_ids = {record.case_id for record in participant_pre}
        subset = case_report[case_report["case_id"].isin(case_ids)]
        rows.append(
            {
                "actor_id": participant_id,
                "number_of_cases": len(case_ids),
                "label_changes": _sum_bool(subset, "label_changed"),
                "label_adoptions": _sum_bool(subset, "label_adoption"),
                "evidence_adoptions": _sum_bool(subset, "ai_evidence_incorporated"),
                "mechanism_adoptions": _sum_bool(subset, "mechanism_adoption"),
                "uncertainty_shifts": int((subset["uncertainty_shift"] != "unchanged").sum())
                if "uncertainty_shift" in subset
                else 0,
                "alternative_suppression": _sum_bool(subset, "alternative_suppression"),
                "alternative_generation": _sum_bool(subset, "alternative_generation"),
                "mean_review_time": None,
            }
        )
    return pd.DataFrame(rows)


def study_level_report(
    annotations: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
    provenance_records: Iterable[Mapping[str, Any]] = (),
    exposure_events: Iterable[Mapping[str, Any]] = (),
    lock_records: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    pd = _pandas()
    prepared = [_coerce(record) for record in annotations]
    cases = case_level_report(prepared, provenance_records, lock_records)
    report = validate_dataset(prepared, provenance_records, exposure_events, lock_records)
    row_count = len(cases)
    jaccards = [
        float(value)
        for value in cases.get("post_ai_primary_jaccard", pd.Series(dtype=float)).dropna()
    ]
    return {
        "case_count": row_count,
        "annotation_count": len(prepared),
        "label_adoption_count": _sum_bool(cases, "label_adoption"),
        "label_adoption_percent": _percent(cases, "label_adoption"),
        "ai_evidence_incorporation_count": _sum_bool(cases, "ai_evidence_incorporated"),
        "ai_evidence_incorporation_percent": _percent(cases, "ai_evidence_incorporated"),
        "evidence_convergence_increased_count": _sum_bool(
            cases, "evidence_convergence_increased"
        ),
        "evidential_displacement_count": _sum_bool(cases, "evidential_displacement"),
        "mechanism_adoption_count": _sum_bool(cases, "mechanism_adoption"),
        "uncertainty_decrease_count": int(
            (cases.get("uncertainty_shift", pd.Series(dtype=str)) == "decreased").sum()
        ),
        "uncertainty_increase_count": int(
            (cases.get("uncertainty_shift", pd.Series(dtype=str)) == "increased").sum()
        ),
        "alternative_suppression_count": _sum_bool(cases, "alternative_suppression"),
        "alternative_generation_count": _sum_bool(cases, "alternative_generation"),
        "alternative_modification_count": _sum_bool(
            cases, "alternative_changed_without_suppression"
        ),
        "rejected_ai_output_count": int(
            (
                cases.get("self_reported_revision_reason", pd.Series(dtype=str))
                == "rejected_ai_output"
            ).sum()
        ),
        "changed_after_rereading_not_ai_count": int(
            (
                cases.get("self_reported_revision_reason", pd.Series(dtype=str))
                == "changed_after_rereading_not_ai"
            ).sum()
        ),
        "post_ai_primary_jaccard_mean": mean(jaccards) if jaccards else None,
        "post_ai_primary_jaccard_median": median(jaccards) if jaccards else None,
        "validation_issue_count": len(report.issues),
        "validation_error_count": len(report.errors),
        "validation_warning_count": len(report.warnings),
        "missingness": _missingness(prepared),
    }


CASE_LEVEL_COLUMNS: tuple[str, ...] = (
    "case_id",
    "human_pre_annotation_id",
    "ai_annotation_id",
    "human_post_annotation_id",
    "control_annotation_id",
    "exposed_ai_annotation_id",
    "exposed_model_run_id",
    "pre_lock_verified",
    "pre_label",
    "ai_label",
    "post_label",
    "label_changed",
    "label_adoption",
    "pre_ai_primary_jaccard",
    "pre_post_primary_jaccard",
    "post_ai_primary_jaccard",
    "ai_evidence_incorporated",
    "evidence_convergence_increased",
    "evidential_displacement",
    "mechanism_adoption",
    "uncertainty_shift",
    "alternative_suppression",
    "alternative_generation",
    "alternative_changed_without_suppression",
    "alternative_mechanism_adopted_from_ai",
    "rationale_overlap",
    "copied_phrase_overlap",
    "self_reported_revision_reason",
)


def _by_case(records: Iterable[TrimHAAAnnotation | Mapping[str, Any]]) -> dict[str, list[TrimHAAAnnotation]]:
    by_case: dict[str, list[TrimHAAAnnotation]] = {}
    for record in records:
        annotation = _coerce(record)
        by_case.setdefault(annotation.case_id, []).append(annotation)
    return by_case


def _first_stage(records: list[TrimHAAAnnotation], stage: str) -> TrimHAAAnnotation | None:
    matches = [record for record in records if record.annotation_stage == stage]
    if len(matches) > 1:
        identifiers = ", ".join(record.annotation_id for record in matches)
        raise ValueError(
            f"Case {matches[0].case_id!r} has multiple {stage!r} records: {identifiers}."
        )
    return matches[0] if matches else None


def _coerce(record: TrimHAAAnnotation | Mapping[str, Any]) -> TrimHAAAnnotation:
    if isinstance(record, TrimHAAAnnotation):
        return record
    return TrimHAAAnnotation.from_record(record)


def _id(record: TrimHAAAnnotation | None) -> str:
    return record.annotation_id if record else ""


def _provenance_by_id(
    records: Iterable[AssistanceProvenance | Mapping[str, Any]],
) -> dict[str, AssistanceProvenance]:
    by_id: dict[str, AssistanceProvenance] = {}
    for record in records:
        if not isinstance(record, AssistanceProvenance):
            record = AssistanceProvenance.from_record(record)
        by_id[record.annotation_id] = record
    return by_id


def _lock_by_annotation(
    records: Iterable[LockRecord | Mapping[str, Any]],
) -> dict[str, LockRecord]:
    by_id: dict[str, LockRecord] = {}
    for record in records:
        if not isinstance(record, LockRecord):
            record = LockRecord.from_record(record)
        by_id[record.annotation_id] = record
    return by_id


def _sum_bool(df: pd.DataFrame, column: str) -> int:
    if column not in df:
        return 0
    return sum(1 for value in df[column] if _is_explicit_true(value))


def _is_explicit_true(value: Any) -> bool:
    """Interpret report booleans without Python truthiness (for example, NaN)."""

    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1"}
    return False


def _percent(df: pd.DataFrame, column: str) -> float | None:
    if column not in df or df.empty:
        return None
    return _sum_bool(df, column) / len(df)


def _missingness(records: list[TrimHAAAnnotation]) -> dict[str, int]:
    counts = {
        "rationale_note": 0,
        "primary_evidence_segment_ids": 0,
        "function_label": 0,
        "rationale_mechanism": 0,
        "uncertainty_flag": 0,
    }
    for record in records:
        if not record.rationale_note:
            counts["rationale_note"] += 1
        if not record.primary_evidence_segment_ids:
            counts["primary_evidence_segment_ids"] += 1
        if not record.function_label:
            counts["function_label"] += 1
        if not record.rationale_mechanism:
            counts["rationale_mechanism"] += 1
        if not record.uncertainty_flag:
            counts["uncertainty_flag"] += 1
    return counts


def _pandas():
    try:
        import pandas as pd
    except ImportError:
        raise RuntimeError(
            "trim_haa.reporting requires the optional pandas dependency. "
            "Install trim-haa[reporting] to use reporting helpers."
        ) from None
    return pd
