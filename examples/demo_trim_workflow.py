"""Run a minimal TRIM validation workflow on the demo data."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from trim.io import (
    annotations_to_dataframe,
    build_annotation_graph,
    load_annotations,
    save_annotations,
)
from trim.compare import (
    broad_family_table,
    contested_cases_table,
    same_cue_table,
    same_function_table,
)
from trim.graph import (
    build_corpus_graph,
    export_graphml,
    export_json_graph,
    graph_summary,
)
from trim.reports import generate_demo_report
from trim.signature import compare_annotations, signature_from_annotation
from trim.validator import (
    format_signature,
    validate_annotations,
    validate_signature,
    validation_report,
)


def main() -> int:
    csv_path = PROJECT_ROOT / "data" / "demo_annotations.csv"
    json_path = PROJECT_ROOT / "data" / "demo_annotations.json"
    output_path = PROJECT_ROOT / "outputs" / "tables" / "demo_annotations_validated.csv"
    same_function_path = (
        PROJECT_ROOT / "outputs" / "tables" / "same_function_different_signature.csv"
    )
    same_cue_path = PROJECT_ROOT / "outputs" / "tables" / "same_cue_different_function.csv"
    broad_family_path = (
        PROJECT_ROOT / "outputs" / "tables" / "broad_family_different_signature.csv"
    )
    contested_cases_path = PROJECT_ROOT / "outputs" / "tables" / "contested_cases.csv"
    comparison_report_path = PROJECT_ROOT / "outputs" / "reports" / "demo_comparison_report.md"
    graphml_path = PROJECT_ROOT / "outputs" / "graphs" / "demo_corpus.graphml"
    json_graph_path = PROJECT_ROOT / "outputs" / "graphs" / "demo_corpus_graph.json"
    graph_summary_path = PROJECT_ROOT / "outputs" / "reports" / "graph_summary.md"

    annotations = load_annotations(csv_path)
    json_annotations = load_annotations(json_path)

    report = validate_annotations(annotations)
    frame = annotations_to_dataframe(annotations)
    issues_table = validation_report(frame)

    print(f"Loaded {len(annotations)} CSV annotations.")
    print(f"Loaded {len(json_annotations)} JSON annotations.")
    print(report.format_text())

    if not issues_table.empty:
        print("\nStructured validation issues:")
        print(issues_table.to_string(index=False))

    first_formatted_signature = format_signature(annotations[0])
    first_signature_issues = validate_signature(first_formatted_signature)
    print("\nFormatted first signature:", first_formatted_signature)
    print(
        "Standalone signature validation:",
        "passed" if not first_signature_issues else "failed",
    )

    save_annotations(output_path, annotations)
    print(f"Wrote normalized annotations to {output_path}.")

    same_function = same_function_table(frame)
    same_cue = same_cue_table(frame)
    broad_family = broad_family_table(frame)
    contested_cases = contested_cases_table(frame)

    same_function.to_csv(same_function_path, index=False)
    same_cue.to_csv(same_cue_path, index=False)
    broad_family.to_csv(broad_family_path, index=False)
    contested_cases.to_csv(contested_cases_path, index=False)
    generate_demo_report(frame, comparison_report_path)

    print(f"Wrote same-function comparison table to {same_function_path}.")
    print(f"Wrote same-cue comparison table to {same_cue_path}.")
    print(f"Wrote broad-family comparison table to {broad_family_path}.")
    print(f"Wrote contested-cases table to {contested_cases_path}.")
    print(f"Wrote comparison report to {comparison_report_path}.")

    edge_attributed_graph = build_annotation_graph(annotations)
    graph = build_corpus_graph(frame)
    export_graphml(graph, graphml_path)
    export_json_graph(graph, json_graph_path)
    _write_graph_summary(graph_summary(graph), graph_summary_path)

    print(
        "Built schema-component graph with "
        f"{edge_attributed_graph.number_of_nodes()} nodes "
        f"and {edge_attributed_graph.number_of_edges()} edges."
    )
    print(
        "Built corpus graph with "
        f"{graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges."
    )
    print(f"Wrote GraphML graph to {graphml_path}.")
    print(f"Wrote JSON graph to {json_graph_path}.")
    print(f"Wrote graph summary to {graph_summary_path}.")

    if len(annotations) >= 2:
        first_signature = signature_from_annotation(annotations[0])
        second_signature = signature_from_annotation(annotations[1])
        comparison = compare_annotations(first_signature, second_signature)
        differing_fields = [
            field_name
            for field_name, values in comparison.items()
            if not values["match"]
        ]
        print("First signature:", first_signature.to_compact())
        print("Second signature:", second_signature.to_compact())
        print("Differing signature fields:", ", ".join(differing_fields) or "none")

    return 0


def _write_graph_summary(summary: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# TRIM Graph Summary",
        "",
        f"- Nodes: {summary['node_count']}",
        f"- Edges: {summary['edge_count']}",
        "",
        "## Node Types",
        "",
        _dict_table(summary["node_types"], "node_type", "count"),
        "",
        "## Friction Loci",
        "",
        _dict_table(summary["friction_locus_counts"], "friction_locus", "count"),
        "",
        "## Rationale Mechanisms",
        "",
        _dict_table(summary["rationale_mechanism_counts"], "rationale_mechanism", "count"),
        "",
        "## Functions",
        "",
        _dict_table(summary["function_counts"], "function_label", "count"),
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def _dict_table(values: dict, label_name: str, count_name: str) -> str:
    if not values:
        return "_No rows._"

    lines = [
        f"| {label_name} | {count_name} |",
        "| --- | ---: |",
    ]
    for label, count in values.items():
        lines.append(f"| {label} | {count} |")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
