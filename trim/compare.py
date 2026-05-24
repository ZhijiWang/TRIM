"""Comparison utilities for human-created TRIM annotations."""

from __future__ import annotations

from typing import Any, Mapping

import pandas as pd

from trim.schema import TrimAnnotation
from trim.signature import SIGNATURE_FIELDS


TABLE_SEPARATOR = "; "


def signature_string(row: pd.Series | Mapping[str, Any] | TrimAnnotation) -> str:
    """Return the six-part TRIM friction signature for a row."""

    return " / ".join(_row_value(row, field_name) for field_name in SIGNATURE_FIELDS)


def group_by_function(df: pd.DataFrame) -> pd.DataFrame:
    """Return cases grouped by ``function_label``."""

    rows: list[dict[str, Any]] = []
    prepared = _with_signature(df)
    for function_label, group in prepared.groupby("function_label", sort=False):
        if not _clean_value(function_label):
            continue
        signatures = _unique_nonempty(group["_signature"])
        rows.append(
            {
                "function_label": _clean_value(function_label),
                "case_count": len(group),
                "case_ids": _join_unique(group["case_id"]),
                "case_labels": _join_unique(group["case_label"]),
                "signature_count": len(signatures),
                "signatures": _join_values(signatures),
            }
        )
    return pd.DataFrame(
        rows,
        columns=[
            "function_label",
            "case_count",
            "case_ids",
            "case_labels",
            "signature_count",
            "signatures",
        ],
    )


def find_same_function_different_signature(df: pd.DataFrame) -> pd.DataFrame:
    """Find cases with the same function label but different signatures."""

    rows: list[dict[str, Any]] = []
    prepared = _with_signature(df)
    for function_label, group in prepared.groupby("function_label", sort=False):
        function_label = _clean_value(function_label)
        if not function_label:
            continue
        signatures = _unique_nonempty(group["_signature"])
        if len(signatures) <= 1:
            continue
        rows.append(
            {
                "function_label": function_label,
                "case_ids": _join_unique(group["case_id"]),
                "case_labels": _join_unique(group["case_label"]),
                "signature_count": len(signatures),
                "signatures": _join_values(signatures),
                "interpretive_payoff": (
                    "Same function label appears with different threshold-rationale "
                    "signatures."
                ),
            }
        )
    return pd.DataFrame(
        rows,
        columns=[
            "function_label",
            "case_ids",
            "case_labels",
            "signature_count",
            "signatures",
            "interpretive_payoff",
        ],
    )


def find_same_cue_different_function(
    df: pd.DataFrame,
    cue_family_filter: str | list[str] | None = None,
) -> pd.DataFrame:
    """Find cases with the same cue family but different function labels."""

    rows: list[dict[str, Any]] = []
    prepared = _with_signature(df)
    cue_families = _normalize_cue_family_filter(cue_family_filter)
    if cue_families is not None:
        prepared = prepared[prepared["cue_family"].isin(cue_families)]

    for cue_family, group in prepared.groupby("cue_family", sort=False):
        cue_family = _clean_value(cue_family)
        if not cue_family:
            continue
        functions = _unique_nonempty(group["function_label"])
        if len(functions) <= 1:
            continue
        rows.append(
            {
                "cue_family": cue_family,
                "case_ids": _join_unique(group["case_id"]),
                "case_labels": _join_unique(group["case_label"]),
                "function_count": len(functions),
                "functions": _join_values(functions),
                "signatures": _join_unique(group["_signature"]),
            }
        )
    return pd.DataFrame(
        rows,
        columns=[
            "cue_family",
            "case_ids",
            "case_labels",
            "function_count",
            "functions",
            "signatures",
        ],
    )


def find_same_broad_family_different_signature(df: pd.DataFrame) -> pd.DataFrame:
    """Find non-empty broad-family groups with different signatures."""

    rows: list[dict[str, Any]] = []
    prepared = _with_signature(df)
    prepared = prepared[prepared["broad_function_family"].map(bool)]
    for broad_family, group in prepared.groupby("broad_function_family", sort=False):
        broad_family = _clean_value(broad_family)
        if not broad_family:
            continue
        signatures = _unique_nonempty(group["_signature"])
        if len(signatures) <= 1:
            continue
        rows.append(
            {
                "broad_function_family": broad_family,
                "case_ids": _join_unique(group["case_id"]),
                "case_labels": _join_unique(group["case_label"]),
                "signature_count": len(signatures),
                "signatures": _join_values(signatures),
                "interpretive_payoff": (
                    "Same broad function family appears with different "
                    "threshold-rationale signatures."
                ),
            }
        )
    return pd.DataFrame(
        rows,
        columns=[
            "broad_function_family",
            "case_ids",
            "case_labels",
            "signature_count",
            "signatures",
            "interpretive_payoff",
        ],
    )


def find_contested_cases(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows where ``alternative_signature`` is not empty."""

    prepared = _with_signature(df)
    mask = prepared["alternative_signature"].map(bool)
    columns = [
        "case_id",
        "case_label",
        "function_label",
        "cue_family",
        "signature",
        "alternative_signature",
        "rationale_note",
    ]
    contested = prepared.loc[mask].copy()
    contested["signature"] = contested["_signature"]
    return contested.reindex(columns=columns).reset_index(drop=True)


def compare_case_pair(
    df: pd.DataFrame,
    case_id_1: str,
    case_id_2: str,
) -> dict[str, Any]:
    """Compare two cases by function, cue, signature fields, and summary flags."""

    prepared = _with_signature(df)
    left = _get_case(prepared, case_id_1)
    right = _get_case(prepared, case_id_2)

    comparison: dict[str, Any] = {}
    for field_name in (
        "function_label",
        "cue_family",
        "friction_locus",
        "rationale_mechanism",
        "epistemic_support",
        "discourse_level",
        "temporal_orientation",
        "uncertainty_flag",
    ):
        left_value = _row_value(left, field_name)
        right_value = _row_value(right, field_name)
        comparison[field_name] = {
            "case_id_1": left_value,
            "case_id_2": right_value,
            "match": left_value == right_value,
        }

    same_function = comparison["function_label"]["match"]
    same_cue = comparison["cue_family"]["match"]
    same_signature = _row_value(left, "_signature") == _row_value(right, "_signature")
    differing_fields = [
        field_name
        for field_name in SIGNATURE_FIELDS
        if _row_value(left, field_name) != _row_value(right, field_name)
    ]

    comparison["same_function"] = same_function
    comparison["same_cue"] = same_cue
    comparison["same_signature"] = same_signature
    comparison["difference_summary"] = _difference_summary(
        case_id_1=case_id_1,
        case_id_2=case_id_2,
        same_function=same_function,
        same_cue=same_cue,
        same_signature=same_signature,
        differing_fields=differing_fields,
    )
    return comparison


def same_function_table(df: pd.DataFrame) -> pd.DataFrame:
    return find_same_function_different_signature(df)


def same_cue_table(
    df: pd.DataFrame,
    cue_family_filter: str | list[str] | None = None,
) -> pd.DataFrame:
    return find_same_cue_different_function(df, cue_family_filter=cue_family_filter)


def broad_family_table(df: pd.DataFrame) -> pd.DataFrame:
    return find_same_broad_family_different_signature(df)


def contested_cases_table(df: pd.DataFrame) -> pd.DataFrame:
    return find_contested_cases(df)


def _with_signature(df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()
    for column in {
        "case_id",
        "case_label",
        "function_label",
        "cue_family",
        "broad_function_family",
        "alternative_signature",
        *SIGNATURE_FIELDS,
    }:
        if column not in prepared.columns:
            prepared[column] = ""
        prepared[column] = prepared[column].map(_clean_value)
    prepared["_signature"] = prepared.apply(signature_string, axis=1)
    return prepared


def _normalize_cue_family_filter(
    cue_family_filter: str | list[str] | None,
) -> set[str] | None:
    if cue_family_filter is None:
        return None
    if isinstance(cue_family_filter, str):
        values = [cue_family_filter]
    else:
        values = cue_family_filter
    return {
        cleaned
        for value in values
        if (cleaned := _clean_value(value))
    }


def _get_case(df: pd.DataFrame, case_id: str) -> pd.Series:
    matches = df.loc[df["case_id"] == case_id]
    if matches.empty:
        raise ValueError(f"Unknown case_id {case_id!r}.")
    if len(matches) > 1:
        raise ValueError(f"case_id {case_id!r} is not unique.")
    return matches.iloc[0]


def _difference_summary(
    case_id_1: str,
    case_id_2: str,
    same_function: bool,
    same_cue: bool,
    same_signature: bool,
    differing_fields: list[str],
) -> str:
    if same_signature:
        signature_text = "same friction signature"
    else:
        signature_text = "different friction signatures"
    function_text = "same function" if same_function else "different functions"
    cue_text = "same cue family" if same_cue else "different cue families"
    if differing_fields:
        field_text = f" Differing signature fields: {', '.join(differing_fields)}."
    else:
        field_text = ""
    return (
        f"{case_id_1} and {case_id_2} have {function_text}, {cue_text}, and "
        f"{signature_text}.{field_text}"
    )


def _join_unique(values: Any) -> str:
    return _join_values(_unique_nonempty(values))


def _join_values(values: list[str]) -> str:
    return TABLE_SEPARATOR.join(values)


def _unique_nonempty(values: Any) -> list[str]:
    seen: set[str] = set()
    unique_values: list[str] = []
    for value in values:
        cleaned = _clean_value(value)
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        unique_values.append(cleaned)
    return unique_values


def _row_value(row: pd.Series | Mapping[str, Any] | TrimAnnotation, field_name: str) -> str:
    if isinstance(row, TrimAnnotation):
        return _clean_value(getattr(row, field_name, ""))
    if isinstance(row, pd.Series):
        return _clean_value(row.get(field_name, ""))
    if isinstance(row, Mapping):
        return _clean_value(row.get(field_name, ""))
    return _clean_value(getattr(row, field_name, ""))


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()
