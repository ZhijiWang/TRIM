"""Run the exact-model, metadata-only OpenAI account audit."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trim_haa.llm.provider_metadata import audit_exact_model_metadata  # noqa: E402


def main() -> int:
    result = audit_exact_model_metadata(os.environ.get("OPENAI_API_KEY"))
    print(json.dumps(result.public_dict(), sort_keys=True, separators=(",", ":")))
    return 0 if result.audit_status in {
        "BLOCKED_NO_CREDENTIAL_AVAILABLE",
        "METADATA_ACCESS_VERIFIED_INFERENCE_NOT_AUTHORIZED",
    } else 1


if __name__ == "__main__":
    raise SystemExit(main())
