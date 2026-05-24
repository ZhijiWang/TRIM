import json
from pathlib import Path

import networkx as nx
import pandas as pd

from trim.graph import (
    build_case_graph,
    build_corpus_graph,
    export_graphml,
    export_json_graph,
    graph_summary,
)
from trim.io import annotations_to_dataframe, load_annotations


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _record(**overrides):
    values = {
        "case_id": "case-1",
        "text": "Demo text",
        "case_label": "Demo case",
        "source": "Demo source",
        "function_label": "demo_function",
        "evidence_anchor": "anchor evidence",
        "evidence_nodes": "first evidence; second evidence",
        "anchor_node": "demo_anchor",
        "friction_locus": "operation_function",
        "rationale_mechanism": "stabilizes",
        "epistemic_support": "textual_anchor",
        "discourse_level": "intradiegetic",
        "temporal_orientation": "immediate",
        "uncertainty_flag": "low",
        "rationale_note": "Human-coded graph rationale.",
    }
    values.update(overrides)
    return values


def test_build_case_graph_preserves_trim_path():
    graph = build_case_graph(_record())

    assert graph.number_of_nodes() == 6
    assert graph.nodes["case-1::case"]["node_type"] == "case"
    assert graph.nodes["case-1::evidence::1"]["label"] == "first evidence"
    assert graph.nodes["case-1::threshold_rationale"]["node_type"] == (
        "threshold_rationale"
    )
    assert graph.has_edge("case-1::case", "case-1::evidence::1")
    assert graph.has_edge("case-1::evidence::1", "case-1::anchor")
    assert graph.has_edge("case-1::anchor", "case-1::function")
    assert graph.edges["case-1::anchor", "case-1::function"]["edge_type"] == (
        "converts_to"
    )
    assert graph.edges["case-1::anchor", "case-1::function"]["friction_locus"] == (
        "operation_function"
    )


def test_build_corpus_graph_does_not_collapse_same_labels():
    frame = pd.DataFrame(
        [
            _record(case_id="case-1", function_label="shared_function"),
            _record(case_id="case-2", function_label="shared_function"),
        ]
    )

    graph = build_corpus_graph(frame)

    assert "case-1::function" in graph
    assert "case-2::function" in graph
    assert graph.nodes["case-1::function"]["label"] == "shared_function"
    assert graph.nodes["case-2::function"]["label"] == "shared_function"


def test_graph_summary_counts_demo_graph():
    annotations = load_annotations(PROJECT_ROOT / "data" / "demo_annotations.csv")
    frame = annotations_to_dataframe(annotations)
    graph = build_corpus_graph(frame)

    summary = graph_summary(graph)

    assert summary["node_count"] == 76
    assert summary["edge_count"] == 102
    assert summary["node_types"]["case"] == 10
    assert summary["node_types"]["evidence"] == 36
    assert summary["node_types"]["threshold_rationale"] == 10
    assert summary["friction_locus_counts"]["operation_function"] == 3
    assert summary["function_counts"]["immediate_stabilization"] == 2


def test_export_graphml_and_json_graph(tmp_path):
    graph = build_case_graph(_record())
    graphml_path = tmp_path / "case.graphml"
    json_path = tmp_path / "case.json"

    export_graphml(graph, graphml_path)
    export_json_graph(graph, json_path)

    loaded_graphml = nx.read_graphml(graphml_path)
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert "case-1::case" in loaded_graphml
    assert payload["directed"] is True
    assert any(node["id"] == "case-1::anchor" for node in payload["nodes"])
