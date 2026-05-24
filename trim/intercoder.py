"""Intercoder comparison utilities for multi-coder TRIM annotations.

Human coders provide annotation values. These functions support reliability
analysis when multiple coders annotate the same cases.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any, Iterable

import pandas as pd


DEFAULT_DISAGREEMENT_FIELDS: tuple[str, ...] = (
    "function_label",
    "friction_locus",
    "rationale_mechanism",
    "temporal_orientation",
    "uncertainty_flag",
)

PAIRWISE_COLUMNS: tuple[str, ...] = (
    "field",
    "coder_id_1",
    "coder_id_2",
    "comparable_cases",
    "agreements",
    "percent_agreement",
)

DISAGREEMENT_COLUMNS: tuple[str, ...] = (
    "case_id",
    "field",
    "coder_values",
    "coders",
    "value_count",
)

HUMAN_REVIEW_COLUMNS: tuple[str, ...] = (
    "locatable?",
    "rationale-coherent?",
    "resists simple refinement?",
)


def pivot_coder_annotations(df: pd.DataFrame, field: str) -> pd.DataFrame:
    """Return a case_id by coder_id matrix for one annotation field."""

    _require_columns(df, ("case_id", "coder_id", field))
    prepared = _clean_frame(df, ("case_id", "coder_id", field))
    prepared = prepared[
        (prepared["case_id"] != "")
        & (prepared["coder_id"] != "")
        & (prepared[field] != "")
    ]

    if prepared.empty:
        return pd.DataFrame()

    grouped = (
        prepared.groupby(["case_id", "coder_id"], sort=True)[field]
        .agg(_first_nonempty)
        .reset_index()
    )
    pivot = grouped.pivot(index="case_id", columns="coder_id", values=field)
    return pivot.fillna("")


def percent_agreement(df: pd.DataFrame, field: str) -> float:
    """Compute simple percent agreement for one field.

    Cases count only when at least two coders provided non-empty values.
    Returns ``NaN`` when there are no comparable cases.
    """

    pivot = pivot_coder_annotations(df, field)
    comparable = _comparable_rows(pivot)
    if comparable.empty:
        return float("nan")

    agreements = sum(_row_agrees(row) for _, row in comparable.iterrows())
    return agreements / len(comparable)


def pairwise_agreement(df: pd.DataFrame, field: str) -> pd.DataFrame:
    """Return pairwise coder agreement for one field."""

    pivot = pivot_coder_annotations(df, field)
    if len(pivot.columns) < 2:
        return pd.DataFrame(columns=PAIRWISE_COLUMNS)

    rows: list[dict[str, Any]] = []
    for coder_id_1, coder_id_2 in combinations(pivot.columns, 2):
        pair = pivot[[coder_id_1, coder_id_2]]
        pair = pair[(pair[coder_id_1] != "") & (pair[coder_id_2] != "")]
        comparable_cases = len(pair)
        agreements = int((pair[coder_id_1] == pair[coder_id_2]).sum())
        agreement = agreements / comparable_cases if comparable_cases else float("nan")
        rows.append(
            {
                "field": field,
                "coder_id_1": coder_id_1,
                "coder_id_2": coder_id_2,
                "comparable_cases": comparable_cases,
                "agreements": agreements,
                "percent_agreement": agreement,
            }
        )

    return pd.DataFrame(rows, columns=PAIRWISE_COLUMNS)


def cohen_kappa_if_two_coders(df: pd.DataFrame, field: str) -> dict[str, Any]:
    """Compute Cohen's kappa for exactly two coders when sklearn is available."""

    pivot = pivot_coder_annotations(df, field)
    coder_ids = list(pivot.columns)
    if len(coder_ids) != 2:
        return {
            "field": field,
            "coder_ids": coder_ids,
            "comparable_cases": 0,
            "kappa": None,
            "warning": "Cohen's kappa requires exactly two coders.",
        }

    pair = pivot[coder_ids]
    pair = pair[(pair[coder_ids[0]] != "") & (pair[coder_ids[1]] != "")]
    if pair.empty:
        return {
            "field": field,
            "coder_ids": coder_ids,
            "comparable_cases": 0,
            "kappa": None,
            "warning": "Cohen's kappa requires at least one comparable case.",
        }

    try:
        from sklearn.metrics import cohen_kappa_score
    except ImportError:
        return {
            "field": field,
            "coder_ids": coder_ids,
            "comparable_cases": len(pair),
            "kappa": None,
            "warning": "scikit-learn is not installed; Cohen's kappa not computed.",
        }

    return {
        "field": field,
        "coder_ids": coder_ids,
        "comparable_cases": len(pair),
        "kappa": float(cohen_kappa_score(pair[coder_ids[0]], pair[coder_ids[1]])),
        "warning": None,
    }


def disagreement_table(
    df: pd.DataFrame,
    fields: Iterable[str] = DEFAULT_DISAGREEMENT_FIELDS,
) -> pd.DataFrame:
    """Return cases where coders disagree on selected fields."""

    rows: list[dict[str, Any]] = []
    for field in fields:
        pivot = pivot_coder_annotations(df, field)
        for case_id, row in _comparable_rows(pivot).iterrows():
            values_by_coder = {
                coder_id: _clean_value(value)
                for coder_id, value in row.items()
                if _clean_value(value)
            }
            unique_values = sorted(set(values_by_coder.values()))
            if len(unique_values) <= 1:
                continue
            rows.append(
                {
                    "case_id": case_id,
                    "field": field,
                    "coder_values": _format_coder_values(values_by_coder),
                    "coders": "; ".join(values_by_coder.keys()),
                    "value_count": len(unique_values),
                }
            )

    return pd.DataFrame(rows, columns=DISAGREEMENT_COLUMNS)


def contested_disagreement_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return disagreements with blank columns for human demarcation review."""

    report = disagreement_table(df, DEFAULT_DISAGREEMENT_FIELDS)
    for column in HUMAN_REVIEW_COLUMNS:
        report[column] = ""
    return report.reindex(columns=[*DISAGREEMENT_COLUMNS, *HUMAN_REVIEW_COLUMNS])


def _require_columns(df: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}.")


def _clean_frame(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    prepared = df.copy()
    for column in columns:
        prepared[column] = prepared[column].map(_clean_value)
    return prepared


def _comparable_rows(pivot: pd.DataFrame) -> pd.DataFrame:
    if pivot.empty:
        return pivot
    comparable_mask = pivot.apply(
        lambda row: sum(_clean_value(value) != "" for value in row) >= 2,
        axis=1,
    )
    return pivot.loc[comparable_mask]


def _row_agrees(row: pd.Series) -> bool:
    values = [_clean_value(value) for value in row if _clean_value(value)]
    return len(set(values)) == 1


def _first_nonempty(values: pd.Series) -> str:
    for value in values:
        cleaned = _clean_value(value)
        if cleaned:
            return cleaned
    return ""


def _format_coder_values(values_by_coder: dict[str, str]) -> str:
    return "; ".join(
        f"{coder_id}={value}"
        for coder_id, value in values_by_coder.items()
    )


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()
