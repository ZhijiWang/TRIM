"""Validation utilities for human-created TRIM annotations.

The validator checks structure, required fields, signature form, and controlled
vocabulary use. Human coders provide the interpretive labels.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

import pandas as pd

from trim.schema import TrimAnnotation
from trim.signature import SIGNATURE_FIELDS, FrictionSignature, parse_signature
from trim.vocabulary import CONTROLLED_VOCABULARIES


REQUIRED_FIELDS: tuple[str, ...] = (
    "case_id",
    "case_label",
    "source",
    "function_label",
    "evidence_anchor",
    "anchor_node",
    "friction_locus",
    "rationale_mechanism",
    "epistemic_support",
    "discourse_level",
    "temporal_orientation",
    "uncertainty_flag",
    "rationale_note",
    "coder_id",
)

CONTROLLED_FIELDS: tuple[str, ...] = (
    "friction_locus",
    "rationale_mechanism",
    "epistemic_support",
    "discourse_level",
    "temporal_orientation",
    "uncertainty_flag",
)

COMPOUND_FIELDS: tuple[str, ...] = (
    "rationale_mechanism",
    "epistemic_support",
)

RATIONALE_NOTE_MIN_LENGTH = 30
ALTERNATIVE_NOTE_TERMS: tuple[str, ...] = ("alternative", "contested", "dominant")
SHORT_RATIONALE_NOTE_MESSAGE = (
    "rationale_note is too short to support review; minimum recommended length "
    "is 30 characters."
)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A validation issue for one field in one case."""

    case_id: str
    field: str
    severity: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "case_id": self.case_id,
            "field": self.field,
            "severity": self.severity,
            "message": self.message,
        }


@dataclass(slots=True)
class ValidationReport:
    """A collection of validation issues."""

    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    def add(
        self,
        case_id: str,
        field: str,
        message: str,
        severity: str = "error",
    ) -> None:
        self.issues.append(
            ValidationIssue(
                case_id=case_id,
                field=field,
                severity=severity,
                message=message,
            )
        )

    def extend(self, other: "ValidationReport") -> None:
        self.issues.extend(other.issues)

    def to_rows(self) -> list[dict[str, str]]:
        return [issue.to_dict() for issue in self.issues]

    def format_text(self) -> str:
        if not self.issues:
            return "Validation passed with no issues."

        heading = "Validation passed with warnings:" if self.valid else "Validation issues:"
        details = "\n".join(
            f"[{issue.severity}] {issue.case_id} {issue.field}: {issue.message}"
            for issue in self.issues
        )
        return f"{heading}\n{details}"


def format_signature(record: TrimAnnotation | Mapping[str, Any]) -> str:
    """Format a record as a slash-delimited TRIM friction signature."""

    return " / ".join(_field_value(record, field_name) for field_name in SIGNATURE_FIELDS)


def validate_signature(signature: str) -> list[ValidationIssue]:
    """Validate a standalone slash-delimited TRIM friction signature."""

    try:
        parsed = parse_signature(signature)
    except ValueError as exc:
        return [
            ValidationIssue(
                case_id="<signature>",
                field="signature",
                severity="error",
                message=str(exc),
            )
        ]

    return _validate_signature_values(_signature_to_values(parsed), case_id="<signature>")


def validate_record(record: TrimAnnotation | Mapping[str, Any]) -> list[ValidationIssue]:
    """Validate one human-created TRIM annotation record."""

    case_id = _field_value(record, "case_id") or "<missing case_id>"
    issues: list[ValidationIssue] = []

    issues.extend(_validate_required_fields(record, case_id))
    signature_values = {
        field_name: _field_value(record, field_name)
        for field_name in SIGNATURE_FIELDS
    }
    issues.extend(_validate_signature_values(signature_values, case_id=case_id))
    issues.extend(_validate_rationale_note(record, case_id))
    issues.extend(_validate_alternative_signature(record, case_id))

    return issues


def validate_dataframe(df: pd.DataFrame) -> list[ValidationIssue]:
    """Validate all records in a pandas DataFrame."""

    issues: list[ValidationIssue] = []
    for record in df.to_dict(orient="records"):
        issues.extend(validate_record(record))
    return issues


def validation_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return validation issues as a pandas DataFrame."""

    columns = ["case_id", "field", "severity", "message"]
    rows = [issue.to_dict() for issue in validate_dataframe(df)]
    return pd.DataFrame(rows, columns=columns)


def validate_annotation(
    annotation: TrimAnnotation | Mapping[str, Any],
) -> ValidationReport:
    """Validate a single human-created TRIM annotation."""

    return ValidationReport(validate_record(annotation))


def validate_annotations(
    annotations: Iterable[TrimAnnotation | Mapping[str, Any]],
) -> ValidationReport:
    """Validate multiple TRIM annotations and combine the issues."""

    combined = ValidationReport()
    for annotation in annotations:
        combined.issues.extend(validate_record(annotation))
    return combined


def _validate_required_fields(
    record: TrimAnnotation | Mapping[str, Any],
    case_id: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for field_name in REQUIRED_FIELDS:
        if not _field_value(record, field_name):
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field=field_name,
                    severity="error",
                    message=f"{field_name} is required.",
                )
            )
    return issues


def _validate_signature_values(
    values: Mapping[str, str],
    case_id: str,
    field_prefix: str = "",
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for field_name in CONTROLLED_FIELDS:
        value = _clean_value(values.get(field_name, ""))
        if not value:
            continue

        allowed_values = CONTROLLED_VOCABULARIES[field_name]
        issue_field = f"{field_prefix}{field_name}"

        if field_name in COMPOUND_FIELDS:
            issues.extend(
                _validate_compound_value(
                    case_id=case_id,
                    field_name=issue_field,
                    value=value,
                    allowed_values=allowed_values,
                )
            )
        elif value not in allowed_values:
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field=issue_field,
                    severity="error",
                    message=(
                        f"{field_name} value {value!r} is not controlled vocabulary. "
                        f"Allowed values: {', '.join(sorted(allowed_values))}."
                    ),
                )
            )

    return issues


def _validate_compound_value(
    case_id: str,
    field_name: str,
    value: str,
    allowed_values: frozenset[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    parts = [part.strip() for part in value.split("+")]

    if any(not part for part in parts):
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field=field_name,
                severity="error",
                message=f"{field_name} contains an empty compound value.",
            )
        )

    if len(parts) > 2:
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field=field_name,
                severity="error",
                message=(
                    f"{field_name} contains {len(parts)} values; "
                    "no more than 2 are allowed."
                ),
            )
        )

    seen: set[str] = set()
    for part in parts:
        if not part:
            continue
        if part in seen:
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field=field_name,
                    severity="error",
                    message=f"{field_name} contains duplicate compound value {part!r}.",
                )
            )
        seen.add(part)

        if part not in allowed_values:
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field=field_name,
                    severity="error",
                    message=(
                        f"{field_name} value {part!r} is not controlled vocabulary. "
                        f"Allowed values: {', '.join(sorted(allowed_values))}."
                    ),
                )
            )

    return issues


def _validate_rationale_note(
    record: TrimAnnotation | Mapping[str, Any],
    case_id: str,
) -> list[ValidationIssue]:
    rationale_note = _field_value(record, "rationale_note")
    if not rationale_note or len(rationale_note) >= RATIONALE_NOTE_MIN_LENGTH:
        return []

    return [
        ValidationIssue(
            case_id=case_id,
            field="rationale_note",
            severity="warning",
            message=SHORT_RATIONALE_NOTE_MESSAGE,
        )
    ]


def _validate_alternative_signature(
    record: TrimAnnotation | Mapping[str, Any],
    case_id: str,
) -> list[ValidationIssue]:
    alternative_signature = _field_value(record, "alternative_signature")
    if not alternative_signature:
        return []

    issues: list[ValidationIssue] = []
    try:
        parsed = parse_signature(alternative_signature)
    except ValueError as exc:
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="alternative_signature",
                severity="error",
                message=str(exc),
            )
        )
    else:
        issues.extend(
            _validate_signature_values(
                _signature_to_values(parsed),
                case_id=case_id,
                field_prefix="alternative_signature.",
            )
        )

    rationale_note = _field_value(record, "rationale_note").lower()
    if not any(term in rationale_note for term in ALTERNATIVE_NOTE_TERMS):
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="alternative_signature",
                severity="error",
                message=(
                    "Alternative signature requires rationale note to mention "
                    "'alternative', 'contested', or 'dominant'."
                ),
            )
        )

    return issues


def _field_value(record: TrimAnnotation | Mapping[str, Any], field_name: str) -> str:
    if isinstance(record, TrimAnnotation):
        return _clean_value(getattr(record, field_name, ""))
    if isinstance(record, Mapping):
        return _clean_value(record.get(field_name, ""))
    return _clean_value(getattr(record, field_name, ""))


def _signature_to_values(signature: FrictionSignature) -> dict[str, str]:
    return signature.to_dict()


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()
