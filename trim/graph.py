"""Graph utilities for TRIM annotations.

The graph preserves human-created annotation paths and keeps case-specific
evidence-to-function structures distinct.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

import networkx as nx
import pandas as pd
from networkx.readwrite import json_graph

from trim.schema import TrimAnnotation, coerce_string_list
from trim.signature import SIGNATURE_FIELDS


EDGE_ATTRIBUTES: tuple[str, ...] = (
    "friction_locus",
    "rationale_mechanism",
    "epistemic_support",
    "discourse_level",
    "temporal_orientation",
    "uncertainty_flag",
    "rationale_note",
)


def build_case_graph(record: TrimAnnotation | Mapping[str, Any] | pd.Series) -> nx.DiGraph:
    """Build a TRIM graph for one annotation record."""

    case_id = _record_value(record, "case_id") or "unknown_case"
    source = _record_value(record, "source")
    case_node_id = _node_id(case_id, "case")
    anchor_node_id = _node_id(case_id, "anchor")
    threshold_node_id = _node_id(case_id, "threshold_rationale")
    function_node_id = _node_id(case_id, "function")
    function_label = _record_value(record, "function_label")

    graph = nx.DiGraph()
    graph.add_node(
        case_node_id,
        case_id=case_id,
        node_type="case",
        label=_record_value(record, "case_label") or case_id,
        source=source,
        text=_record_value(record, "text"),
    )

    evidence_nodes = list(
        coerce_string_list(_raw_record_value(record, "evidence_nodes"))
    )
    if not evidence_nodes:
        raise ValueError(
            "evidence_nodes requires at least one non-empty evidence node."
        )
    for index, evidence_text in enumerate(evidence_nodes, start=1):
        evidence_node_id = _node_id(case_id, "evidence", str(index))
        graph.add_node(
            evidence_node_id,
            case_id=case_id,
            node_type="evidence",
            label=evidence_text,
            source=source,
            text=evidence_text,
        )
        graph.add_edge(
            case_node_id,
            evidence_node_id,
            case_id=case_id,
            edge_type="contains_evidence",
            label="contains_evidence",
        )

    evidence_anchor = _required_record_value(record, "evidence_anchor")
    anchor_label = _required_record_value(record, "anchor_node")
    graph.add_node(
        anchor_node_id,
        case_id=case_id,
        node_type="anchor",
        label=anchor_label,
        source=source,
        text=evidence_anchor,
    )

    for index in range(1, len(evidence_nodes) + 1):
        graph.add_edge(
            _node_id(case_id, "evidence", str(index)),
            anchor_node_id,
            case_id=case_id,
            edge_type="contributes_to_anchor",
            label="contributes_to_anchor",
        )

    threshold_attributes = _threshold_attributes(record)
    graph.add_node(
        threshold_node_id,
        case_id=case_id,
        node_type="threshold_rationale",
        label=_threshold_label(record),
        source=source,
        text=_record_value(record, "rationale_note"),
        **threshold_attributes,
    )
    graph.add_edge(
        anchor_node_id,
        threshold_node_id,
        case_id=case_id,
        edge_type="has_threshold_rationale",
        label="has_threshold_rationale",
    )
    graph.add_edge(
        threshold_node_id,
        function_node_id,
        case_id=case_id,
        edge_type="points_to_function",
        label="points_to_function",
    )

    graph.add_node(
        function_node_id,
        case_id=case_id,
        node_type="function",
        label=function_label,
        source=source,
        text=function_label,
    )
    graph.add_edge(
        anchor_node_id,
        function_node_id,
        case_id=case_id,
        edge_type="converts_to",
        label="converts_to",
        **threshold_attributes,
    )

    return graph


def build_corpus_graph(df: pd.DataFrame) -> nx.DiGraph:
    """Combine per-case graphs into a corpus graph without collapsing cases."""

    graph = nx.DiGraph()
    for record in df.to_dict(orient="records"):
        graph = nx.compose(graph, build_case_graph(record))
    return graph


def export_graphml(G: nx.DiGraph, path: str | Path) -> None:
    """Export a graph to GraphML."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(G, output_path)


def export_json_graph(G: nx.DiGraph, path: str | Path) -> None:
    """Export a graph as node-link JSON."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = json_graph.node_link_data(G)
    if "links" in data and "edges" not in data:
        data["edges"] = data.pop("links")
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def graph_summary(G: nx.DiGraph) -> dict[str, Any]:
    """Summarize graph size and key human-coded TRIM attributes."""

    node_type_counts = Counter(
        _clean_value(attributes.get("node_type"))
        for _, attributes in G.nodes(data=True)
        if _clean_value(attributes.get("node_type"))
    )
    friction_locus_counts = Counter(
        _clean_value(attributes.get("friction_locus"))
        for _, _, attributes in G.edges(data=True)
        if attributes.get("edge_type") == "converts_to"
        and _clean_value(attributes.get("friction_locus"))
    )
    rationale_mechanism_counts = Counter(
        _clean_value(attributes.get("rationale_mechanism"))
        for _, _, attributes in G.edges(data=True)
        if attributes.get("edge_type") == "converts_to"
        and _clean_value(attributes.get("rationale_mechanism"))
    )
    function_counts = Counter(
        _clean_value(attributes.get("label"))
        for _, attributes in G.nodes(data=True)
        if attributes.get("node_type") == "function"
        and _clean_value(attributes.get("label"))
    )

    return {
        "node_count": G.number_of_nodes(),
        "edge_count": G.number_of_edges(),
        "node_types": dict(sorted(node_type_counts.items())),
        "friction_locus_counts": dict(sorted(friction_locus_counts.items())),
        "rationale_mechanism_counts": dict(sorted(rationale_mechanism_counts.items())),
        "function_counts": dict(sorted(function_counts.items())),
    }


def _threshold_attributes(record: TrimAnnotation | Mapping[str, Any] | pd.Series) -> dict[str, str]:
    return {
        field_name: _record_value(record, field_name)
        for field_name in EDGE_ATTRIBUTES
    }


def _threshold_label(record: TrimAnnotation | Mapping[str, Any] | pd.Series) -> str:
    return " / ".join(_record_value(record, field_name) for field_name in SIGNATURE_FIELDS)


def _node_id(case_id: str, node_type: str, suffix: str | None = None) -> str:
    pieces = [case_id, node_type]
    if suffix is not None:
        pieces.append(suffix)
    return "::".join(_safe_node_piece(piece) for piece in pieces)


def _safe_node_piece(value: str) -> str:
    cleaned = _clean_value(value) or "blank"
    return cleaned.replace("::", "_")


def _record_value(record: TrimAnnotation | Mapping[str, Any] | pd.Series, field_name: str) -> str:
    return _clean_value(_raw_record_value(record, field_name))


def _required_record_value(
    record: TrimAnnotation | Mapping[str, Any] | pd.Series,
    field_name: str,
) -> str:
    value = _record_value(record, field_name)
    if not value:
        raise ValueError(f"{field_name} is required for graph conversion.")
    return value


def _raw_record_value(record: TrimAnnotation | Mapping[str, Any] | pd.Series, field_name: str) -> Any:
    if isinstance(record, TrimAnnotation):
        return getattr(record, field_name, "")
    if isinstance(record, pd.Series):
        return record.get(field_name, "")
    if isinstance(record, Mapping):
        return record.get(field_name, "")
    return getattr(record, field_name, "")


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()
