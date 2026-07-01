"""Validation for TRIM-HAA core records, provenance, and lineage."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable, Mapping

from trim_haa.comparison import copied_phrase_overlap
from trim_haa.exposure import ExposureEvent
from trim_haa.hashing import looks_like_sha256
from trim_haa.locking import LockRecord, verify_locked_annotation
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
        "self_reported_revision_reason",
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
            )
        )
    if provenance.self_reported_revision_reason == "other" and not provenance.self_reported_revision_note:
        issues.append(
            _issue(
                annotation_id,
                "self_reported_revision_note",
                "self_reported_revision_note is required when self_reported_revision_reason=other.",
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
    exposure_events: Iterable[ExposureEvent | Mapping[str, Any]] = (),
    lock_records: Iterable[LockRecord | Mapping[str, Any]] = (),
) -> ValidationReport:
    annotations = [_coerce_annotation(record) for record in core_records]
    provenance = [_coerce_provenance(record) for record in provenance_records]
    exposures = [_coerce_exposure_event(record) for record in exposure_events]
    locks = [_coerce_lock_record(record) for record in lock_records]
    report = validate_core_records(annotations)
    for record in provenance:
        report.extend(validate_provenance_record(record))
    report.extend(_validate_provenance_completeness(annotations, provenance))
    report.extend(_validate_stage_condition_matrix(annotations, provenance))
    report.extend(_validate_exposed_ai_links(annotations, provenance))
    report.extend(_validate_exposure_events(annotations, provenance, exposures))
    report.extend(_validate_locks(annotations, provenance, locks))
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
        if annotation.status != prov.lock_status:
            issues.append(
                _issue(
                    annotation.annotation_id,
                    "lock_status",
                    "Core status and provenance lock_status must match.",
                )
            )
    return issues


def _validate_stage_condition_matrix(
    annotations: list[TrimHAAAnnotation],
    provenance: list[AssistanceProvenance],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    prov_by_id = {record.annotation_id: record for record in provenance}
    for annotation in annotations:
        prov = prov_by_id.get(annotation.annotation_id)
        if prov is None:
            continue
        stage = annotation.annotation_stage
        if stage == "human_pre":
            issues.extend(
                _require_stage_values(
                    annotation,
                    prov,
                    actor_type="human",
                    parent_empty=True,
                    ai_output_exposed="none",
                    exposure_order="none",
                    interface_condition="independent",
                    pre_ai_annotation_locked="not_applicable",
                    exposed_empty=True,
                )
            )
        elif stage == "ai_independent":
            issues.extend(
                _require_stage_values(
                    annotation,
                    prov,
                    actor_type="model",
                    parent_empty=True,
                    ai_output_exposed="none",
                    exposure_order="none",
                    interface_condition="independent",
                    pre_ai_annotation_locked="not_applicable",
                    exposed_empty=True,
                )
            )
        elif stage == "human_post_ai":
            if annotation.actor_type != "human":
                issues.append(_issue(annotation.annotation_id, "actor_type", "human_post_ai requires actor_type=human."))
            if prov.ai_output_exposed == "none":
                issues.append(_issue(annotation.annotation_id, "ai_output_exposed", "human_post_ai requires ai_output_exposed other than none."))
            if prov.exposure_order not in {"human_first", "ai_first"}:
                issues.append(_issue(annotation.annotation_id, "exposure_order", "human_post_ai exposure_order must be human_first or ai_first."))
            if prov.interface_condition != "ai_review":
                issues.append(_issue(annotation.annotation_id, "interface_condition", "human_post_ai requires interface_condition=ai_review."))
            if prov.pre_ai_annotation_locked != "yes":
                issues.append(_issue(annotation.annotation_id, "pre_ai_annotation_locked", "human_post_ai requires pre_ai_annotation_locked=yes."))
        elif stage == "human_second_pass_control":
            issues.extend(
                _require_stage_values(
                    annotation,
                    prov,
                    actor_type="human",
                    parent_empty=False,
                    ai_output_exposed="none",
                    exposure_order="control_second_pass",
                    interface_condition="control_review",
                    pre_ai_annotation_locked="yes",
                    exposed_empty=True,
                )
            )
        elif stage == "adjudicated":
            if annotation.actor_type != "human":
                issues.append(_issue(annotation.annotation_id, "actor_type", "adjudicated records require actor_type=human."))
            if not annotation.parent_annotation_id:
                issues.append(_issue(annotation.annotation_id, "parent_annotation_id", "adjudicated records must reference a prior record."))
            if prov.interface_condition not in {"independent", "ai_review", "control_review"}:
                issues.append(_issue(annotation.annotation_id, "interface_condition", "adjudicated records require a known interface_condition."))
    return issues


def _require_stage_values(
    annotation: TrimHAAAnnotation,
    prov: AssistanceProvenance,
    *,
    actor_type: str,
    parent_empty: bool,
    ai_output_exposed: str,
    exposure_order: str,
    interface_condition: str,
    pre_ai_annotation_locked: str,
    exposed_empty: bool,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if annotation.actor_type != actor_type:
        issues.append(_issue(annotation.annotation_id, "actor_type", f"{annotation.annotation_stage} requires actor_type={actor_type}."))
    if parent_empty and annotation.parent_annotation_id:
        issues.append(_issue(annotation.annotation_id, "parent_annotation_id", f"{annotation.annotation_stage} requires empty parent_annotation_id."))
    if not parent_empty and not annotation.parent_annotation_id:
        issues.append(_issue(annotation.annotation_id, "parent_annotation_id", f"{annotation.annotation_stage} requires parent_annotation_id."))
    expected = {
        "ai_output_exposed": ai_output_exposed,
        "exposure_order": exposure_order,
        "interface_condition": interface_condition,
        "pre_ai_annotation_locked": pre_ai_annotation_locked,
    }
    for field_name, value in expected.items():
        if getattr(prov, field_name) != value:
            issues.append(_issue(annotation.annotation_id, field_name, f"{annotation.annotation_stage} requires {field_name}={value}."))
    if exposed_empty and (prov.exposed_ai_annotation_id or prov.exposed_model_run_id):
        issues.append(_issue(annotation.annotation_id, "exposed_ai_annotation_id", f"{annotation.annotation_stage} must not contain exposed AI linkage."))
    return issues


def _validate_exposed_ai_links(
    annotations: list[TrimHAAAnnotation],
    provenance: list[AssistanceProvenance],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    annotation_by_id = {record.annotation_id: record for record in annotations}
    prov_by_id = {record.annotation_id: record for record in provenance}
    for annotation in annotations:
        prov = prov_by_id.get(annotation.annotation_id)
        if prov is None:
            continue
        if annotation.annotation_stage == "human_post_ai":
            if not prov.exposed_ai_annotation_id:
                issues.append(_issue(annotation.annotation_id, "exposed_ai_annotation_id", "human_post_ai requires exposed_ai_annotation_id."))
                continue
            if not prov.exposed_model_run_id:
                issues.append(_issue(annotation.annotation_id, "exposed_model_run_id", "human_post_ai requires exposed_model_run_id."))
            ai = annotation_by_id.get(prov.exposed_ai_annotation_id)
            ai_prov = prov_by_id.get(prov.exposed_ai_annotation_id)
            if ai is None:
                issues.append(_issue(annotation.annotation_id, "exposed_ai_annotation_id", "exposed_ai_annotation_id does not reference an existing Core record."))
                continue
            if ai.annotation_stage != "ai_independent":
                issues.append(_issue(annotation.annotation_id, "exposed_ai_annotation_id", "exposed_ai_annotation_id must reference an ai_independent record."))
            if ai.case_id != annotation.case_id:
                issues.append(_issue(annotation.annotation_id, "exposed_ai_annotation_id", "Exposed AI record must have the same case_id."))
            if ai_prov is None:
                issues.append(_issue(annotation.annotation_id, "exposed_ai_annotation_id", "Exposed AI record must have a provenance row."))
            elif prov.exposed_model_run_id != ai_prov.model_run_id:
                issues.append(_issue(annotation.annotation_id, "exposed_model_run_id", "exposed_model_run_id must match exposed AI provenance model_run_id."))
        elif prov.exposed_ai_annotation_id or prov.exposed_model_run_id:
            issues.append(_issue(annotation.annotation_id, "exposed_ai_annotation_id", f"{annotation.annotation_stage} must not contain exposed AI linkage."))
    return issues


def _validate_exposure_events(
    annotations: list[TrimHAAAnnotation],
    provenance: list[AssistanceProvenance],
    events: list[ExposureEvent],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    annotation_by_id = {record.annotation_id: record for record in annotations}
    prov_by_id = {record.annotation_id: record for record in provenance}
    seen: set[str] = set()
    events_by_post: dict[str, list[ExposureEvent]] = {}
    for event in events:
        if event.exposure_event_id in seen:
            issues.append(_issue(event.exposure_event_id, "exposure_event_id", "Duplicate exposure_event_id."))
        seen.add(event.exposure_event_id)
        events_by_post.setdefault(event.human_post_annotation_id, []).append(event)
        post = annotation_by_id.get(event.human_post_annotation_id)
        pre = annotation_by_id.get(event.human_pre_annotation_id)
        ai = annotation_by_id.get(event.ai_annotation_id)
        ai_prov = prov_by_id.get(event.ai_annotation_id)
        if post is None:
            issues.append(_issue(event.exposure_event_id, "human_post_annotation_id", "Exposure event points to unknown human-post record."))
            continue
        if pre is None or post.parent_annotation_id != event.human_pre_annotation_id:
            issues.append(_issue(event.exposure_event_id, "human_pre_annotation_id", "Exposure event points to wrong human-pre record."))
        if post.case_id != event.case_id:
            issues.append(_issue(event.exposure_event_id, "case_id", "Exposure event points to wrong case."))
        if ai is None:
            issues.append(_issue(event.exposure_event_id, "ai_annotation_id", "Exposure event points to unknown AI record."))
        elif ai.annotation_stage != "ai_independent":
            issues.append(_issue(event.exposure_event_id, "ai_annotation_id", "Exposure event AI record must be ai_independent."))
        elif ai.case_id != event.case_id:
            issues.append(_issue(event.exposure_event_id, "case_id", "Exposure event AI record has wrong case_id."))
        if ai_prov is not None and event.model_run_id != ai_prov.model_run_id:
            issues.append(_issue(event.exposure_event_id, "model_run_id", "Exposure event model_run_id must match AI provenance."))
        post_prov = prov_by_id.get(event.human_post_annotation_id)
        if post_prov and (
            event.ai_annotation_id != post_prov.exposed_ai_annotation_id
            or event.model_run_id != post_prov.exposed_model_run_id
        ):
            issues.append(_issue(event.exposure_event_id, "ai_annotation_id", "Exposure event disagrees with human-post provenance exposure linkage."))
        issues.extend(_validate_exposure_event_timestamp(event))
    for post_id, post_events in events_by_post.items():
        if len(post_events) > 1:
            issues.append(_issue(post_id, "exposure_event_id", "Multiple exposure events for one human-post record.", severity="warning"))
    return issues


def _validate_locks(
    annotations: list[TrimHAAAnnotation],
    provenance: list[AssistanceProvenance],
    locks: list[LockRecord],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    annotation_by_id = {record.annotation_id: record for record in annotations}
    prov_by_id = {record.annotation_id: record for record in provenance}
    lock_by_annotation = {record.annotation_id: record for record in locks}
    required_parent_ids = {
        record.parent_annotation_id
        for record in annotations
        if record.annotation_stage in {"human_post_ai", "human_second_pass_control"}
        and record.parent_annotation_id
    }
    for parent_id in required_parent_ids:
        parent = annotation_by_id.get(parent_id)
        prov = prov_by_id.get(parent_id)
        lock = lock_by_annotation.get(parent_id)
        if parent is None:
            continue
        if parent.status != "locked":
            issues.append(_issue(parent_id, "status", "Parent record requires Core status=locked."))
        if prov is None or prov.lock_status != "locked":
            issues.append(_issue(parent_id, "lock_status", "Parent record requires provenance lock_status=locked."))
        if lock is None:
            issues.append(_issue(parent_id, "lock_manifest", "Parent record requires a lock-manifest row."))
        elif not verify_locked_annotation(parent, lock):
            issues.append(_issue(parent_id, "canonical_record_sha256", "Stored lock hash does not match current canonical annotation payload."))
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


def _validate_exposure_event_timestamp(event: ExposureEvent) -> list[ValidationIssue]:
    if _parse_timestamp(event.exposure_timestamp) is None and event.exposure_timestamp:
        return [
            _issue(
                event.exposure_event_id,
                "exposure_timestamp",
                "Exposure event timestamp is not valid ISO format.",
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


def _coerce_exposure_event(record: ExposureEvent | Mapping[str, Any]) -> ExposureEvent:
    if isinstance(record, ExposureEvent):
        return record
    return ExposureEvent.from_record(record)


def _coerce_lock_record(record: LockRecord | Mapping[str, Any]) -> LockRecord:
    if isinstance(record, LockRecord):
        return record
    return LockRecord.from_record(record)


def _issue(annotation_id: str, field: str, message: str, severity: str = "error") -> ValidationIssue:
    return ValidationIssue(annotation_id, field, severity, message)
