"""Descriptive TRIM-HAA reports."""

from __future__ import annotations

from statistics import mean, median
from typing import Any, Iterable, Mapping

import pandas as pd

from trim_haa.comparison import compare_pre_ai_post
from trim_haa.schema import TrimHAAAnnotation
from trim_haa.validator import validate_dataset


def case_level_report(
    annotations: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    by_case = _by_case(annotations)
    for case_id, records in by_case.items():
        human_pre = _first_stage(records, "human_pre")
        ai = _first_stage(records, "ai_independent")
        post = _first_stage(records, "human_post_ai")
        control = _first_stage(records, "human_second_pass_control")
        row = {
            "case_id": case_id,
            "human_pre_annotation_id": _id(human_pre),
            "ai_annotation_id": _id(ai),
            "human_post_annotation_id": _id(post),
            "control_annotation_id": _id(control),
        }
        if human_pre and ai and post:
            comparison = compare_pre_ai_post(human_pre, ai, post)
            row.update(
                {
                    "pre_label": comparison["pre_label"],
                    "ai_label": comparison["ai_label"],
                    "post_label": comparison["post_label"],
                    "label_adoption": comparison["label_adopted_from_ai"],
                    "pre_ai_primary_jaccard": comparison["pre_ai_primary_jaccard"],
                    "pre_post_primary_jaccard": comparison["pre_post_primary_jaccard"],
                    "post_ai_primary_jaccard": comparison["post_ai_primary_jaccard"],
                    "evidence_adoption": comparison["evidence_adoption"],
                    "evidential_displacement": comparison["evidential_displacement"],
                    "mechanism_adoption": comparison["mechanism_adopted_from_ai"],
                    "uncertainty_shift": comparison["uncertainty_shift"],
                    "alternative_suppression": comparison["alternative_suppressed"],
                    "alternative_generation": comparison["alternative_generated"],
                    "rationale_overlap": comparison["rationale_overlap"],
                }
            )
        rows.append(row)
    return pd.DataFrame(rows, columns=CASE_LEVEL_COLUMNS)


def participant_level_report(
    annotations: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
    case_report: pd.DataFrame | None = None,
) -> pd.DataFrame:
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
                "label_changes": _sum_bool(subset, "label_adoption"),
                "label_adoptions": _sum_bool(subset, "label_adoption"),
                "evidence_adoptions": _sum_bool(subset, "evidence_adoption"),
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
) -> dict[str, Any]:
    prepared = [_coerce(record) for record in annotations]
    cases = case_level_report(prepared)
    report = validate_dataset(prepared, provenance_records)
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
        "evidence_adoption_count": _sum_bool(cases, "evidence_adoption"),
        "evidence_adoption_percent": _percent(cases, "evidence_adoption"),
        "evidential_displacement_count": _sum_bool(cases, "evidential_displacement"),
        "mechanism_adoption_count": _sum_bool(cases, "mechanism_adoption"),
        "alternative_suppression_count": _sum_bool(cases, "alternative_suppression"),
        "alternative_generation_count": _sum_bool(cases, "alternative_generation"),
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
    "pre_label",
    "ai_label",
    "post_label",
    "label_adoption",
    "pre_ai_primary_jaccard",
    "pre_post_primary_jaccard",
    "post_ai_primary_jaccard",
    "evidence_adoption",
    "evidential_displacement",
    "mechanism_adoption",
    "uncertainty_shift",
    "alternative_suppression",
    "alternative_generation",
    "rationale_overlap",
)


def _by_case(records: Iterable[TrimHAAAnnotation | Mapping[str, Any]]) -> dict[str, list[TrimHAAAnnotation]]:
    by_case: dict[str, list[TrimHAAAnnotation]] = {}
    for record in records:
        annotation = _coerce(record)
        by_case.setdefault(annotation.case_id, []).append(annotation)
    return by_case


def _first_stage(records: list[TrimHAAAnnotation], stage: str) -> TrimHAAAnnotation | None:
    for record in records:
        if record.annotation_stage == stage:
            return record
    return None


def _coerce(record: TrimHAAAnnotation | Mapping[str, Any]) -> TrimHAAAnnotation:
    if isinstance(record, TrimHAAAnnotation):
        return record
    return TrimHAAAnnotation.from_record(record)


def _id(record: TrimHAAAnnotation | None) -> str:
    return record.annotation_id if record else ""


def _sum_bool(df: pd.DataFrame, column: str) -> int:
    if column not in df:
        return 0
    return sum(1 for value in df[column] if bool(value))


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
