"""Command-line interface for TRIM-HAA."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

from trim_haa import __version__
from trim_haa.comparison import compare_annotations
from trim_haa.locking import LockRecord, verify_locked_annotation
from trim_haa.schema import TrimHAAAnnotation
from trim_haa.validator import validate_core_records


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trim-haa",
        description="Validate, lock-check, and compare TRIM-HAA annotation records.",
    )
    subparsers = parser.add_subparsers(dest="command")

    version = subparsers.add_parser("version", help="Show the package version.")
    version.set_defaults(func=cmd_version)

    validate = subparsers.add_parser("validate", help="Validate one or more Core CSV files.")
    validate.add_argument("core_csv", nargs="+", type=Path)
    validate.set_defaults(func=cmd_validate)

    verify = subparsers.add_parser("verify-lock", help="Verify an annotation against a lock manifest.")
    verify.add_argument("annotation_csv", type=Path)
    verify.add_argument("lock_manifest_csv", type=Path)
    verify.set_defaults(func=cmd_verify_lock)

    compare = subparsers.add_parser("compare", help="Compare two annotation CSV files without a truth verdict.")
    compare.add_argument("left_csv", type=Path)
    compare.add_argument("right_csv", type=Path)
    compare.set_defaults(func=cmd_compare)

    walkthrough = subparsers.add_parser("run-walkthrough", help="Run the author-only In a Grove walkthrough.")
    walkthrough.set_defaults(func=cmd_run_walkthrough)

    synthetic = subparsers.add_parser("run-synthetic", help="Run the synthetic dry-run workflow.")
    synthetic.add_argument(
        "--invalid",
        action="store_true",
        help="Run the invalid synthetic fixture instead of the valid fixture.",
    )
    synthetic.set_defaults(func=cmd_run_synthetic)

    parser.set_defaults(func=cmd_help)
    return parser


def cmd_help(args: argparse.Namespace) -> int:
    build_parser().print_help()
    return 0


def cmd_version(args: argparse.Namespace) -> int:
    print(__version__)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    had_errors = False
    for path in args.core_csv:
        rows = _read_csv(path)
        annotations = [TrimHAAAnnotation.from_record(row) for row in rows]
        report = validate_core_records(annotations)
        errors = len(report.errors)
        warnings = len(report.warnings)
        had_errors = had_errors or errors > 0
        status = "error" if errors else "ok"
        print(
            f"{path}: records={len(rows)} errors={errors} warnings={warnings} status={status}"
        )
    return 1 if had_errors else 0


def cmd_verify_lock(args: argparse.Namespace) -> int:
    annotations = _read_csv(args.annotation_csv)
    locks = _read_csv(args.lock_manifest_csv)
    if not annotations:
        print(f"{args.annotation_csv}: no annotation rows found", file=sys.stderr)
        return 2
    if not locks:
        print(f"{args.lock_manifest_csv}: no lock rows found", file=sys.stderr)
        return 2
    annotation = TrimHAAAnnotation.from_record(annotations[0])
    lock_by_id = {row.get("annotation_id", ""): row for row in locks}
    lock_row = lock_by_id.get(annotation.annotation_id, locks[0])
    verified = verify_locked_annotation(annotation, LockRecord.from_record(lock_row))
    print(f"{annotation.annotation_id}: verification={'passed' if verified else 'failed'}")
    return 0 if verified else 1


def cmd_compare(args: argparse.Namespace) -> int:
    left_rows = _read_csv(args.left_csv)
    right_rows = _read_csv(args.right_csv)
    if not left_rows or not right_rows:
        print("compare requires at least one row in each CSV file", file=sys.stderr)
        return 2
    result = compare_annotations(left_rows[0], right_rows[0])
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_run_walkthrough(args: argparse.Namespace) -> int:
    return _run_repo_script("scripts/run_in_a_grove_walkthrough.py")


def cmd_run_synthetic(args: argparse.Namespace) -> int:
    root = _repo_root()
    fixture = (
        root / "examples" / "synthetic_dry_run" / ("invalid" if args.invalid else "valid")
    )
    return _run_repo_script(
        "scripts/run_trim_haa_synthetic_dry_run.py",
        "--root",
        str(fixture),
        *(["--expect-invalid"] if args.invalid else []),
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
    except FileNotFoundError:
        raise SystemExit(f"file not found: {path}") from None


def _run_repo_script(relative_path: str, *args: str) -> int:
    root = _repo_root()
    script = root / relative_path
    if not script.exists():
        print(
            f"{relative_path} is available only from a source checkout.",
            file=sys.stderr,
        )
        return 2
    completed = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=root,
        check=False,
    )
    return completed.returncode


def _repo_root() -> Path:
    for candidate in (Path.cwd(), *Path.cwd().parents):
        if (candidate / "src" / "trim_haa").is_dir():
            return candidate
    return Path.cwd()


if __name__ == "__main__":
    raise SystemExit(main())
