"""Schema objects for TRIM annotations.

The schema is intentionally descriptive rather than predictive: it records
human-created annotation values and provides a core graph-shaped representation.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


ANNOTATION_FIELDS: tuple[str, ...] = (
    "case_id",
    "text",
    "case_label",
    "source",
    "language",
    "case_type",
    "language_access_mode",
    "case_scope",
    "shared_context_ids",
    "cross_case_context_permitted",
    "required_context_segments",
    "function_label",
    "cue_family",
    "broad_function_family",
    "evidence_anchor",
    "evidence_nodes",
    "primary_evidence_segment_ids",
    "context_segment_ids",
    "evidence_highlight",
    "anchor_node",
    "friction_locus",
    "rationale_mechanism",
    "epistemic_support",
    "discourse_level",
    "temporal_orientation",
    "uncertainty_flag",
    "rationale_note",
    "alternative_signature",
    "coder_id",
    "status",
)

LIST_FIELDS: frozenset[str] = frozenset(
    {
        "evidence_nodes",
        "primary_evidence_segment_ids",
        "context_segment_ids",
        "shared_context_ids",
        "required_context_segments",
    }
)


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    try:
        return bool(value != value)
    except Exception:
        return False


def _coerce_text(value: Any) -> str:
    if _is_missing(value):
        return ""
    return str(value).strip()


def _coerce_optional_text(value: Any) -> str | None:
    text = _coerce_text(value)
    return text or None


def coerce_string_list(value: Any) -> tuple[str, ...]:
    """Coerce CSV/JSON representations into a tuple of non-empty strings."""

    if _is_missing(value):
        return ()

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return ()

        if text.startswith("["):
            try:
                decoded = json.loads(text)
            except json.JSONDecodeError:
                decoded = None
            if isinstance(decoded, list):
                return tuple(_coerce_text(item) for item in decoded if _coerce_text(item))

        separator = "|" if "|" in text else ";"
        return tuple(part.strip() for part in text.split(separator) if part.strip())

    if isinstance(value, (list, tuple, set)):
        return tuple(_coerce_text(item) for item in value if _coerce_text(item))

    return (_coerce_text(value),) if _coerce_text(value) else ()


@dataclass(slots=True)
class EvidenceNode:
    """A human-selected text fragment or cue that supports an anchor."""

    node_id: str
    text: str
    role: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AnchorNode:
    """The interpretive anchor that evidence nodes gather around."""

    node_id: str
    text: str
    evidence_node_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.evidence_node_ids = coerce_string_list(self.evidence_node_ids)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ThresholdRationaleEdge:
    """The threshold-rationale relation from an anchor to a function."""

    edge_id: str
    source_anchor_id: str
    target_function_id: str
    friction_locus: str
    rationale_mechanism: str
    epistemic_support: str
    discourse_level: str
    temporal_orientation: str
    uncertainty_flag: str
    rationale_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class FunctionNode:
    """The human-coded function reached through a threshold-rationale edge."""

    node_id: str
    label: str
    cue_family: str = ""
    broad_function_family: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class TrimAnnotation:
    """A single flat TRIM annotation record.

    The flat fields are useful for CSV/JSON exchange. Use ``to_core_components``
    to view the same annotation as evidence nodes, anchor node, edge, and
    function node. v0.2.1 metadata fields record language access, primary versus
    context segment selection, and shared-context permissions without changing
    the v0.2.0 evidence-node compatibility path.
    """

    case_id: str = ""
    text: str = ""
    case_label: str = ""
    source: str = ""
    language: str = ""
    case_type: str = ""
    language_access_mode: str = ""
    case_scope: str = ""
    shared_context_ids: tuple[str, ...] = ()
    cross_case_context_permitted: str = ""
    required_context_segments: tuple[str, ...] = ()
    function_label: str = ""
    cue_family: str = ""
    broad_function_family: str = ""
    evidence_anchor: str = ""
    evidence_nodes: tuple[str, ...] = ()
    primary_evidence_segment_ids: tuple[str, ...] = ()
    context_segment_ids: tuple[str, ...] = ()
    evidence_highlight: str = ""
    anchor_node: str = ""
    friction_locus: str = ""
    rationale_mechanism: str = ""
    epistemic_support: str = ""
    discourse_level: str = ""
    temporal_orientation: str = ""
    uncertainty_flag: str = ""
    rationale_note: str = ""
    alternative_signature: str | None = None
    coder_id: str = ""
    status: str = ""

    def __post_init__(self) -> None:
        for field_name in ANNOTATION_FIELDS:
            if field_name in LIST_FIELDS:
                setattr(
                    self,
                    field_name,
                    coerce_string_list(getattr(self, field_name)),
                )
                continue
            elif field_name == "alternative_signature":
                self.alternative_signature = _coerce_optional_text(
                    self.alternative_signature
                )
            else:
                setattr(self, field_name, _coerce_text(getattr(self, field_name)))

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "TrimAnnotation":
        """Create an annotation from a mapping, ignoring unknown keys."""

        values = {field_name: record.get(field_name, "") for field_name in ANNOTATION_FIELDS}
        return cls(**values)

    def to_record(self) -> dict[str, Any]:
        """Return a JSON-friendly flat record."""

        record = {field_name: getattr(self, field_name) for field_name in ANNOTATION_FIELDS}
        for field_name in LIST_FIELDS:
            record[field_name] = list(getattr(self, field_name))
        return record

    def to_csv_record(self) -> dict[str, str]:
        """Return a CSV-friendly flat record."""

        record: dict[str, str] = {}
        for field_name in ANNOTATION_FIELDS:
            value = getattr(self, field_name)
            if field_name in LIST_FIELDS:
                record[field_name] = "|".join(getattr(self, field_name))
            elif value is None:
                record[field_name] = ""
            else:
                record[field_name] = str(value)
        return record

    def to_core_components(self) -> dict[str, Any]:
        """Represent the flat annotation as the TRIM core graph components."""

        evidence_values = self.evidence_nodes or self.primary_evidence_segment_ids
        if not evidence_values:
            raise ValueError(
                "evidence_nodes or primary_evidence_segment_ids requires at least "
                "one non-empty evidence node."
            )
        if not self.evidence_anchor:
            raise ValueError("evidence_anchor is required for graph conversion.")
        if not self.anchor_node:
            raise ValueError("anchor_node is required for graph conversion.")

        case_prefix = self.case_id or "unidentified_case"
        evidence = tuple(
            EvidenceNode(
                node_id=f"{case_prefix}:evidence:{index}",
                text=node_text,
                role=(
                    "evidence"
                    if self.evidence_nodes
                    else "primary_evidence_segment_id"
                ),
            )
            for index, node_text in enumerate(evidence_values, start=1)
        )
        anchor = AnchorNode(
            node_id=f"{case_prefix}:anchor",
            text=self.anchor_node,
            evidence_node_ids=tuple(node.node_id for node in evidence),
            metadata={
                "evidence_anchor": self.evidence_anchor,
                "primary_evidence_segment_ids": self.primary_evidence_segment_ids,
                "context_segment_ids": self.context_segment_ids,
                "evidence_highlight": self.evidence_highlight,
                "case_scope": self.case_scope,
                "shared_context_ids": self.shared_context_ids,
                "cross_case_context_permitted": self.cross_case_context_permitted,
                "required_context_segments": self.required_context_segments,
                "language_access_mode": self.language_access_mode,
            },
        )
        function = FunctionNode(
            node_id=f"{case_prefix}:function",
            label=self.function_label,
            cue_family=self.cue_family,
            broad_function_family=self.broad_function_family,
        )
        edge = ThresholdRationaleEdge(
            edge_id=f"{case_prefix}:threshold_rationale",
            source_anchor_id=anchor.node_id,
            target_function_id=function.node_id,
            friction_locus=self.friction_locus,
            rationale_mechanism=self.rationale_mechanism,
            epistemic_support=self.epistemic_support,
            discourse_level=self.discourse_level,
            temporal_orientation=self.temporal_orientation,
            uncertainty_flag=self.uncertainty_flag,
            rationale_note=self.rationale_note,
        )
        return {
            "evidence_nodes": evidence,
            "anchor_node": anchor,
            "threshold_rationale_edge": edge,
            "function_node": function,
        }
