"""Human-AI assistance provenance sidecar records and lineage utilities."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

from trim_haa.hashing import sha256_text
from trim_haa.schema import TrimHAAAnnotation, clean_text

PROVENANCE_FIELDS: tuple[str, ...] = (
    "annotation_id",
    "parent_annotation_id",
    "case_id",
    "actor_id",
    "actor_type",
    "annotation_stage",
    "pre_ai_annotation_locked",
    "ai_output_exposed",
    "exposure_order",
    "interface_condition",
    "model_provider",
    "model_name",
    "model_version_or_date",
    "prompt_template_id",
    "prompt_hash",
    "system_prompt_hash",
    "model_run_id",
    "retry_count",
    "regenerated_output",
    "temperature_or_sampling",
    "output_components_shown",
    "exposure_timestamp",
    "post_edit_timestamp",
    "changed_label",
    "changed_primary_evidence",
    "changed_rationale_mechanism",
    "changed_uncertainty",
    "changed_alternative",
    "adoption_type",
    "human_revision_reason",
    "prior_access_to_other_annotations",
    "lock_status",
)

PRE_AI_LOCK_VALUES = frozenset({"yes", "no", "not_applicable"})
AI_OUTPUT_EXPOSED_VALUES = frozenset(
    {
        "none",
        "label_only",
        "evidence_only",
        "label_and_evidence",
        "rationale_only",
        "full_core_record",
        "full_core_and_depth",
    }
)
EXPOSURE_ORDER_VALUES = frozenset(
    {"none", "human_first", "ai_first", "control_second_pass"}
)
INTERFACE_CONDITION_VALUES = frozenset(
    {"independent", "ai_review", "control_review"}
)
CHANGE_VALUES = frozenset({"yes", "no", "not_applicable"})
ADOPTION_TYPES = frozenset(
    {
        "no_change",
        "accepted_ai_label",
        "accepted_ai_evidence",
        "accepted_ai_mechanism",
        "partial_ai_adoption",
        "ai_prompted_new_human_interpretation",
        "rejected_ai_output",
        "changed_after_rereading_not_ai",
        "unclear",
    }
)
LOCK_STATUS_VALUES = frozenset({"draft", "locked", "superseded"})

PROVENANCE_CONTROLLED_FIELDS: dict[str, frozenset[str]] = {
    "pre_ai_annotation_locked": PRE_AI_LOCK_VALUES,
    "ai_output_exposed": AI_OUTPUT_EXPOSED_VALUES,
    "exposure_order": EXPOSURE_ORDER_VALUES,
    "interface_condition": INTERFACE_CONDITION_VALUES,
    "changed_label": CHANGE_VALUES,
    "changed_primary_evidence": CHANGE_VALUES,
    "changed_rationale_mechanism": CHANGE_VALUES,
    "changed_uncertainty": CHANGE_VALUES,
    "changed_alternative": CHANGE_VALUES,
    "adoption_type": ADOPTION_TYPES,
    "lock_status": LOCK_STATUS_VALUES,
}


@dataclass(slots=True)
class AssistanceProvenance:
    """Sidecar metadata for how an annotation record was produced/exposed."""

    annotation_id: str = ""
    parent_annotation_id: str = ""
    case_id: str = ""
    actor_id: str = ""
    actor_type: str = ""
    annotation_stage: str = ""
    pre_ai_annotation_locked: str = "not_applicable"
    ai_output_exposed: str = "none"
    exposure_order: str = "none"
    interface_condition: str = "independent"
    model_provider: str = ""
    model_name: str = ""
    model_version_or_date: str = ""
    prompt_template_id: str = ""
    prompt_hash: str = ""
    system_prompt_hash: str = ""
    model_run_id: str = ""
    retry_count: str = "0"
    regenerated_output: str = "no"
    temperature_or_sampling: str = ""
    output_components_shown: str = ""
    exposure_timestamp: str = ""
    post_edit_timestamp: str = ""
    changed_label: str = "not_applicable"
    changed_primary_evidence: str = "not_applicable"
    changed_rationale_mechanism: str = "not_applicable"
    changed_uncertainty: str = "not_applicable"
    changed_alternative: str = "not_applicable"
    adoption_type: str = "no_change"
    human_revision_reason: str = ""
    prior_access_to_other_annotations: str = "none"
    lock_status: str = "draft"

    def __post_init__(self) -> None:
        for field_name in PROVENANCE_FIELDS:
            setattr(self, field_name, clean_text(getattr(self, field_name)))

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "AssistanceProvenance":
        values = {field_name: record.get(field_name, "") for field_name in PROVENANCE_FIELDS}
        return cls(**values)

    def to_record(self) -> dict[str, str]:
        return asdict(self)


def prompt_hash(prompt_text: str) -> str:
    """Hash exact prompt text; hidden chain-of-thought must never be supplied."""

    return sha256_text(prompt_text)


def annotation_index(
    annotations: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
) -> dict[str, TrimHAAAnnotation]:
    index: dict[str, TrimHAAAnnotation] = {}
    for annotation in annotations:
        if not isinstance(annotation, TrimHAAAnnotation):
            annotation = TrimHAAAnnotation.from_record(annotation)
        index[annotation.annotation_id] = annotation
    return index


def children_by_parent(
    annotations: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
) -> dict[str, list[str]]:
    children: dict[str, list[str]] = {}
    for annotation in annotations:
        if not isinstance(annotation, TrimHAAAnnotation):
            annotation = TrimHAAAnnotation.from_record(annotation)
        if annotation.parent_annotation_id:
            children.setdefault(annotation.parent_annotation_id, []).append(
                annotation.annotation_id
            )
    return children


def lineage_for(
    annotation_id: str,
    annotations: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
) -> list[str]:
    """Return parent-to-child lineage ending at annotation_id."""

    index = annotation_index(annotations)
    lineage: list[str] = []
    seen: set[str] = set()
    current_id = annotation_id
    while current_id:
        if current_id in seen:
            raise ValueError(f"Cycle detected at annotation_id {current_id!r}.")
        seen.add(current_id)
        current = index.get(current_id)
        if current is None:
            raise ValueError(f"Unknown annotation_id {current_id!r}.")
        lineage.append(current_id)
        current_id = current.parent_annotation_id
    return list(reversed(lineage))


def export_lineage_rows(
    annotations: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
) -> list[dict[str, str]]:
    index = annotation_index(annotations)
    rows: list[dict[str, str]] = []
    for annotation in index.values():
        rows.append(
            {
                "annotation_id": annotation.annotation_id,
                "parent_annotation_id": annotation.parent_annotation_id,
                "case_id": annotation.case_id,
                "annotation_stage": annotation.annotation_stage,
                "actor_id": annotation.actor_id,
                "actor_type": annotation.actor_type,
            }
        )
    return rows

