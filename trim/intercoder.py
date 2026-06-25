"""Intercoder comparison utilities for multi-coder TRIM annotations.

Human coders provide annotation values. These functions support agreement and
disagreement analysis when multiple coders annotate the same cases.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any, Iterable, Mapping

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

COMPOUND_PAIRWISE_COLUMNS: tuple[str, ...] = (
    "field",
    "coder_id_1",
    "coder_id_2",
    "comparable_cases",
    "exact_set_agreements",
    "exact_set_agreement",
    "primary_agreements",
    "primary_agreement",
    "compatible_single_compound_agreements",
    "compatible_single_compound_agreement",
    "any_overlap_agreements",
    "any_overlap_agreement",
    "mean_jaccard_overlap",
)

SEGMENT_PAIRWISE_COLUMNS: tuple[str, ...] = (
    "field",
    "coder_id_1",
    "coder_id_2",
    "comparable_cases",
    "exact_set_agreements",
    "exact_set_agreement",
    "any_overlap_agreements",
    "any_overlap_agreement",
    "mean_jaccard_overlap",
)

PRIMARY_CONTEXT_COLUMNS: tuple[str, ...] = (
    "case_id",
    "coder_id_1",
    "coder_id_2",
    "primary_exact_set_agreement",
    "primary_jaccard_overlap",
    "context_exact_set_agreement",
    "context_jaccard_overlap",
    "cross_role_overlap",
)

DISAGREEMENT_COLUMNS: tuple[str, ...] = (
    "case_id",
    "field",
    "coder_values",
    "coders",
    "value_count",
    "raw_disagreement",
    "compatible_difference",
    "adjudicated_codebook_ambiguity",
    "adjudicated_substantive_pathway_variation",
    "insufficient_evidence",
    "disagreement_category",
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
    """Return pairwise raw-string agreement for one field."""

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


def compound_value_metrics(left: str, right: str) -> dict[str, bool | float]:
    """Compare two ordered ``+``-joined values without collapsing their roles."""

    left_parts = _compound_parts(left)
    right_parts = _compound_parts(right)
    if not left_parts or not right_parts:
        raise ValueError("Compound agreement requires two non-empty values.")

    left_set = set(left_parts)
    right_set = set(right_parts)
    intersection = left_set & right_set
    union = left_set | right_set
    return {
        "exact_set_agreement": left_set == right_set,
        "primary_agreement": left_parts[0] == right_parts[0],
        "any_overlap_agreement": bool(intersection),
        "jaccard_overlap": len(intersection) / len(union),
    }


def compatible_single_compound_value(left: str, right: str) -> bool:
    """Return whether a single value is contained in the other compound value."""

    left_parts = _compound_parts(left)
    right_parts = _compound_parts(right)
    if not left_parts or not right_parts:
        raise ValueError("Compound compatibility requires two non-empty values.")
    if len(left_parts) == len(right_parts):
        return set(left_parts) == set(right_parts)
    if len(left_parts) == 1:
        return left_parts[0] in set(right_parts)
    if len(right_parts) == 1:
        return right_parts[0] in set(left_parts)
    return bool(set(left_parts) & set(right_parts))


def pairwise_compound_agreement(df: pd.DataFrame, field: str) -> pd.DataFrame:
    """Return compound-aware pairwise agreement for a ``+``-joined field."""

    pivot = pivot_coder_annotations(df, field)
    if len(pivot.columns) < 2:
        return pd.DataFrame(columns=COMPOUND_PAIRWISE_COLUMNS)

    rows: list[dict[str, Any]] = []
    for coder_id_1, coder_id_2 in combinations(pivot.columns, 2):
        pair = pivot[[coder_id_1, coder_id_2]]
        pair = pair[(pair[coder_id_1] != "") & (pair[coder_id_2] != "")]
        metrics = [
            compound_value_metrics(row[coder_id_1], row[coder_id_2])
            for _, row in pair.iterrows()
        ]
        comparable_cases = len(metrics)
        exact_set_agreements = sum(
            bool(metric["exact_set_agreement"]) for metric in metrics
        )
        primary_agreements = sum(
            bool(metric["primary_agreement"]) for metric in metrics
        )
        compatible_single_compound_agreements = sum(
            compatible_single_compound_value(row[coder_id_1], row[coder_id_2])
            for _, row in pair.iterrows()
        )
        any_overlap_agreements = sum(
            bool(metric["any_overlap_agreement"]) for metric in metrics
        )
        rows.append(
            {
                "field": field,
                "coder_id_1": coder_id_1,
                "coder_id_2": coder_id_2,
                "comparable_cases": comparable_cases,
                "exact_set_agreements": exact_set_agreements,
                "exact_set_agreement": (
                    exact_set_agreements / comparable_cases
                    if comparable_cases
                    else float("nan")
                ),
                "primary_agreements": primary_agreements,
                "primary_agreement": (
                    primary_agreements / comparable_cases
                    if comparable_cases
                    else float("nan")
                ),
                "compatible_single_compound_agreements": (
                    compatible_single_compound_agreements
                ),
                "compatible_single_compound_agreement": (
                    compatible_single_compound_agreements / comparable_cases
                    if comparable_cases
                    else float("nan")
                ),
                "any_overlap_agreements": any_overlap_agreements,
                "any_overlap_agreement": (
                    any_overlap_agreements / comparable_cases
                    if comparable_cases
                    else float("nan")
                ),
                "mean_jaccard_overlap": (
                    sum(float(metric["jaccard_overlap"]) for metric in metrics)
                    / comparable_cases
                    if comparable_cases
                    else float("nan")
                ),
            }
        )

    return pd.DataFrame(rows, columns=COMPOUND_PAIRWISE_COLUMNS)


def segment_set_metrics(left: Any, right: Any) -> dict[str, bool | float]:
    """Compare two segment-ID sets without treating order as meaningful."""

    left_set = set(_split_segment_ids(left))
    right_set = set(_split_segment_ids(right))
    if not left_set or not right_set:
        raise ValueError("Segment comparison requires two non-empty values.")
    intersection = left_set & right_set
    union = left_set | right_set
    return {
        "exact_set_agreement": left_set == right_set,
        "any_overlap_agreement": bool(intersection),
        "jaccard_overlap": len(intersection) / len(union),
    }


def pairwise_segment_agreement(
    df: pd.DataFrame,
    field: str = "primary_evidence_segment_ids",
) -> pd.DataFrame:
    """Return pairwise segment-set agreement and overlap for one segment field."""

    pivot = pivot_coder_annotations(df, field)
    if len(pivot.columns) < 2:
        return pd.DataFrame(columns=SEGMENT_PAIRWISE_COLUMNS)

    rows: list[dict[str, Any]] = []
    for coder_id_1, coder_id_2 in combinations(pivot.columns, 2):
        pair = pivot[[coder_id_1, coder_id_2]]
        pair = pair[(pair[coder_id_1] != "") & (pair[coder_id_2] != "")]
        metrics = [
            segment_set_metrics(row[coder_id_1], row[coder_id_2])
            for _, row in pair.iterrows()
        ]
        comparable_cases = len(metrics)
        exact_set_agreements = sum(
            bool(metric["exact_set_agreement"]) for metric in metrics
        )
        any_overlap_agreements = sum(
            bool(metric["any_overlap_agreement"]) for metric in metrics
        )
        rows.append(
            {
                "field": field,
                "coder_id_1": coder_id_1,
                "coder_id_2": coder_id_2,
                "comparable_cases": comparable_cases,
                "exact_set_agreements": exact_set_agreements,
                "exact_set_agreement": (
                    exact_set_agreements / comparable_cases
                    if comparable_cases
                    else float("nan")
                ),
                "any_overlap_agreements": any_overlap_agreements,
                "any_overlap_agreement": (
                    any_overlap_agreements / comparable_cases
                    if comparable_cases
                    else float("nan")
                ),
                "mean_jaccard_overlap": (
                    sum(float(metric["jaccard_overlap"]) for metric in metrics)
                    / comparable_cases
                    if comparable_cases
                    else float("nan")
                ),
            }
        )
    return pd.DataFrame(rows, columns=SEGMENT_PAIRWISE_COLUMNS)


def primary_context_segment_overlap(df: pd.DataFrame) -> pd.DataFrame:
    """Compare primary and context evidence selections for each coder pair."""

    _require_columns(
        df,
        (
            "case_id",
            "coder_id",
            "primary_evidence_segment_ids",
            "context_segment_ids",
        ),
    )
    prepared = _clean_frame(
        df,
        (
            "case_id",
            "coder_id",
            "primary_evidence_segment_ids",
            "context_segment_ids",
        ),
    )
    rows: list[dict[str, Any]] = []
    for case_id, group in prepared.groupby("case_id", sort=True):
        coder_rows = {
            row["coder_id"]: row
            for _, row in group.iterrows()
            if row["coder_id"]
        }
        for coder_id_1, coder_id_2 in combinations(sorted(coder_rows), 2):
            left = coder_rows[coder_id_1]
            right = coder_rows[coder_id_2]
            primary = _safe_segment_metrics(
                left["primary_evidence_segment_ids"],
                right["primary_evidence_segment_ids"],
            )
            context = _safe_segment_metrics(
                left["context_segment_ids"],
                right["context_segment_ids"],
            )
            left_primary = set(_split_segment_ids(left["primary_evidence_segment_ids"]))
            right_primary = set(_split_segment_ids(right["primary_evidence_segment_ids"]))
            left_context = set(_split_segment_ids(left["context_segment_ids"]))
            right_context = set(_split_segment_ids(right["context_segment_ids"]))
            cross_role = (left_primary & right_context) | (right_primary & left_context)
            rows.append(
                {
                    "case_id": case_id,
                    "coder_id_1": coder_id_1,
                    "coder_id_2": coder_id_2,
                    "primary_exact_set_agreement": primary["exact_set_agreement"],
                    "primary_jaccard_overlap": primary["jaccard_overlap"],
                    "context_exact_set_agreement": context["exact_set_agreement"],
                    "context_jaccard_overlap": context["jaccard_overlap"],
                    "cross_role_overlap": "|".join(sorted(cross_role)),
                }
            )
    return pd.DataFrame(rows, columns=PRIMARY_CONTEXT_COLUMNS)


def stratified_pairwise_agreement(
    df: pd.DataFrame,
    field: str,
    strata_fields: Iterable[str] = ("language_access_mode", "case_scope"),
) -> pd.DataFrame:
    """Return pairwise agreement within language-access or scope strata."""

    rows: list[pd.DataFrame] = []
    for stratum_field in strata_fields:
        if stratum_field not in df.columns:
            continue
        for stratum_value, group in df.groupby(stratum_field, sort=True):
            clean_stratum = _clean_value(stratum_value)
            if not clean_stratum:
                continue
            table = pairwise_agreement(group, field)
            if table.empty:
                continue
            table.insert(0, "stratum_field", stratum_field)
            table.insert(1, "stratum_value", clean_stratum)
            rows.append(table)
    if not rows:
        return pd.DataFrame(
            columns=["stratum_field", "stratum_value", *PAIRWISE_COLUMNS]
        )
    return pd.concat(rows, ignore_index=True)


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
                    "raw_disagreement": "yes",
                    "compatible_difference": "",
                    "adjudicated_codebook_ambiguity": "",
                    "adjudicated_substantive_pathway_variation": "",
                    "insufficient_evidence": "",
                    "disagreement_category": "",
                }
            )

    return pd.DataFrame(rows, columns=DISAGREEMENT_COLUMNS)


def contested_disagreement_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return disagreements with blank columns for human demarcation review."""

    report = disagreement_table(df, DEFAULT_DISAGREEMENT_FIELDS)
    for column in HUMAN_REVIEW_COLUMNS:
        report[column] = ""
    return report.reindex(columns=[*DISAGREEMENT_COLUMNS, *HUMAN_REVIEW_COLUMNS])


def apply_disagreement_categories(
    disagreement_df: pd.DataFrame,
    categories: Mapping[str, str] | pd.DataFrame,
) -> pd.DataFrame:
    """Add adjudication categories without altering raw disagreement rows."""

    prepared = disagreement_df.copy()
    if isinstance(categories, pd.DataFrame):
        category_map = {
            _clean_value(row["case_id"]): _clean_value(row["disagreement_category"])
            for _, row in categories.iterrows()
            if "case_id" in row and "disagreement_category" in row
        }
    else:
        category_map = {
            _clean_value(case_id): _clean_value(category)
            for case_id, category in categories.items()
        }
    for column in DISAGREEMENT_COLUMNS:
        if column not in prepared.columns:
            prepared[column] = ""
    for index, row in prepared.iterrows():
        category = category_map.get(_clean_value(row["case_id"]), "")
        if not category:
            continue
        prepared.at[index, "disagreement_category"] = category
        if category == "compatible_difference":
            prepared.at[index, "compatible_difference"] = "yes"
        elif category == "codebook_ambiguity":
            prepared.at[index, "adjudicated_codebook_ambiguity"] = "yes"
        elif category == "substantive_pathway_variation":
            prepared.at[index, "adjudicated_substantive_pathway_variation"] = "yes"
        elif category == "insufficient_evidence":
            prepared.at[index, "insufficient_evidence"] = "yes"
    return prepared.reindex(columns=DISAGREEMENT_COLUMNS)


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


def _compound_parts(value: Any) -> tuple[str, ...]:
    return tuple(
        cleaned
        for part in _clean_value(value).split("+")
        if (cleaned := _clean_value(part))
    )


def _split_segment_ids(value: Any) -> tuple[str, ...]:
    text = _clean_value(value)
    if not text:
        return ()
    separator = "|" if "|" in text else ";"
    return tuple(part.strip() for part in text.split(separator) if part.strip())


def _safe_segment_metrics(left: Any, right: Any) -> dict[str, bool | float]:
    left_set = set(_split_segment_ids(left))
    right_set = set(_split_segment_ids(right))
    if not left_set and not right_set:
        return {
            "exact_set_agreement": True,
            "any_overlap_agreement": False,
            "jaccard_overlap": 1.0,
        }
    if not left_set or not right_set:
        return {
            "exact_set_agreement": False,
            "any_overlap_agreement": False,
            "jaccard_overlap": 0.0,
        }
    return segment_set_metrics(left, right)


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()
