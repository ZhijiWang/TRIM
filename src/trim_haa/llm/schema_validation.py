"""JSON Schema validation with non-sensitive error summaries."""

from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator


def schema_error_summaries(instance: Any, schema: dict[str, Any]) -> list[str]:
    """Return deterministic validator/path summaries without echoing instance values."""

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda error: (list(error.absolute_path), error.validator or ""))
    summaries: list[str] = []
    for error in errors:
        path = "/".join(str(part) for part in error.absolute_path) or "<root>"
        keyword = error.validator or "schema"
        summaries.append(f"schema_validation_failed:{keyword}:{path}")
    return summaries


def validate_schema(instance: Any, schema: dict[str, Any]) -> None:
    summaries = schema_error_summaries(instance, schema)
    if summaries:
        raise ValueError(";".join(summaries))
