"""Run the synthetic-only, blocked human-coding scaffold dry-run."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trim_haa.human_coding.dry_run import run_human_coding_dry_run  # noqa: E402


def main() -> int:
    try:
        plan = run_human_coding_dry_run(ROOT)
    except Exception as exc:
        print(f"DRY_RUN_INVALID: {type(exc).__name__}: {exc}")
        return 1
    report = {
        "actual_adjudications_completed": plan["actual_adjudications_completed"],
        "actual_annotations_created": plan["actual_annotations_created"],
        "actual_annotations_locked": plan["actual_annotations_locked"],
        "actual_coding_sessions_started": plan["actual_coding_sessions_started"],
        "actual_packets_inspected": plan["actual_packets_inspected"],
        "coding_allowed": plan["coding_allowed"],
        "status": plan["overall_status"],
    }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    print("DRY_RUN_VALID_HUMAN_CODING_BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
