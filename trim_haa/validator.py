"""Validation for TRIM-HAA core records, provenance, and lineage."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable, Mapping

from trim_haa.comparison import copied_phrase_overlap
from trim_haa.hashing import looks_like_sha256
from trim_haa.provenance import (
    AssistanceProvenance,
    PROVENANCE_CONTROLLED_FIELDS,
)
from trim_haa.schema import (
    CONTROLLED_FIELDS,
    CORE_FIELDS,
    TrimHAAAnnotation,
    clean_text,
)

REQUIRED_CORE_FIELDS: tuple[str, ...] = (
    "annotation_id",
    "case_id",
    "actor_id",
    "actor_type",
    "annotation_stage",
    "primary_evidence_segment_ids",
    "function_label",
    "rationale_mechanism",
    "uncertainty_flag",
    "rationale_note",
    "alternative_pathway_present",
    "status",
)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    annotation_id: str
    field: str
    severity: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "annotation_id": self.annotation_id,
            "field": self.field,
            "severity": self.severity,
            "message": self.message,
        }


@dataclass(slots=True)
class ValidationReport:
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

    def add(self, annotation_id: str, field: str, message: str, severity: str = "error") -> None:
        self.issues.append(ValidationIssue(annotation_id, field, severity, message))

    def extend(self, issues: Iterable[ValidationIssue]) -> None:
        self.issues.extend(issues)

    def to_rows(self) -> list[dict[str, str]]:
        return [issue.to_dict() for issue in self.issues]


def validate_core_record(record: TrimHAAAnnotation | Mapping[str, Any]) -> list[ValidationIssue]:
    annotation = _coerce_annotation(record)
    annotation_id = annotation.annotation_id or "<missing annotation_id>"
    issues: list[ValidationIssue] = []
    raw = annotation.to_record()

    for field_name in REQUIRED_CORE_FIELDS:
        value = raw.get(field_name)
        if field_name == "primary_evidence_segment_ids":
            if not value:
                issues.append(_issue(annotation_id, field_name, f"{field_name} is required."))
        elif not clean_text(value):
            issues.append(_issue(annotation_id, field_name, f"{field_name} is required."))

    for field_name, allowed in CONTROLLED_FIELDS.items():
        value = clean_text(raw.get(field_name, ""))
        if value and value not in allowed:
            issues.append(
                _issue(
                    annotation_id,
                    field_name,
                    f"{field_name} value {value!r} is not allowed. Allowed: {', '.join(sorted(allowed))}.",
                )
            )

    if annotation.annotation_stage in {"human_pre", "ai_independent"} and annotation.parent_annotation_id:
        issues.append(
            _issue(
                annotation_id,
                "parent_annotation_id",
                "Independent records must not have parent_annotation_id.",
            )
        )

    if annotation.actor_type == "model" and annotation.annotation_stage != "ai_independent":
        issues.append(
            _issue(annotation_id, "annotation_stage", "Model actors must use ai_independent stage.")
        )

    if annotation.annotation_stage == "ai_independent" and annotation.actor_type != "model":
        issues.append(_issue(annotation_id, "actor_type", "AI records require actor_type=model."))

    if annotation.has_alternative:
        if not annotation.alternative_mechanism:
            issues.append(
                _issue(
                    annotation_id,
                    "alternative_mechanism",
                    "alternative_mechanism is required when alternative_pathway_present=yes.",
                )
            )
        if not annotation.alternative_note:
            issues.append(
                _issue(
                    annotation_id,
                    "alternative_note",
                    "alternative_note is required when alternative_pathway_present=yes.",
                )
            )
    return issues


def validate_core_records(records: Iterable[TrimHAAAnnotation | Mapping[str, Any]]) -> ValidationReport:
    annotations = [_coerce_annotation(record) for record in records]
    report = ValidationReport()
    seen: dict[str, TrimHAAAnnotation] = {}
    for annotation in annotations:
        report.extend(validate_core_record(annotation))
        if annotation.annotation_id in seen:
            report.add(
                annotation.annotation_id,
                "annotation_id",
                "annotation_id must be globally unique.",
            )
            if annotation.status == "locked" or seen[annotation.annotation_id].status == "locked":
                report.add(
                    annotation.annotation_id,
                    "status",
                    "Locked records are immutable; duplicate locked annotation_id with differing rows is invalid.",
                )
        seen[annotation.annotation_id] = annotation
    report.extend(validate_relationships(annotations))
    return report


def validate_provenance_record(record: AssistanceProvenance | Mapping[str, Any]) -> list[ValidationIssue]:
    provenance = _coerce_provenance(record)
    annotation_id = provenance.annotation_id or "<missing annotation_id>"
    issues: list[ValidationIssue] = []
    raw = provenance.to_record()

    for field_name in (
        "annotation_id",
        "case_id",
        "actor_id",
        "actor_type",
        "annotation_stage",
        "pre_ai_annotation_locked",
        "ai_output_exposed",
        "exposure_order",
        "interface_condition",
        "retry_count",
        "regenerated_output",
        "adoption_type",
        "lock_status",
    ):
        if not clean_text(raw.get(field_name, "")):
            issues.append(_issue(annotation_id, field_name, f"{field_name} is required."))

    for field_name, allowed in PROVENANCE_CONTROLLED_FIELDS.items():
        value = clean_text(raw.get(field_name, ""))
        if value and value not in allowed:
            issues.append(
                _issue(
                    annotation_id,
                    field_name,
                    f"{field_name} value {value!r} is not allowed. Allowed: {', '.join(sorted(allowed))}.",
                )
            )

    for field_name in ("changed_label", "changed_primary_evidence", "changed_rationale_mechanism", "changed_uncertainty", "changed_alternative"):
        if not clean_text(raw.get(field_name, "")):
            issues.append(_issue(annotation_id, field_name, f"{field_name} is required."))

    if provenance.annotation_stage == "ai_independent":
        for field_name in (
            "model_provider",
            "model_name",
            "model_version_or_date",
            "prompt_template_id",
            "prompt_hash",
            "model_run_id",
            "retry_count",
            "regenerated_output",
        ):
            if not clean_text(raw.get(field_name, "")):
                issues.append(
                    _issue(
                        annotation_id,
                        field_name,
                        f"{field_name} is required for ai_independent records.",
                    )
                )
        if provenance.prompt_hash and not looks_like_sha256(provenance.prompt_hash):
            issues.append(_issue(annotation_id, "prompt_hash", "prompt_hash must be a SHA-256 hex digest."))
        if not provenance.system_prompt_hash:
            pass
        elif not looks_like_sha256(provenance.system_prompt_hash):
            issues.append(
                _issue(annotation_id, "system_prompt_hash", "system_prompt_hash must be a SHA-256 hex digest when supplied.")
            )
        if provenance.model_version_or_date and provenance.model_version_or_date.count("-") == 2:
            issues.append(
                _issue(
                    annotation_id,
                    "model_version_or_date",
                    "AI record uses a date label rather than exact provider-side version.",
                    severity="warning",
                )
            )
        try:
            if int(provenance.retry_count) > 1:
                issues.append(
                    _issue(
                        annotation_id,
                        "retry_count",
                        "Model output regenerated more than once.",
                        severity="warning",
                    )
                )
        except ValueError:
            issues.append(_issue(annotation_id, "retry_count", "retry_count must be an integer."))

    if provenance.annotation_stage == "human_post_ai" and provenance.ai_output_exposed == "none":
        issues.append(
            _issue(
                annotation_id,
                "ai_output_exposed",
                "human_post_ai submitted without exposure metadata.",
                severity="warning",
            )
        )

    issues.extend(_validate_timestamp_order(provenance))
    return issues


def validate_relationships(
    records: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
) -> list[ValidationIssue]:
    annotations = [_coerce_annotation(record) for record in records]
    index = {annotation.annotation_id: annotation for annotation in annotations}
    issues: list[ValidationIssue] = []

    for annotation in annotations:
        if annotation.parent_annotation_id == annotation.annotation_id and annotation.annotation_id:
            issues.append(_issue(annotation.annotation_id, "parent_annotation_id", "A record cannot parent itself."))
        if not annotation.parent_annotation_id:
            continue
        parent = index.get(annotation.parent_annotation_id)
        if parent is None:
            issues.append(_issue(annotation.annotation_id, "parent_annotation_id", "Parent annotation does not exist."))
            continue
        if parent.case_id != annotation.case_id:
            issues.append(_issue(annotation.annotation_id, "case_id", "Parent and child must have the same case_id."))
        if annotation.annotation_stage in {"human_post_ai", "human_second_pass_control"}:
            if parent.annotation_stage != "human_pre":
                issues.append(
                    _issue(annotation.annotation_id, "parent_annotation_id", f"{annotation.annotation_stage} parent must be human_pre.")
                )
            if parent.status != "locked":
                issues.append(
                    _issue(annotation.annotation_id, "parent_annotation_id", f"{annotation.annotation_stage} parent must be locked.")
                )
    issues.extend(_cycle_issues(index))
    return issues


def validate_dataset(
    core_records: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
    provenance_records: Iterable[AssistanceProvenance | Mapping[str, Any]] = (),
) -> ValidationReport:
    annotations = [_coerce_annotation(record) for record in core_records]
    provenance = [_coerce_provenance(record) for record in provenance_records]
    report = validate_core_records(annotations)
    for record in provenance:
        report.extend(validate_provenance_record(record))
    report.extend(_validate_provenance_completeness(annotations, provenance))
    report.extend(_validate_changed_flag_consistency(annotations, provenance))
    report.extend(_copying_warnings(annotations))
    return report


def _validate_provenance_completeness(
    annotations: list[TrimHAAAnnotation],
    provenance: list[AssistanceProvenance],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    prov_by_id = {record.annotation_id: record for record in provenance}
    for annotation in annotations:
        if annotation.annotation_id not in prov_by_id:
            issues.append(
                _issue(
                    annotation.annotation_id,
                    "provenance",
                    "No provenance sidecar row for annotation.",
                    severity="warning",
                )
            )
            continue
        prov = prov_by_id[annotation.annotation_id]
        for field_name in ("parent_annotation_id", "case_id", "actor_id", "actor_type", "annotation_stage"):
            if getattr(annotation, field_name) != getattr(prov, field_name):
                issues.append(
                    _issue(
                        annotation.annotation_id,
                        field_name,
                        f"Core and provenance disagree on {field_name}.",
                    )
                )
    return issues


def _validate_changed_flag_consistency(
    annotations: list[TrimHAAAnnotation],
    provenance: list[AssistanceProvenance],
) -> list[ValidationIssue]:
    index = {annotation.annotation_id: annotation for annotation in annotations}
    prov_by_id = {record.annotation_id: record for record in provenance}
    issues: list[ValidationIssue] = []
    field_pairs = {
        "changed_label": "function_label",
        "changed_primary_evidence": "primary_evidence_segment_ids",
        "changed_rationale_mechanism": "rationale_mechanism",
        "changed_uncertainty": "uncertainty_flag",
        "changed_alternative": "alternative_pathway_present",
    }
    for annotation in annotations:
        if not annotation.parent_annotation_id:
            continue
        parent = index.get(annotation.parent_annotation_id)
        prov = prov_by_id.get(annotation.annotation_id)
        if parent is None or prov is None:
            continue
        for flag_name, core_field in field_pairs.items():
            flag = getattr(prov, flag_name)
            if flag == "not_applicable":
                continue
            changed = getattr(parent, core_field) != getattr(annotation, core_field)
            if flag == "no" and changed:
                issues.append(
                    _issue(annotation.annotation_id, flag_name, "Changed field marked no but values differ.", severity="warning")
                )
            elif flag == "yes" and not changed:
                issues.append(
                    _issue(annotation.annotation_id, flag_name, "Changed field marked yes but values are identical.", severity="warning")
                )
    return issues


def _copying_warnings(annotations: list[TrimHAAAnnotation]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    by_case = {}
    for annotation in annotations:
        by_case.setdefault(annotation.case_id, []).append(annotation)
    for case_annotations in by_case.values():
        ai_records = [row for row in case_annotations if row.annotation_stage == "ai_independent"]
        post_records = [row for row in case_annotations if row.annotation_stage == "human_post_ai"]
        for post in post_records:
            for ai in ai_records:
                if copied_phrase_overlap(post.rationale_note, ai.rationale_note) >= 0.8:
                    issues.append(
                        _issue(
                            post.annotation_id,
                            "rationale_note",
                            "Rationale contains unusually high copied phrase overlap with AI rationale.",
                            severity="warning",
                        )
                    )
                if _submitted_fields_equal(post, ai):
                    issues.append(
                        _issue(
                            post.annotation_id,
                            "annotation",
                            "Post-AI record is identical to AI record across all submitted core fields.",
                            severity="warning",
                        )
                    )
    return issues


def _cycle_issues(index: dict[str, TrimHAAAnnotation]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for annotation_id in index:
        seen: set[str] = set()
        current = index[annotation_id]
        while current.parent_annotation_id:
            if current.annotation_id in seen:
                issues.append(_issue(annotation_id, "parent_annotation_id", "Cycles are forbidden."))
                break
            seen.add(current.annotation_id)
            parent = index.get(current.parent_annotation_id)
            if parent is None:
                break
            current = parent
    return issues


def _validate_timestamp_order(prov: AssistanceProvenance) -> list[ValidationIssue]:
    if not prov.exposure_timestamp or not prov.post_edit_timestamp:
        return []
    exposure = _parse_timestamp(prov.exposure_timestamp)
    post = _parse_timestamp(prov.post_edit_timestamp)
    if exposure is None or post is None:
        return []
    if post < exposure:
        return [
            _issue(
                prov.annotation_id,
                "post_edit_timestamp",
                "post_edit_timestamp must not precede exposure_timestamp.",
            )
        ]
    return []


def _parse_timestamp(value: str) -> datetime | None:
    text = clean_text(value)
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _submitted_fields_equal(left: TrimHAAAnnotation, right: TrimHAAAnnotation) -> bool:
    fields = (
        "primary_evidence_segment_ids",
        "function_label",
        "rationale_mechanism",
        "uncertainty_flag",
        "rationale_note",
        "alternative_pathway_present",
        "alternative_mechanism",
        "alternative_note",
    )
    return all(getattr(left, field_name) == getattr(right, field_name) for field_name in fields)


def _coerce_annotation(record: TrimHAAAnnotation | Mapping[str, Any]) -> TrimHAAAnnotation:
    if isinstance(record, TrimHAAAnnotation):
        return record
    return TrimHAAAnnotation.from_record(record)


def _coerce_provenance(record: AssistanceProvenance | Mapping[str, Any]) -> AssistanceProvenance:
    if isinstance(record, AssistanceProvenance):
        return record
    return AssistanceProvenance.from_record(record)


def _issue(annotation_id: str, field: str, message: str, severity: str = "error") -> ValidationIssue:
    return ValidationIssue(annotation_id, field, severity, message)

