"""Utilities for exploratory AI execution stress-test analysis.

These helpers intentionally report descriptive pipeline outputs only. AI-to-AI
comparison is not human intercoder reliability evidence.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from statistics import mean, median
from typing import Any, Mapping

import pandas as pd

from trim.intercoder import (
    compatible_single_compound_value,
    compound_value_metrics,
    segment_set_metrics,
)
from trim.schema import coerce_string_list


COMMON_COMPARISON_FIELDS: tuple[str, ...] = (
    "function_label",
    "friction_locus",
    "rationale_mechanism",
    "epistemic_support",
    "discourse_level",
    "temporal_orientation",
    "uncertainty_flag",
)

PATHWAY_CATEGORIES: frozenset[str] = frozenset(
    {
        "same_function_same_pathway",
        "same_function_different_pathway",
        "different_function_partially_shared_pathway",
        "different_function_different_pathway",
        "no_fit_disagreement",
        "insufficient_comparable_data",
    }
)


@dataclass(frozen=True, slots=True)
class SubmissionAvailability:
    """Presence metadata for an expected locked submission bundle."""

    coding_file: bool
    question_log_file: bool
    language_access_file: bool
    return_manifest_file: bool
    protocol_deviation_file: bool

    @property
    def complete(self) -> bool:
        return all(
            (
                self.coding_file,
                self.question_log_file,
                self.language_access_file,
                self.return_manifest_file,
                self.protocol_deviation_file,
            )
        )


def jaccard(left: str, right: str) -> float:
    """Return Jaccard overlap for pipe/semicolon/list-like segment values."""

    left_set = set(coerce_string_list(left))
    right_set = set(coerce_string_list(right))
    if not left_set and not right_set:
        return 1.0
    if not left_set or not right_set:
        return 0.0
    return len(left_set & right_set) / len(left_set | right_set)


def primary_context_role_reversal(
    left_primary: str,
    left_context: str,
    right_primary: str,
    right_context: str,
) -> str:
    """Return segments selected as primary by one side and context by the other."""

    left_primary_set = set(coerce_string_list(left_primary))
    left_context_set = set(coerce_string_list(left_context))
    right_primary_set = set(coerce_string_list(right_primary))
    right_context_set = set(coerce_string_list(right_context))
    reversed_segments = sorted(
        (left_primary_set & right_context_set) | (right_primary_set & left_context_set)
    )
    return "|".join(reversed_segments)


def alternative_signature_present(record: Mapping[str, Any]) -> bool:
    return bool(str(record.get("alternative_signature", "")).strip())


def classify_pathway(left: Mapping[str, Any], right: Mapping[str, Any]) -> str:
    """Conservatively classify the high-level relation between two pathways."""

    left_function = _clean(left.get("function_label"))
    right_function = _clean(right.get("function_label"))
    if not left_function or not right_function:
        return "insufficient_comparable_data"
    if left_function == "no_fit" or right_function == "no_fit":
        return (
            "same_function_same_pathway"
            if left_function == right_function and _same_pathway(left, right)
            else "no_fit_disagreement"
        )
    if left_function == right_function:
        return (
            "same_function_same_pathway"
            if _same_pathway(left, right)
            else "same_function_different_pathway"
        )
    return (
        "different_function_partially_shared_pathway"
        if _shared_pathway_fields(left, right) >= 3
        else "different_function_different_pathway"
    )


def case_comparison(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    *,
    left_label: str = "Codex",
    right_label: str = "Claude",
) -> pd.DataFrame:
    """Return case-level comparison across common TRIM fields."""

    left_records = _records_by_case(left_df)
    right_records = _records_by_case(right_df)
    rows: list[dict[str, Any]] = []
    for case_id in sorted(set(left_records) | set(right_records)):
        left = left_records.get(case_id, {})
        right = right_records.get(case_id, {})
        row: dict[str, Any] = {"case_id": case_id}
        for field in COMMON_COMPARISON_FIELDS:
            row[f"{left_label}_{field}"] = _clean(left.get(field))
            row[f"{right_label}_{field}"] = _clean(right.get(field))
            row[f"{field}_match"] = (
                bool(row[f"{left_label}_{field}"])
                and row[f"{left_label}_{field}"] == row[f"{right_label}_{field}"]
            )
        row[f"{left_label}_primary_segments"] = _clean(
            left.get("primary_evidence_segment_ids")
        )
        row[f"{right_label}_primary_segments"] = _clean(
            right.get("primary_evidence_segment_ids")
        )
        row["exact_primary_segment_match"] = (
            set(coerce_string_list(row[f"{left_label}_primary_segments"]))
            == set(coerce_string_list(row[f"{right_label}_primary_segments"]))
        )
        row["primary_evidence_jaccard"] = jaccard(
            row[f"{left_label}_primary_segments"],
            row[f"{right_label}_primary_segments"],
        )
        row[f"{left_label}_context_segments"] = _clean(left.get("context_segment_ids"))
        row[f"{right_label}_context_segments"] = _clean(right.get("context_segment_ids"))
        row["context_jaccard"] = jaccard(
            row[f"{left_label}_context_segments"],
            row[f"{right_label}_context_segments"],
        )
        row["primary_context_role_reversal"] = primary_context_role_reversal(
            row[f"{left_label}_primary_segments"],
            row[f"{left_label}_context_segments"],
            row[f"{right_label}_primary_segments"],
            row[f"{right_label}_context_segments"],
        )
        row[f"{left_label}_alternative_signature_present"] = (
            alternative_signature_present(left)
        )
        row[f"{right_label}_alternative_signature_present"] = (
            alternative_signature_present(right)
        )
        row["pathway_classification"] = classify_pathway(left, right)
        rows.append(row)
    return pd.DataFrame(rows)


def field_agreement(case_comparison_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize exact and compatible agreement from a case comparison table."""

    rows: list[dict[str, Any]] = []
    comparable_cases = len(case_comparison_df)
    for field in COMMON_COMPARISON_FIELDS:
        match_column = f"{field}_match"
        agreements = int(case_comparison_df[match_column].sum())
        row = {
            "field": field,
            "comparable_cases": comparable_cases,
            "exact_agreements": agreements,
            "exact_agreement": agreements / comparable_cases
            if comparable_cases
            else float("nan"),
            "compatible_agreements": "",
            "compatible_agreement": "",
        }
        if field in {"rationale_mechanism", "epistemic_support"}:
            compatible = 0
            for _, comparison in case_comparison_df.iterrows():
                values = [
                    comparison.get(f"Codex_{field}", ""),
                    comparison.get(f"Claude_{field}", ""),
                ]
                if values[0] and values[1] and compatible_single_compound_value(
                    values[0], values[1]
                ):
                    compatible += 1
            row["compatible_agreements"] = compatible
            row["compatible_agreement"] = (
                compatible / comparable_cases
                if comparable_cases
                else float("nan")
            )
        rows.append(row)
    return pd.DataFrame(rows)


def evidence_overlap(case_comparison_df: pd.DataFrame) -> pd.DataFrame:
    return case_comparison_df[
        [
            "case_id",
            "exact_primary_segment_match",
            "primary_evidence_jaccard",
            "context_jaccard",
            "primary_context_role_reversal",
        ]
    ].copy()


def uncertainty_distribution(df: pd.DataFrame, label: str) -> pd.DataFrame:
    counts = Counter(_clean(value) for value in df.get("uncertainty_flag", []))
    rows = [
        {
            "model": label,
            "uncertainty_flag": key,
            "count": value,
            "proportion": value / len(df) if len(df) else float("nan"),
        }
        for key, value in sorted(counts.items())
        if key
    ]
    return pd.DataFrame(rows)


def alternative_signature_frequency(df: pd.DataFrame, label: str) -> dict[str, Any]:
    count = int(df.get("alternative_signature", pd.Series(dtype=str)).map(bool).sum())
    total = len(df)
    return {
        "model": label,
        "alternative_signature_count": count,
        "case_count": total,
        "alternative_signature_rate": count / total if total else float("nan"),
    }


def model_pattern_summary(df: pd.DataFrame, label: str) -> dict[str, Any]:
    primary_counts = [
        len(coerce_string_list(value))
        for value in df.get("primary_evidence_segment_ids", [])
    ]
    context_counts = [
        len(coerce_string_list(value)) for value in df.get("context_segment_ids", [])
    ]
    rationale_lengths = [len(_clean(value)) for value in df.get("rationale_note", [])]
    return {
        "model": label,
        "case_count": len(df),
        "medium_uncertainty_count": int((df["uncertainty_flag"] == "medium").sum()),
        "low_uncertainty_count": int((df["uncertainty_flag"] == "low").sum()),
        "alternative_signature_count": int(df["alternative_signature"].map(bool).sum()),
        "all_segment_primary_count": int(
            sum(count >= 4 for count in primary_counts)
        ),
        "mean_primary_segment_count": mean(primary_counts) if primary_counts else 0,
        "mean_context_segment_count": mean(context_counts) if context_counts else 0,
        "median_rationale_length": median(rationale_lengths)
        if rationale_lengths
        else 0,
        "no_fit_count": int((df["function_label"] == "no_fit").sum()),
        "discourse_level_distribution": dict(Counter(df["discourse_level"])),
    }


def _same_pathway(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    return all(_clean(left.get(field)) == _clean(right.get(field)) for field in COMMON_COMPARISON_FIELDS)


def _shared_pathway_fields(left: Mapping[str, Any], right: Mapping[str, Any]) -> int:
    shared = 0
    for field in COMMON_COMPARISON_FIELDS[1:]:
        left_value = _clean(left.get(field))
        right_value = _clean(right.get(field))
        if not left_value or not right_value:
            continue
        if left_value == right_value:
            shared += 1
        elif field in {"rationale_mechanism", "epistemic_support"}:
            try:
                metrics = compound_value_metrics(left_value, right_value)
            except ValueError:
                continue
            if metrics["any_overlap_agreement"]:
                shared += 1
    return shared


def _records_by_case(df: pd.DataFrame) -> dict[str, Mapping[str, Any]]:
    return {
        _clean(record.get("case_id")): record
        for record in df.to_dict(orient="records")
        if _clean(record.get("case_id"))
    }


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()
