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
    manifest_metadata: Any = None,
    shared_context_registry: Any = None,
) -> list[ValidationIssue]:
    """Validate one human-created TRIM annotation record."""

    case_id = _field_value(record, "case_id") or "<missing case_id>"
    manifest = _records_by_key(manifest_metadata, "case_id")
    registry = _records_by_key(shared_context_registry, "shared_context_id")
    issues: list[ValidationIssue] = []

    issues.extend(_validate_required_fields(record, case_id))
    issues.extend(_validate_function_label(record, case_id))
    issues.extend(_validate_v0_2_1_metadata(record, case_id, manifest, registry))
    issues.extend(
        _validate_evidence_fields(
            record,
            case_id,
            known_segment_ids,
            manifest,
            registry,
        )
    )
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


def validate_dataframe(
    df: pd.DataFrame,
    *,
    known_segment_ids: Iterable[str] | Mapping[str, Iterable[str]] | None = None,
    manifest_metadata: Any = None,
    shared_context_registry: Any = None,
) -> list[ValidationIssue]:
    """Validate all records in a pandas DataFrame."""

    issues: list[ValidationIssue] = []
    for record in df.to_dict(orient="records"):
        issues.extend(
            validate_record(
                record,
                known_segment_ids=known_segment_ids,
                manifest_metadata=manifest_metadata,
                shared_context_registry=shared_context_registry,
            )
        )
    return issues


def validate_retest_manifest(
    manifest_metadata: Any,
    shared_context_registry: Any | None = None,
) -> list[ValidationIssue]:
    """Validate v0.2.1 retest manifest scope and shared-context references."""

    manifest = _records_by_key(manifest_metadata, "case_id")
    registry = _records_by_key(shared_context_registry, "shared_context_id")
    issues: list[ValidationIssue] = []
    all_segments = _all_manifest_segments(manifest)

    for case_id, record in manifest.items():
        issues.extend(_validate_manifest_scope_record(record, case_id, registry))
        required_segments = coerce_string_list(record.get("required_context_segments"))
        shared_ids = coerce_string_list(record.get("shared_context_ids"))
        permitted = _permitted_shared_segments(shared_ids, registry)

        for segment_id in required_segments:
            if segment_id not in all_segments:
                issues.append(
                    ValidationIssue(
                        case_id=case_id,
                        field="required_context_segments",
                        severity="error",
                        message=f"Unknown required context segment {segment_id!r}.",
                    )
                )
            elif shared_ids and segment_id not in permitted:
                issues.append(
                    ValidationIssue(
                        case_id=case_id,
                        field="required_context_segments",
                        severity="error",
                        message=(
                            f"Required context segment {segment_id!r} is outside "
                            "the declared shared-context group."
                        ),
                    )
                )
    return issues


def validate_shared_context_registry(
    manifest_metadata: Any,
    shared_context_registry: Any,
) -> list[ValidationIssue]:
    """Validate shared-context registry membership and segment references."""

    manifest = _records_by_key(manifest_metadata, "case_id")
    registry = _records_by_key(shared_context_registry, "shared_context_id")
    segment_to_case = _segment_to_case_map(manifest)
    issues: list[ValidationIssue] = []

    for shared_context_id, record in registry.items():
        members = coerce_string_list(record.get("member_case_ids"))
        permitted_segments = coerce_string_list(record.get("permitted_segment_ids"))
        if not members:
            issues.append(
                ValidationIssue(
                    case_id=shared_context_id,
                    field="member_case_ids",
                    severity="error",
                    message="member_case_ids is required.",
                )
            )
        if not permitted_segments:
            issues.append(
                ValidationIssue(
                    case_id=shared_context_id,
                    field="permitted_segment_ids",
                    severity="error",
                    message="permitted_segment_ids is required.",
                )
            )
        for member in members:
            if member not in manifest:
                issues.append(
                    ValidationIssue(
                        case_id=shared_context_id,
                        field="member_case_ids",
                        severity="error",
                        message=f"Unknown member case ID {member!r}.",
                    )
                )
        for segment_id in permitted_segments:
            owner_case = segment_to_case.get(segment_id)
            if owner_case is None:
                issues.append(
                    ValidationIssue(
                        case_id=shared_context_id,
                        field="permitted_segment_ids",
                        severity="error",
                        message=f"Unknown permitted segment ID {segment_id!r}.",
                    )
                )
            elif members and owner_case not in members:
                issues.append(
                    ValidationIssue(
                        case_id=shared_context_id,
                        field="permitted_segment_ids",
                        severity="error",
                        message=(
                            f"Permitted segment {segment_id!r} belongs to "
                            f"{owner_case!r}, which is not a member case."
                        ),
                    )
                )
    return issues


def validate_source_packet_segment_coverage(
    manifest_metadata: Any,
    source_packet_text: str,
) -> list[ValidationIssue]:
    """Validate that manifest segment IDs appear in the coder-facing packet."""

    manifest = _records_by_key(manifest_metadata, "case_id")
    packet = _clean_value(source_packet_text)
    issues: list[ValidationIssue] = []
    for case_id, record in manifest.items():
        for field_name in ("segment_ids", "required_context_segments"):
            for segment_id in coerce_string_list(record.get(field_name)):
                if segment_id and segment_id not in packet:
                    issues.append(
                        ValidationIssue(
                            case_id=case_id,
                            field=field_name,
                            severity="error",
                            message=(
                                f"Segment ID {segment_id!r} is not present in "
                                "the coder-facing source packet."
                            ),
                        )
                    )
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
    manifest: Mapping[str, Mapping[str, Any]],
    registry: Mapping[str, Mapping[str, Any]],
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
    shared_context_ids = coerce_string_list(
        _raw_field_value(record, "shared_context_ids")
    )
    case_scope = _field_value(record, "case_scope")
    cross_case_context_permitted = _field_value(record, "cross_case_context_permitted")

    if cross_case_context_permitted == "no":
        if shared_context_ids:
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field="shared_context_ids",
                    severity="error",
                    message=(
                        "shared_context_ids must be empty when "
                        "cross_case_context_permitted=no."
                    ),
                )
            )
        if required_context_segments:
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field="required_context_segments",
                    severity="error",
                    message=(
                        "required_context_segments must be empty when "
                        "cross_case_context_permitted=no."
                    ),
                )
            )

    if case_scope in {"supplied_related_cases", "shared_narrative_field"}:
        if not shared_context_ids:
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field="shared_context_ids",
                    severity="error",
                    message=(
                        f"case_scope={case_scope} requires shared_context_ids."
                    ),
                )
            )
        if cross_case_context_permitted != "yes":
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field="cross_case_context_permitted",
                    severity="error",
                    message=(
                        f"case_scope={case_scope} requires "
                        "cross_case_context_permitted=yes."
                    ),
                )
            )

    if case_scope == "local_passage" and required_context_segments:
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="required_context_segments",
                severity="error",
                message="case_scope=local_passage cannot use cross-case context.",
            )
        )

    if registry:
        for shared_context_id in shared_context_ids:
            if shared_context_id not in registry:
                issues.append(
                    ValidationIssue(
                        case_id=case_id,
                        field="shared_context_ids",
                        severity="error",
                        message=f"Unknown shared-context ID {shared_context_id!r}.",
                    )
                )
            else:
                members = set(
                    coerce_string_list(registry[shared_context_id].get("member_case_ids"))
                )
                if members and case_id not in members:
                    issues.append(
                        ValidationIssue(
                            case_id=case_id,
                            field="shared_context_ids",
                            severity="error",
                            message=(
                                f"Case {case_id!r} is not a member of "
                                f"shared-context ID {shared_context_id!r}."
                            ),
                        )
                    )
    elif shared_context_ids:
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="shared_context_ids",
                severity="error",
                message="shared_context_ids requires a shared-context registry.",
            )
        )

    if manifest and case_id not in manifest:
        issues.append(
            ValidationIssue(
                case_id=case_id,
                field="case_id",
                severity="error",
                message=f"case_id {case_id!r} is not present in manifest metadata.",
            )
        )

    if (
        required_context_segments
        and cross_case_context_permitted != "yes"
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

    if required_context_segments and registry:
        permitted = _permitted_shared_segments(shared_context_ids, registry)
        for segment_id in required_context_segments:
            if segment_id not in permitted:
                issues.append(
                    ValidationIssue(
                        case_id=case_id,
                        field="required_context_segments",
                        severity="error",
                        message=(
                            f"Required context segment {segment_id!r} is outside "
                            "the declared shared-context group."
                        ),
                    )
                )
    return issues


def _validate_evidence_fields(
    record: TrimAnnotation | Mapping[str, Any],
    case_id: str,
    known_segment_ids: Iterable[str] | Mapping[str, Iterable[str]] | None,
    manifest: Mapping[str, Mapping[str, Any]],
    registry: Mapping[str, Mapping[str, Any]],
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

    local_segments = _local_segments_for_case(manifest, known_segment_ids, case_id)
    shared_segments = _permitted_shared_segments(
        coerce_string_list(_raw_field_value(record, "shared_context_ids")),
        registry,
    )
    primary_allowed = local_segments
    context_allowed = (
        (local_segments | shared_segments)
        if local_segments is not None
        else _known_segments_for_case(known_segment_ids, case_id)
    )

    if primary_allowed is not None:
        unknown_primary = sorted(set(primary_segments) - primary_allowed)
        if unknown_primary:
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field="primary_evidence_segment_ids",
                    severity="error",
                    message=(
                        "Unknown segment IDs for local primary evidence in "
                        "this case: "
                        f"{', '.join(unknown_primary)}."
                    ),
                )
            )

    if context_allowed is not None:
        unknown_context = sorted(set(context_segments) - context_allowed)
        if unknown_context:
            issues.append(
                ValidationIssue(
                    case_id=case_id,
                    field="context_segment_ids",
                    severity="error",
                    message=(
                        "Unknown or unpermitted context segment IDs for this case: "
                        f"{', '.join(unknown_context)}."
                    ),
                )
            )

    if (
        primary_segments
        and primary_allowed is not None
        and set(primary_segments) == primary_allowed
        and not context_segments
        and len(primary_allowed) > 1
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


def _validate_manifest_scope_record(
    record: Mapping[str, Any],
    case_id: str,
    registry: Mapping[str, Mapping[str, Any]],
) -> list[ValidationIssue]:
    return _validate_v0_2_1_metadata(record, case_id, {}, registry)


def _records_by_key(table: Any, key: str) -> dict[str, Mapping[str, Any]]:
    if table is None:
        return {}
    if isinstance(table, pd.DataFrame):
        records = table.to_dict(orient="records")
    elif isinstance(table, Mapping):
        if all(isinstance(value, Mapping) for value in table.values()):
            return {
                _clean_value(record_key): value
                for record_key, value in table.items()
                if _clean_value(record_key)
            }
        records = [table]
    elif isinstance(table, Iterable) and not isinstance(table, (str, bytes)):
        records = list(table)
    else:
        raise TypeError(f"Unsupported table type for {key}: {type(table)!r}")

    keyed: dict[str, Mapping[str, Any]] = {}
    for record in records:
        if not isinstance(record, Mapping):
            continue
        record_key = _clean_value(record.get(key, ""))
        if record_key:
            keyed[record_key] = record
    return keyed


def _all_manifest_segments(
    manifest: Mapping[str, Mapping[str, Any]],
) -> set[str]:
    return {
        segment_id
        for record in manifest.values()
        for segment_id in coerce_string_list(record.get("segment_ids"))
    }


def _segment_to_case_map(
    manifest: Mapping[str, Mapping[str, Any]],
) -> dict[str, str]:
    return {
        segment_id: case_id
        for case_id, record in manifest.items()
        for segment_id in coerce_string_list(record.get("segment_ids"))
    }


def _local_segments_for_case(
    manifest: Mapping[str, Mapping[str, Any]],
    known_segment_ids: Iterable[str] | Mapping[str, Iterable[str]] | None,
    case_id: str,
) -> set[str] | None:
    if case_id in manifest:
        return set(coerce_string_list(manifest[case_id].get("segment_ids")))
    return _known_segments_for_case(known_segment_ids, case_id)


def _permitted_shared_segments(
    shared_context_ids: tuple[str, ...],
    registry: Mapping[str, Mapping[str, Any]],
) -> set[str]:
    return {
        segment_id
        for shared_context_id in shared_context_ids
        if shared_context_id in registry
        for segment_id in coerce_string_list(
            registry[shared_context_id].get("permitted_segment_ids")
        )
    }


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()
