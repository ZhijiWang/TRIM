"""Lightweight TRIM-HAA core annotation schema."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

ACTOR_TYPES: frozenset[str] = frozenset({"human", "model"})
ANNOTATION_STAGES: frozenset[str] = frozenset(
    {
        "human_pre",
        "ai_independent",
        "human_post_ai",
        "human_second_pass_control",
        "adjudicated",
    }
)
UNCERTAINTY_FLAGS: frozenset[str] = frozenset({"low", "medium", "high"})
YES_NO_VALUES: frozenset[str] = frozenset({"yes", "no"})
CORE_STATUS_VALUES: frozenset[str] = frozenset({"draft", "locked", "superseded"})

CORE_FIELDS: tuple[str, ...] = (
    "annotation_id",
    "case_id",
    "parent_annotation_id",
    "actor_id",
    "actor_type",
    "annotation_stage",
    "primary_evidence_segment_ids",
    "function_label",
    "rationale_mechanism",
    "uncertainty_flag",
    "rationale_note",
    "alternative_pathway_present",
    "alternative_mechanism",
    "alternative_note",
    "status",
)

CONTROLLED_FIELDS: dict[str, frozenset[str]] = {
    "actor_type": ACTOR_TYPES,
    "annotation_stage": ANNOTATION_STAGES,
    "uncertainty_flag": UNCERTAINTY_FLAGS,
    "alternative_pathway_present": YES_NO_VALUES,
    "status": CORE_STATUS_VALUES,
}


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if value != value:
            return ""
    except Exception:
        pass
    return str(value).strip()


def coerce_segment_ids(value: Any) -> tuple[str, ...]:
    """Coerce pipe, semicolon, comma, or list values into segment IDs."""

    if value is None:
        return ()
    if isinstance(value, (list, tuple, set)):
        return tuple(clean_text(item) for item in value if clean_text(item))

    text = clean_text(value)
    if not text:
        return ()
    for separator in ("|", ";", ","):
        if separator in text:
            return tuple(part.strip() for part in text.split(separator) if part.strip())
    return (text,)


@dataclass(slots=True)
class TrimHAAAnnotation:
    """One submitted core annotation record for a human-AI audit stage."""

    annotation_id: str = ""
    case_id: str = ""
    parent_annotation_id: str = ""
    actor_id: str = ""
    actor_type: str = ""
    annotation_stage: str = ""
    primary_evidence_segment_ids: tuple[str, ...] = ()
    function_label: str = ""
    rationale_mechanism: str = ""
    uncertainty_flag: str = ""
    rationale_note: str = ""
    alternative_pathway_present: str = "no"
    alternative_mechanism: str = ""
    alternative_note: str = ""
    status: str = "draft"

    def __post_init__(self) -> None:
        for field_name in CORE_FIELDS:
            if field_name == "primary_evidence_segment_ids":
                self.primary_evidence_segment_ids = coerce_segment_ids(
                    self.primary_evidence_segment_ids
                )
            else:
                setattr(self, field_name, clean_text(getattr(self, field_name)))

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "TrimHAAAnnotation":
        values = {field_name: record.get(field_name, "") for field_name in CORE_FIELDS}
        return cls(**values)

    def to_record(self) -> dict[str, Any]:
        record = asdict(self)
        record["primary_evidence_segment_ids"] = list(self.primary_evidence_segment_ids)
        return record

    def to_csv_record(self) -> dict[str, str]:
        record: dict[str, str] = {}
        for field_name in CORE_FIELDS:
            value = getattr(self, field_name)
            if field_name == "primary_evidence_segment_ids":
                record[field_name] = "|".join(value)
            else:
                record[field_name] = clean_text(value)
        return record

    @property
    def is_independent(self) -> bool:
        return self.annotation_stage in {"human_pre", "ai_independent"} and not (
            self.parent_annotation_id
        )

    @property
    def has_alternative(self) -> bool:
        return self.alternative_pathway_present == "yes"


def records_to_annotations(records: list[Mapping[str, Any]]) -> list[TrimHAAAnnotation]:
    return [TrimHAAAnnotation.from_record(record) for record in records]

