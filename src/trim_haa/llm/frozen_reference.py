"""Read only allowlisted public metadata from the immutable PR #18 Git object."""

from __future__ import annotations

import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any


PR18_HEAD = "eac65f27bbe302a17e5f508ac1d516178e917aea"
PUBLIC_JSON_PATHS = {
    "data/studies/human_llm_pilot/allocation_manifest.json",
    "data/studies/human_llm_pilot/freeze_package_manifest.json",
    "data/studies/human_llm_pilot/manual_freeze_manifest.json",
    "data/studies/human_llm_pilot/prompt_assembly_manifest.json",
    "data/studies/human_llm_pilot/sample_manifest.json",
}
PUBLIC_BYTE_PATHS = PUBLIC_JSON_PATHS | {
    "schemas/human_llm_model_response.schema.json",
}


class FrozenReferenceError(RuntimeError):
    """Raised when the pinned public freeze reference is unavailable or altered."""


def _require_allowlisted(path: str) -> None:
    if path not in PUBLIC_BYTE_PATHS or "source_packet" in path:
        raise FrozenReferenceError(f"path is not an allowlisted PR #18 public metadata artifact: {path}")


def read_public_bytes(root: str | Path, path: str) -> bytes:
    """Read one allowlisted blob locally; this function performs no fetch or network access."""

    _require_allowlisted(path)
    result = subprocess.run(
        ["git", "show", f"{PR18_HEAD}:{path}"],
        cwd=Path(root),
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise FrozenReferenceError(
            f"pinned PR #18 public artifact is unavailable locally: {path}; no network fallback is permitted"
        )
    return result.stdout


def load_public_json(root: str | Path, path: str) -> dict[str, Any]:
    if path not in PUBLIC_JSON_PATHS:
        raise FrozenReferenceError(f"path is not an allowlisted PR #18 public JSON artifact: {path}")
    try:
        value = json.loads(read_public_bytes(root, path).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FrozenReferenceError(f"invalid pinned public JSON artifact: {path}") from exc
    if not isinstance(value, dict):
        raise FrozenReferenceError(f"pinned public JSON artifact must be an object: {path}")
    return value


def _canonical_unprefixed(record: dict[str, Any], excluded_field: str) -> str:
    payload = deepcopy(record)
    payload.pop(excluded_field, None)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _normalized_file_hash(value: bytes) -> str:
    normalized = value.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def load_and_verify_public_freeze(root: str | Path) -> dict[str, dict[str, Any]]:
    """Load the public planning manifests and verify the frozen hashes needed by dry-run."""

    allocation_path = "data/studies/human_llm_pilot/allocation_manifest.json"
    sample_path = "data/studies/human_llm_pilot/sample_manifest.json"
    prompt_path = "data/studies/human_llm_pilot/prompt_assembly_manifest.json"
    manual_path = "data/studies/human_llm_pilot/manual_freeze_manifest.json"
    freeze_path = "data/studies/human_llm_pilot/freeze_package_manifest.json"
    schema_path = "schemas/human_llm_model_response.schema.json"

    allocation = load_public_json(root, allocation_path)
    sample = load_public_json(root, sample_path)
    prompt = load_public_json(root, prompt_path)
    manual = load_public_json(root, manual_path)
    freeze = load_public_json(root, freeze_path)
    schema_bytes = read_public_bytes(root, schema_path)
    schema = json.loads(schema_bytes.decode("utf-8"))

    if _canonical_unprefixed(allocation, "allocation_hash") != allocation.get("allocation_hash"):
        raise FrozenReferenceError("PR #18 allocation canonical hash mismatch")
    if _canonical_unprefixed(sample, "sample_manifest_hash") != sample.get("sample_manifest_hash"):
        raise FrozenReferenceError("PR #18 sample canonical hash mismatch")
    if _normalized_file_hash(read_public_bytes(root, prompt_path)) != freeze.get("prompt_assembly_manifest_hash"):
        raise FrozenReferenceError("PR #18 prompt assembly manifest hash mismatch")
    if _normalized_file_hash(schema_bytes) != freeze.get("model_response_schema_hash"):
        raise FrozenReferenceError("PR #18 model response schema hash mismatch")
    if manual.get("manual_manifest_hash") != freeze.get("manual_manifest_hash"):
        raise FrozenReferenceError("PR #18 manual manifest reference mismatch")
    if sample.get("sample_manifest_hash") != allocation.get("sample_manifest_hash"):
        raise FrozenReferenceError("PR #18 sample/allocation reference mismatch")
    if len(allocation.get("case_order", [])) != sample.get("sample_size"):
        raise FrozenReferenceError("PR #18 allocation case count mismatch")
    if set(allocation.get("case_order", [])) != set(sample.get("selected_case_ids", [])):
        raise FrozenReferenceError("PR #18 allocation selected-case set mismatch")

    return {
        "allocation": allocation,
        "sample": sample,
        "prompt_assembly": prompt,
        "manual_freeze": manual,
        "freeze_package": freeze,
        "model_response_schema": schema,
    }
