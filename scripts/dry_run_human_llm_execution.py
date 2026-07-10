"""Run the blocked, metadata-only human--LLM execution dry-run."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trim_haa.llm.dry_run import run_dry_run  # noqa: E402


def main() -> int:
    try:
        plan = run_dry_run(ROOT)
    except Exception as exc:  # fail closed with a non-sensitive summary
        print(f"DRY_RUN_INVALID: {type(exc).__name__}: {exc}")
        return 1
    report = {
        "actual_provider_calls_performed": plan["actual_provider_calls_performed"],
        "execution_allowed": plan["execution_allowed"],
        "outputs_generated": plan["outputs_generated"],
        "packets_inspected": plan["packets_inspected"],
        "requests_transmitted": plan["requests_transmitted"],
        "responses_received": plan["responses_received"],
        "status": plan["overall_execution_status"],
    }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    print("DRY_RUN_VALID_EXECUTION_BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
