"""Validation utilities for human-created TRIM annotations.

The validator checks structure, required fields, signature form, and controlled
vocabulary use. Human coders provide the interpretive labels.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

import pandas as pd

from trim.schema import TrimAnnotation, coerce_string_list
from trim.signature import (
    SIGNATURE_FIELDS,
    FrictionSignature,
    parse_signature,
    validate_signature_values,
)
from trim.vocabulary import (
    CASE_SCOPES,
    CONTROLLED_VOCABULARIES,
    FUNCTION_LABELS,
    LANGUAGE_ACCESS_MODES,
    QUESTION_REVISION_VALUES,
    QUESTION_STATUS_VALUES,
    QUESTION_TYPES,
    YES_NO_VALUES,
    validate_closed_value,
)


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
    "coder_id",
)

RATIONALE_NOTE_MIN_LENGTH = 30
ALTERNATIVE_RATIONALE_MIN_LENGTH = 60
SHORT_RATIONALE_NOTE_MESSAGE = (
    "rationale_note is too short to support review; minimum recommended length "
    "is 30 characters."
)
SHORT_ALTERNATIVE_RATIONALE_MESSAGE = (
    "alternative_signature requires rationale_note documentation of at least "
    "60 characters."
)
EVIDENCE_NODES_REQUIRED_MESSAGE = (
    "evidence_nodes or primary_evidence_segment_ids requires at least one "
    "non-empty evidence node."
)
PRIMARY_EVIDENCE_REQUIRED_MESSAGE = (
    "primary_evidence_segment_ids is required for v0.2.1 coding records."
)
PRIMARY_EVIDENCE_LIMIT_MESSAGE = (
    "primary_evidence_segment_ids must contain one to three segment IDs."
)
LOW_UNCERTAINTY_WITH_ALTERNATIVE_MESSAGE = (
    "A complete alternative_signature should normally use at least medium "
    "uncertainty."
)

QUESTION_LOG_FIELDS: tuple[str, ...] = (
    "question_id",
    "case_id",
    "question_type",
    "question_text",
    "provisional_resolution",
    "did_question_change_code",
    "blocking_or_nonblocking",
    "requires_manual_revision",
    "coder_id",
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

    return _signature_validation_issues(
        _signature_to_values(parsed),
        case_id="<signature>",
    )


def validate_record(
    record: TrimAnnotation | Mapping[str, Any],
    *,
    known_segment_ids: Iterable[str] | Mapping[str, Iterable[str]] | None = None,
) -> list[ValidationIssue]:
    """Validate one human-created TRIM annotation record."""

    case_id = _field_value(record, "case_id") or "<missing case_id>"
    issues: list[ValidationIssue] = []

    issues.extend(_validate_required_fields(record, case_id))
    issues.extend(_validate_function_label(record, case_id))
    issues.extend(_validate_v0_2_1_metadata(record, case_id))
    issues.extend(_validate_evidence_fields(record, case_id, known_segment_ids))
    signature_values = {
        field_name: _field_value(record, field_name)
        for field_name in SIGNATURE_FIELDS
    }
    issues.extend(
        _signature_validation_issues(
            signature_values,
            case_id=case_id,
            include_required=False,
        )
    )
    issues.extend(_validate_rationale_note(record, case_id))
    issues.extend(_validate_alternative_signature(record, case_id))

    return issues


def validate_dataframe(df: pd.DataFrame) -> list[ValidationIssue]:
    """Validate all records in a pandas DataFrame."""

    issues: list[ValidationIssue] = []
    for record in df.to_dict(orient="records"):
        issues.extend(validate_record(record))
    return issues


def validate_question_log_record(
    record: Mapping[str, Any],
) -> list[ValidationIssue]:
    """Validate one v0.2.1 question-log row."""

    case_id = _clean_value(record.get("case_id", "")) or "<missing case_id>"
    issues: list[ValidationIssue] = []
    for field_name in QUESTION_LOG_FIELDS:
        if not _clean_value(record.get(field_name, "")):
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field=field_name,
                    severity="error",
                    message=f"{field_name} is required.",
                )
            )

    controlled_checks = {
        "question_type": QUESTION_TYPES,
        "did_question_change_code": YES_NO_VALUES,
        "blocking_or_nonblocking": QUESTION_STATUS_VALUES,
        "requires_manual_revision": QUESTION_REVISION_VALUES,
    }
    for field_name, allowed in controlled_checks.items():
        value = _clean_value(record.get(field_name, ""))
        if not value:
            continue
        for message in validate_closed_value(field_name, value, allowed):
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field=field_name,
                    severity="error",
                    message=message,
                )
            )
    return issues


def validate_question_log_dataframe(df: pd.DataFrame) -> list[ValidationIssue]:
    """Validate every row in a v0.2.1 question log."""

    return [
        issue
        for record in df.to_dict(orient="records")
        for issue in validate_question_log_record(record)
    ]


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


def _validate_function_label(
    record: TrimAnnotation | Mapping[str, Any],
    case_id: str,
) -> list[ValidationIssue]:
    function_label = _field_value(record, "function_label")
    if not function_label:
        return []
    return [
        ValidationIssue(
            case_id=case_id,
            field="function_label",
            severity="error",
            message=message,
        )
        for message in validate_closed_value(
            "function_label",
            function_label,
            FUNCTION_LABELS,
        )
    ]


def _validate_v0_2_1_metadata(
    record: TrimAnnotation | Mapping[str, Any],
    case_id: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    controlled_checks = {
        "language_access_mode": LANGUAGE_ACCESS_MODES,
        "case_scope": CASE_SCOPES,
        "cross_case_context_permitted": YES_NO_VALUES,
    }
    for field_name, allowed in controlled_checks.items():
        value = _field_value(record, field_name)
        if not value:
            continue
        issues.extend(
            ValidationIssue(
                case_id=case_id,
                field=field_name,
                severity="error",
                message=message,
            )
            for message in validate_closed_value(field_name, value, allowed)
        )

    if _is_v0_2_1_record(record):
        for field_name in (
            "language_access_mode",
            "case_scope",
            "cross_case_context_permitted",
        ):
            if not _field_value(record, field_name):
                issues.append(
                    ValidationIssue(
                        case_id=case_id,
                        field=field_name,
                        severity="error",
                        message=f"{field_name} is required for v0.2.1 records.",
                    )
                )

    required_context_segments = coerce_string_list(
        _raw_field_value(record, "required_context_segments")
    )
    if (
        required_context_segments
        and _field_value(record, "cross_case_context_permitted") != "yes"
    ):
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="cross_case_context_permitted",
                severity="error",
                message=(
                    "required_context_segments requires "
                    "cross_case_context_permitted=yes."
                ),
            )
        )
    return issues


def _validate_evidence_fields(
    record: TrimAnnotation | Mapping[str, Any],
    case_id: str,
    known_segment_ids: Iterable[str] | Mapping[str, Iterable[str]] | None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    evidence_nodes = coerce_string_list(_raw_field_value(record, "evidence_nodes"))
    primary_segments = coerce_string_list(
        _raw_field_value(record, "primary_evidence_segment_ids")
    )
    context_segments = coerce_string_list(
        _raw_field_value(record, "context_segment_ids")
    )

    if _is_v0_2_1_record(record) and not primary_segments:
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="primary_evidence_segment_ids",
                severity="error",
                message=PRIMARY_EVIDENCE_REQUIRED_MESSAGE,
            )
        )

    if not evidence_nodes and not primary_segments:
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="evidence_nodes",
                severity="error",
                message=EVIDENCE_NODES_REQUIRED_MESSAGE,
            )
        )

    if primary_segments and not 1 <= len(primary_segments) <= 3:
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="primary_evidence_segment_ids",
                severity="error",
                message=PRIMARY_EVIDENCE_LIMIT_MESSAGE,
            )
        )

    issues.extend(
        _duplicate_segment_issues(
            case_id,
            "primary_evidence_segment_ids",
            primary_segments,
        )
    )
    issues.extend(
        _duplicate_segment_issues(
            case_id,
            "context_segment_ids",
            context_segments,
        )
    )

    overlap = sorted(set(primary_segments) & set(context_segments))
    if overlap:
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="context_segment_ids",
                severity="error",
                message=(
                    "Segments cannot be both primary evidence and context: "
                    f"{', '.join(overlap)}."
                ),
            )
        )

    allowed_segments = _known_segments_for_case(known_segment_ids, case_id)
    if allowed_segments is not None:
        for field_name, values in (
            ("primary_evidence_segment_ids", primary_segments),
            ("context_segment_ids", context_segments),
        ):
            unknown = sorted(set(values) - allowed_segments)
            if unknown:
                issues.append(
                    ValidationIssue(
                        case_id=case_id,
                        field=field_name,
                        severity="error",
                        message=(
                            "Unknown segment IDs for this case: "
                            f"{', '.join(unknown)}."
                        ),
                    )
                )

    if (
        primary_segments
        and allowed_segments is not None
        and set(primary_segments) == allowed_segments
        and not context_segments
        and len(allowed_segments) > 1
    ):
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="primary_evidence_segment_ids",
                severity="warning",
                message=(
                    "All known segments are marked primary with no context "
                    "segments; confirm the selection is discriminative."
                ),
            )
        )

    return issues


def _signature_validation_issues(
    values: Mapping[str, Any],
    case_id: str,
    field_prefix: str = "",
    *,
    include_required: bool = True,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    errors_by_field = validate_signature_values(
        values,
        include_required=include_required,
    )
    for field_name, messages in errors_by_field.items():
        issue_field = f"{field_prefix}{field_name}"
        issues.extend(
            ValidationIssue(
                case_id=case_id,
                field=issue_field,
                severity="error",
                message=message,
            )
            for message in messages
        )
    return issues


def _validate_rationale_note(
    record: TrimAnnotation | Mapping[str, Any],
    case_id: str,
) -> list[ValidationIssue]:
    rationale_note = _field_value(record, "rationale_note")
    alternative_signature = _field_value(record, "alternative_signature")

    if alternative_signature:
        issues: list[ValidationIssue] = []
        uncertainty_flag = _field_value(record, "uncertainty_flag")
        if uncertainty_flag == "low":
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field="uncertainty_flag",
                    severity="warning",
                    message=LOW_UNCERTAINTY_WITH_ALTERNATIVE_MESSAGE,
                )
            )
        if len(rationale_note) < ALTERNATIVE_RATIONALE_MIN_LENGTH:
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field="rationale_note",
                    severity="error",
                    message=SHORT_ALTERNATIVE_RATIONALE_MESSAGE,
                )
            )
        return issues

    if not rationale_note:
        return [
            ValidationIssue(
                case_id=case_id,
                field="rationale_note",
                severity="error",
                message="rationale_note is required.",
            )
        ]

    if len(rationale_note) >= RATIONALE_NOTE_MIN_LENGTH:
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
            _signature_validation_issues(
                _signature_to_values(parsed),
                case_id=case_id,
                field_prefix="alternative_signature.",
            )
        )

    return issues


def _field_value(record: TrimAnnotation | Mapping[str, Any], field_name: str) -> str:
    return _clean_value(_raw_field_value(record, field_name))


def _raw_field_value(
    record: TrimAnnotation | Mapping[str, Any],
    field_name: str,
) -> Any:
    if isinstance(record, TrimAnnotation):
        return getattr(record, field_name, "")
    if isinstance(record, Mapping):
        return record.get(field_name, "")
    return getattr(record, field_name, "")


def _signature_to_values(signature: FrictionSignature) -> dict[str, str]:
    return signature.to_dict()


def _is_v0_2_1_record(record: TrimAnnotation | Mapping[str, Any]) -> bool:
    status = _field_value(record, "status")
    return (
        "v0_2_1" in status
        or bool(_field_value(record, "language_access_mode"))
        or bool(_field_value(record, "case_scope"))
        or bool(_field_value(record, "primary_evidence_segment_ids"))
        or bool(_field_value(record, "context_segment_ids"))
    )


def _duplicate_segment_issues(
    case_id: str,
    field_name: str,
    values: tuple[str, ...],
) -> list[ValidationIssue]:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if not duplicates:
        return []
    return [
        ValidationIssue(
            case_id=case_id,
            field=field_name,
            severity="error",
            message=f"{field_name} contains duplicate segment IDs: {', '.join(duplicates)}.",
        )
    ]


def _known_segments_for_case(
    known_segment_ids: Iterable[str] | Mapping[str, Iterable[str]] | None,
    case_id: str,
) -> set[str] | None:
    if known_segment_ids is None:
        return None
    if isinstance(known_segment_ids, Mapping):
        values = known_segment_ids.get(case_id)
        if values is None:
            return None
        return set(coerce_string_list(values))
    return set(coerce_string_list(known_segment_ids))


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()
