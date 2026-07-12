"""Local-only JSON Schema resolution for frozen coder-schema references."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


def load_schema(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"schema must be a JSON object: {path}")
    return value


def local_schema_registry(root: str | Path) -> Registry:
    root_path = Path(root)
    coder_schema = load_schema(root_path / "schemas" / "human_llm_coder_output.schema.json")
    resource = Resource.from_contents(coder_schema)
    return Registry().with_resource(coder_schema["$id"], resource)


def schema_errors(instance: Any, schema: dict[str, Any], *, root: str | Path) -> list[str]:
    validator = Draft202012Validator(schema, registry=local_schema_registry(root))
    errors = sorted(validator.iter_errors(instance), key=lambda error: (list(error.absolute_path), error.validator or ""))
    return [
        f"schema_validation_failed:{error.validator or 'schema'}:{'/'.join(str(part) for part in error.absolute_path) or '<root>'}"
        for error in errors
    ]
