"""Run the TRIM workflow with an optional source-segment layer."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from trim.compare import (
    broad_family_table,
    contested_cases_table,
    same_cue_table,
    same_function_table,
)
from trim.graph import build_corpus_graph, export_graphml, export_json_graph
from trim.reports import generate_demo_report
from trim.validator import validation_report


GROVE_CASE_IDS = ["GROVE_TAJOMARU", "GROVE_MASAGO", "GROVE_TAKEHIRO"]


def load_and_link_segments(
    annotations_path: Path,
    segments_path: Path,
    case_ids: list[str] | None = None,
) -> pd.DataFrame:
    """Load demo annotations and link selected cases to source segment IDs."""

    selected_case_ids = case_ids or GROVE_CASE_IDS
    annotations = pd.read_csv(annotations_path, dtype=str, keep_default_na=False)
    segments = pd.read_csv(segments_path, dtype=str, keep_default_na=False)
    segment_lookup = {
        row["case_id"]: row
        for row in segments.to_dict(orient="records")
    }

    linked = annotations.loc[annotations["case_id"].isin(selected_case_ids)].copy()
    linked = linked.sort_values(
        by="case_id",
        key=lambda series: series.map({case_id: index for index, case_id in enumerate(selected_case_ids)}),
    )

    for index, row in linked.iterrows():
        segment = segment_lookup.get(row["case_id"])
        if not segment:
            continue
        linked.at[index, "evidence_anchor"] = (
            f"{segment['segment_id']}: {segment['original_text']}"
        )

    return linked.reset_index(drop=True)


def run_workflow(repo_root: Path | None = None) -> dict[str, Path]:
    """Run validation, comparison, reporting, and graph export for linked cases."""

    root = repo_root or Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    outputs_dir = root / "outputs"
    table_dir = outputs_dir / "tables" / "in_a_grove_segments"
    report_dir = outputs_dir / "reports"
    graph_dir = outputs_dir / "graphs"

    for path in (table_dir, report_dir, graph_dir):
        path.mkdir(parents=True, exist_ok=True)

    linked = load_and_link_segments(
        data_dir / "demo_annotations.csv",
        data_dir / "source_segments_demo.csv",
    )

    linked_path = data_dir / "in_a_grove_three_cases_with_segments.csv"
    linked.to_csv(linked_path, index=False)

    validation_path = report_dir / "in_a_grove_segments_validation.csv"
    validation_report(linked).to_csv(validation_path, index=False)

    report_path = report_dir / "in_a_grove_segments_report.md"
    generate_demo_report(linked, report_path)

    table_paths = {
        "same_function": table_dir / "same_function_different_signature.csv",
        "same_cue": table_dir / "same_cue_different_function.csv",
        "broad_family": table_dir / "broad_family_different_signature.csv",
        "contested_cases": table_dir / "contested_cases.csv",
    }
    same_function_table(linked).to_csv(table_paths["same_function"], index=False)
    same_cue_table(linked).to_csv(table_paths["same_cue"], index=False)
    broad_family_table(linked).to_csv(table_paths["broad_family"], index=False)
    contested_cases_table(linked).to_csv(table_paths["contested_cases"], index=False)

    graph = build_corpus_graph(linked)
    graphml_path = graph_dir / "in_a_grove_segments.graphml"
    json_path = graph_dir / "in_a_grove_segments.json"
    export_graphml(graph, graphml_path)
    export_json_graph(graph, json_path)

    return {
        "linked_annotations": linked_path,
        "validation": validation_path,
        "report": report_path,
        "graphml": graphml_path,
        "json": json_path,
        **table_paths,
    }


def main() -> None:
    outputs = run_workflow()
    for label, path in outputs.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
