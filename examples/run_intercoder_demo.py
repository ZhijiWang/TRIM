"""Prepare a small intercoder workflow report for TRIM."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from trim.intercoder import DEFAULT_DISAGREEMENT_FIELDS, disagreement_table, pairwise_agreement
from trim.schema import ANNOTATION_FIELDS


def run_intercoder_demo(repo_root: Path | None = None) -> Path:
    """Check the second-coder template and write a preparation report."""

    root = repo_root or Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    report_dir = root / "outputs" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    primary = pd.read_csv(data_dir / "demo_annotations.csv", dtype=str, keep_default_na=False)
    template = pd.read_csv(data_dir / "second_coder_template.csv", dtype=str, keep_default_na=False)
    combined = pd.concat(
        [primary.loc[primary["case_id"].isin(template["case_id"])], template],
        ignore_index=True,
    )

    template_columns_match = list(template.columns) == list(ANNOTATION_FIELDS)
    pairwise = pairwise_agreement(combined, "friction_locus")
    disagreements = disagreement_table(combined, DEFAULT_DISAGREEMENT_FIELDS)

    report_path = report_dir / "intercoder_demo_report.md"
    report_lines = [
        "# Intercoder Demo Report",
        "",
        "## Template Status",
        "",
        f"- Template rows: {len(template)}",
        f"- Columns match TRIM schema: {'yes' if template_columns_match else 'no'}",
        "- Coder-assigned fields are prepared for independent completion.",
        "",
        "## Current Comparison Status",
        "",
        "The included second-coder file is a template. Field-level reliability "
        "statistics become meaningful after independent labels are completed.",
        "",
        f"- Pairwise rows currently available for `friction_locus`: {len(pairwise)}",
        f"- Disagreement rows currently available: {len(disagreements)}",
        "",
        "## Next Step",
        "",
        "Return a completed second-coder CSV with a distinct `coder_id`, then "
        "run `trim.intercoder` utilities on the combined annotations.",
        "",
    ]
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    return report_path


def main() -> None:
    report_path = run_intercoder_demo()
    print(f"intercoder_report: {report_path}")


if __name__ == "__main__":
    main()
