"""CSV, JSON, and graph IO helpers for TRIM annotations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import networkx as nx
import pandas as pd

from trim.schema import ANNOTATION_FIELDS, TrimAnnotation


def load_annotations(path: str | Path) -> list[TrimAnnotation]:
    """Load annotations from CSV or JSON based on file extension."""

    annotation_path = Path(path)
    suffix = annotation_path.suffix.lower()
    if suffix == ".csv":
        return load_csv(annotation_path)
    if suffix == ".json":
        return load_json(annotation_path)
    raise ValueError(f"Unsupported annotation file type: {annotation_path.suffix}")


def load_csv(path: str | Path) -> list[TrimAnnotation]:
    """Load TRIM annotations from a CSV file."""

    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    return [TrimAnnotation.from_record(record) for record in frame.to_dict(orient="records")]


def load_json(path: str | Path) -> list[TrimAnnotation]:
    """Load TRIM annotations from a JSON list or an ``annotations`` object."""

    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, dict):
        records = payload.get("annotations")
    else:
        records = payload

    if not isinstance(records, list):
        raise ValueError("JSON annotations must be a list or contain an 'annotations' list.")

    return [TrimAnnotation.from_record(record) for record in records]


def save_annotations(path: str | Path, annotations: Iterable[TrimAnnotation]) -> None:
    """Save annotations to CSV or JSON based on file extension."""

    annotation_path = Path(path)
    annotation_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = annotation_path.suffix.lower()
    if suffix == ".csv":
        save_csv(annotation_path, annotations)
        return
    if suffix == ".json":
        save_json(annotation_path, annotations)
        return
    raise ValueError(f"Unsupported annotation file type: {annotation_path.suffix}")


def save_csv(path: str | Path, annotations: Iterable[TrimAnnotation]) -> None:
    """Save annotations as CSV with a stable field order."""

    frame = annotations_to_dataframe(annotations)
    frame.to_csv(path, index=False)


def save_json(path: str | Path, annotations: Iterable[TrimAnnotation]) -> None:
    """Save annotations as a JSON list."""

    records = [_coerce_annotation(annotation).to_record() for annotation in annotations]
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def annotations_to_dataframe(annotations: Iterable[TrimAnnotation]) -> pd.DataFrame:
    """Convert annotations to a pandas DataFrame suitable for tabular reports."""

    records = [_coerce_annotation(annotation).to_csv_record() for annotation in annotations]
    return pd.DataFrame(records, columns=ANNOTATION_FIELDS)


def build_annotation_graph(annotations: Iterable[TrimAnnotation]) -> nx.MultiDiGraph:
    """Build a graph using the TRIM evidence-anchor-edge-function structure."""

    graph = nx.MultiDiGraph()
    for annotation in annotations:
        annotation = _coerce_annotation(annotation)
        components = annotation.to_core_components()
        evidence_nodes = components["evidence_nodes"]
        anchor_node = components["anchor_node"]
        rationale_edge = components["threshold_rationale_edge"]
        function_node = components["function_node"]

        graph.add_node(
            anchor_node.node_id,
            kind="anchor",
            text=anchor_node.text,
            evidence_anchor=annotation.evidence_anchor,
            case_id=annotation.case_id,
        )
        graph.add_node(
            function_node.node_id,
            kind="function",
            label=function_node.label,
            cue_family=function_node.cue_family,
            broad_function_family=function_node.broad_function_family,
            case_id=annotation.case_id,
        )

        for evidence_node in evidence_nodes:
            graph.add_node(
                evidence_node.node_id,
                kind="evidence",
                text=evidence_node.text,
                case_id=annotation.case_id,
            )
            graph.add_edge(
                evidence_node.node_id,
                anchor_node.node_id,
                kind="evidence_to_anchor",
                case_id=annotation.case_id,
            )

        graph.add_edge(
            rationale_edge.source_anchor_id,
            rationale_edge.target_function_id,
            key=rationale_edge.edge_id,
            kind="threshold_rationale",
            friction_locus=rationale_edge.friction_locus,
            rationale_mechanism=rationale_edge.rationale_mechanism,
            epistemic_support=rationale_edge.epistemic_support,
            discourse_level=rationale_edge.discourse_level,
            temporal_orientation=rationale_edge.temporal_orientation,
            uncertainty_flag=rationale_edge.uncertainty_flag,
            rationale_note=rationale_edge.rationale_note,
            case_id=annotation.case_id,
        )

    return graph


def _coerce_annotation(annotation: TrimAnnotation) -> TrimAnnotation:
    if isinstance(annotation, TrimAnnotation):
        return annotation
    return TrimAnnotation.from_record(annotation)
