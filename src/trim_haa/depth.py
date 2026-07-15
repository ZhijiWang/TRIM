"""Optional interpretive-depth fields for TRIM-HAA."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from trim_haa.schema import clean_text

SIGNATURE_FIELDS: tuple[str, ...] = (
    "friction_locus",
    "rationale_mechanism",
    "epistemic_support",
    "discourse_level",
    "temporal_orientation",
    "uncertainty_flag",
)

DEPTH_FIELDS: tuple[str, ...] = (
    "annotation_id",
    "context_segment_ids",
    "evidence_anchor",
    "anchor_node",
    "friction_locus",
    "epistemic_support",
    "discourse_level",
    "temporal_orientation",
    "full_alternative_signature",
    "question_log_reference",
)


@dataclass(slots=True)
class TrimHAADepth:
    """Optional depth module linked to a core record by annotation_id."""

    annotation_id: str = ""
    context_segment_ids: tuple[str, ...] = ()
    evidence_anchor: str = ""
    anchor_node: str = ""
    friction_locus: str = ""
    epistemic_support: str = ""
    discourse_level: str = ""
    temporal_orientation: str = ""
    full_alternative_signature: str = ""
    question_log_reference: str = ""

    def __post_init__(self) -> None:
        for field_name in DEPTH_FIELDS:
            if field_name == "context_segment_ids":
                self.context_segment_ids = coerce_string_list(self.context_segment_ids)
            else:
                setattr(self, field_name, clean_text(getattr(self, field_name)))

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "TrimHAADepth":
        values = {field_name: record.get(field_name, "") for field_name in DEPTH_FIELDS}
        return cls(**values)

    def to_record(self) -> dict[str, Any]:
        record = asdict(self)
        record["context_segment_ids"] = list(self.context_segment_ids)
        return record

    def to_csv_record(self) -> dict[str, str]:
        record = {field_name: clean_text(getattr(self, field_name)) for field_name in DEPTH_FIELDS}
        record["context_segment_ids"] = "|".join(self.context_segment_ids)
        return record


LEGACY_COMPATIBLE_DEPTH_FIELDS: tuple[str, ...] = (
    "friction_locus",
    "epistemic_support",
    "discourse_level",
    "temporal_orientation",
    "rationale_mechanism",
    "uncertainty_flag",
)


def coerce_string_list(value: Any) -> tuple[str, ...]:
    """Coerce list-like or delimited text values into a tuple of strings."""

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
