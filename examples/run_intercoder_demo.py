"""Prepare a small intercoder workflow report for TRIM."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from trim.intercoder import (
    DEFAULT_DISAGREEMENT_FIELDS,
    disagreement_table,
    pairwise_agreement,
    pairwise_compound_agreement,
)
from trim.schema import ANNOTATION_FIELDS


def run_intercoder_demo(repo_root: Path | None = None) -> Path:
    """Check the second-coder template and write a preparation report."""

    root = repo_root or PROJECT_ROOT
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
    compound_pairwise = pairwise_compound_agreement(
        combined,
        "rationale_mechanism",
    )
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
        "The included three-case second-coder file is a blank software and "
        "onboarding template. It does not provide reliability evidence.",
        "",
        f"- Pairwise rows currently available for `friction_locus`: {len(pairwise)}",
        "- Compound-aware pairwise rows currently available for "
        f"`rationale_mechanism`: {len(compound_pairwise)}",
        f"- Disagreement rows currently available: {len(disagreements)}",
        "",
        "## Next Step",
        "",
        "Return independently completed annotations with a distinct `coder_id`, "
        "then run `trim.intercoder` utilities before adjudication. Treat a "
        "ten-case run as a preliminary usability pilot, not a definitive "
        "reliability study.",
        "",
    ]
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    return report_path


def main() -> None:
    report_path = run_intercoder_demo()
    print(f"intercoder_report: {report_path}")


if __name__ == "__main__":
    main()
