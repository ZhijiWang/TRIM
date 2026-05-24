"""Command-line interface for TRIM."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import pandas as pd

from trim.compare import (
    broad_family_table,
    contested_cases_table,
    same_cue_table,
    same_function_table,
)
from trim.graph import build_corpus_graph, export_graphml, export_json_graph
from trim.io import annotations_to_dataframe, load_annotations
from trim.reports import generate_demo_report
from trim.validator import validation_report


def main(argv: Sequence[str] | None = None) -> int:
    """Run the TRIM command-line interface."""

    raw_argv = list(sys.argv[1:] if argv is None else argv)
    if argv is None:
        raw_argv = _normalize_executable_alias(raw_argv)
    parser = _build_parser()
    args = parser.parse_args(raw_argv)
    return args.func(args)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trim",
        description="Validate, compare, report, and graph TRIM annotations.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate",
        aliases=["trim-validate"],
        help="Validate annotations.",
    )
    validate_parser.add_argument("input", help="Input annotation CSV or JSON.")
    validate_parser.add_argument(
        "--out",
        required=True,
        help="Output validation report CSV.",
    )
    validate_parser.set_defaults(func=_cmd_validate)

    report_parser = subparsers.add_parser(
        "report",
        aliases=["trim-report"],
        help="Generate a demo comparison report.",
    )
    report_parser.add_argument("input", help="Input annotation CSV or JSON.")
    report_parser.add_argument(
        "--out",
        required=True,
        help="Output markdown report path.",
    )
    report_parser.set_defaults(func=_cmd_report)

    graph_parser = subparsers.add_parser(
        "graph",
        aliases=["trim-graph"],
        help="Generate graph outputs.",
    )
    graph_parser.add_argument("input", help="Input annotation CSV or JSON.")
    graph_parser.add_argument(
        "--graphml",
        required=True,
        help="Output GraphML path.",
    )
    graph_parser.add_argument(
        "--json",
        required=True,
        help="Output JSON graph path.",
    )
    graph_parser.set_defaults(func=_cmd_graph)

    compare_parser = subparsers.add_parser(
        "compare",
        aliases=["trim-compare"],
        help="Generate comparison tables.",
    )
    compare_parser.add_argument("input", help="Input annotation CSV or JSON.")
    compare_parser.add_argument(
        "--outdir",
        required=True,
        help="Output directory for comparison CSV tables.",
    )
    compare_parser.set_defaults(func=_cmd_compare)

    return parser


def _cmd_validate(args: argparse.Namespace) -> int:
    frame = _load_frame(args.input)
    report = validation_report(frame)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(output_path, index=False)
    print(f"Wrote validation report to {output_path}.")
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    frame = _load_frame(args.input)
    output_path = Path(args.out)
    generate_demo_report(frame, output_path)
    print(f"Wrote report to {output_path}.")
    return 0


def _cmd_graph(args: argparse.Namespace) -> int:
    frame = _load_frame(args.input)
    graph = build_corpus_graph(frame)
    graphml_path = Path(args.graphml)
    json_path = Path(args.json)
    export_graphml(graph, graphml_path)
    export_json_graph(graph, json_path)
    print(f"Wrote GraphML graph to {graphml_path}.")
    print(f"Wrote JSON graph to {json_path}.")
    return 0


def _cmd_compare(args: argparse.Namespace) -> int:
    frame = _load_frame(args.input)
    output_dir = Path(args.outdir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tables = {
        "same_function_different_signature.csv": same_function_table(frame),
        "same_cue_different_function.csv": same_cue_table(frame),
        "broad_family_different_signature.csv": broad_family_table(frame),
        "contested_cases.csv": contested_cases_table(frame),
    }
    for filename, table in tables.items():
        output_path = output_dir / filename
        table.to_csv(output_path, index=False)
        print(f"Wrote {output_path}.")
    return 0


def _load_frame(path: str | Path) -> pd.DataFrame:
    annotations = load_annotations(path)
    return annotations_to_dataframe(annotations)


def _normalize_executable_alias(argv: list[str]) -> list[str]:
    """Allow direct calls like ``trim-validate input.csv --out report.csv``."""

    executable = Path(sys.argv[0]).name
    command_aliases = {
        "trim-validate": "validate",
        "trim-report": "report",
        "trim-graph": "graph",
        "trim-compare": "compare",
    }
    command = command_aliases.get(executable)
    if command is None:
        return argv
    return [command, *argv]


if __name__ == "__main__":
    raise SystemExit(main())
