"""Report helpers for TRIM validation and comparison outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from trim.compare import (
    broad_family_table,
    contested_cases_table,
    same_cue_table,
    same_function_table,
)
from trim.validator import validate_dataframe, validation_report


def write_markdown_table(df: pd.DataFrame, path: str | Path) -> None:
    """Write a DataFrame as a markdown table."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_dataframe_to_markdown(df), encoding="utf-8")


def generate_demo_report(df: pd.DataFrame, output_path: str | Path) -> dict[str, pd.DataFrame]:
    """Generate the demo comparison report and return its source tables."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    issues = validate_dataframe(df)
    error_count = sum(issue.severity == "error" for issue in issues)
    warning_count = sum(issue.severity == "warning" for issue in issues)

    tables = {
        "same_function_table": same_function_table(df),
        "same_cue_table": same_cue_table(df),
        "primary_same_cue_table": same_cue_table(df, cue_family_filter="prophecy"),
        "additional_same_cue_table": _additional_same_cue_groups(df),
        "broad_family_table": broad_family_table(df),
        "contested_cases_table": contested_cases_table(df),
    }

    lines = [
        "# TRIM Demo Comparison Report",
        "",
        "## Validation Summary",
        "",
        f"- Records: {len(df)}",
        f"- Errors: {error_count}",
        f"- Warnings: {warning_count}",
        "",
    ]

    issue_table = validation_report(df)
    if issue_table.empty:
        lines.append("Validation passed with no issues.")
    else:
        lines.append(_dataframe_to_markdown(issue_table))

    lines.extend(
        [
            "",
            "## Same Function / Different Signature",
            "",
            _dataframe_to_markdown(tables["same_function_table"]),
            "",
            "## Same Cue / Different Function",
            "",
            "### Primary same-cue test: prophecy",
            "",
            _dataframe_to_markdown(tables["primary_same_cue_table"]),
            "",
            "### Additional detected same-cue groups",
            "",
            _dataframe_to_markdown(tables["additional_same_cue_table"]),
            "",
            "### Full same-cue output table",
            "",
            _dataframe_to_markdown(tables["same_cue_table"]),
            "",
            "## Broad Family / Different Signature",
            "",
            _dataframe_to_markdown(tables["broad_family_table"]),
            "",
            "## Contested Cases",
            "",
            _dataframe_to_markdown(tables["contested_cases_table"]),
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return tables


def _additional_same_cue_groups(df: pd.DataFrame) -> pd.DataFrame:
    table = same_cue_table(df)
    if table.empty:
        return table
    return table.loc[table["cue_family"] != "prophecy"].reset_index(drop=True)


def _dataframe_to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"

    columns = [str(column) for column in df.columns]
    rows = []
    for _, row in df.iterrows():
        rows.append([_markdown_cell(row[column]) for column in df.columns])

    header = "| " + " | ".join(_markdown_cell(column) for column in columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def _markdown_cell(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).replace("\n", "<br>").replace("|", "\\|")
