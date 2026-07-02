"""Explicit AI exposure-event records for TRIM-HAA."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

from trim_haa.schema import clean_text

EXPOSURE_EVENT_FIELDS: tuple[str, ...] = (
    "exposure_event_id",
    "human_post_annotation_id",
    "human_pre_annotation_id",
    "ai_annotation_id",
    "model_run_id",
    "case_id",
    "exposure_sequence",
    "output_components_shown",
    "exposure_timestamp",
    "interface_condition",
    "notes",
)


@dataclass(slots=True)
class ExposureEvent:
    """One event where model output was shown to a human reviewer."""

    exposure_event_id: str = ""
    human_post_annotation_id: str = ""
    human_pre_annotation_id: str = ""
    ai_annotation_id: str = ""
    model_run_id: str = ""
    case_id: str = ""
    exposure_sequence: str = "1"
    output_components_shown: str = ""
    exposure_timestamp: str = ""
    interface_condition: str = "ai_review"
    notes: str = ""

    def __post_init__(self) -> None:
        for field_name in EXPOSURE_EVENT_FIELDS:
            setattr(self, field_name, clean_text(getattr(self, field_name)))

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "ExposureEvent":
        return cls(
            **{
                field_name: record.get(field_name, "")
                for field_name in EXPOSURE_EVENT_FIELDS
            }
        )

    def to_record(self) -> dict[str, str]:
        return asdict(self)


def exposure_index(
    events: Iterable[ExposureEvent | Mapping[str, Any]],
) -> dict[str, ExposureEvent]:
    index: dict[str, ExposureEvent] = {}
    for event in events:
        if not isinstance(event, ExposureEvent):
            event = ExposureEvent.from_record(event)
        index[event.exposure_event_id] = event
    return index


def exposures_by_human_post(
    events: Iterable[ExposureEvent | Mapping[str, Any]],
) -> dict[str, list[ExposureEvent]]:
    by_post: dict[str, list[ExposureEvent]] = {}
    for event in events:
        if not isinstance(event, ExposureEvent):
            event = ExposureEvent.from_record(event)
        by_post.setdefault(event.human_post_annotation_id, []).append(event)
    return by_post

