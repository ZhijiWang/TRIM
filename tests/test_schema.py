import pytest

from trim.schema import TrimAnnotation


def test_annotation_coerces_evidence_nodes_from_csv_string():
    annotation = TrimAnnotation(
        case_id="case-1",
        evidence_nodes="first cue|second cue",
    )

    assert annotation.evidence_nodes == ("first cue", "second cue")


def test_annotation_core_components_follow_trim_model():
    annotation = TrimAnnotation(
        case_id="case-1",
        function_label="boundary legitimation",
        cue_family="oath formula",
        broad_function_family="normative ordering",
        evidence_anchor="The assembly accepts the stated boundary.",
        evidence_nodes=("oath was spoken", "assembly accepted"),
        anchor_node="assembly accepted the boundary",
        friction_locus="boundary_setting",
        rationale_mechanism="authorizes",
        epistemic_support="textual_anchor",
        discourse_level="intradiegetic",
        temporal_orientation="retrospective",
        uncertainty_flag="low",
        rationale_note="Human-coded rationale.",
    )

    components = annotation.to_core_components()

    assert len(components["evidence_nodes"]) == 2
    assert components["anchor_node"].node_id == "case-1:anchor"
    assert components["anchor_node"].text == "assembly accepted the boundary"
    assert components["anchor_node"].metadata["evidence_anchor"] == (
        "The assembly accepts the stated boundary."
    )
    assert components["threshold_rationale_edge"].source_anchor_id == "case-1:anchor"
    assert components["function_node"].label == "boundary legitimation"


def test_core_components_reject_anchor_only_annotation():
    annotation = TrimAnnotation(
        case_id="case-1",
        evidence_anchor="Source-facing passage",
        anchor_node="normalized_anchor",
    )

    with pytest.raises(
        ValueError,
        match="evidence_nodes or primary_evidence_segment_ids requires",
    ):
        annotation.to_core_components()


def test_core_components_accept_primary_segment_ids_for_v0_2_1():
    annotation = TrimAnnotation(
        case_id="case-1",
        evidence_anchor="Segment S2",
        primary_evidence_segment_ids="case-1_S2|case-1_S3",
        context_segment_ids="case-1_S1",
        anchor_node="visible confirmation",
        function_label="immediate_stabilization",
        friction_locus="operation_function",
        rationale_mechanism="stabilizes",
        epistemic_support="textual_anchor",
        discourse_level="intradiegetic",
        temporal_orientation="immediate",
        uncertainty_flag="low",
    )

    components = annotation.to_core_components()

    assert [node.text for node in components["evidence_nodes"]] == [
        "case-1_S2",
        "case-1_S3",
    ]
    assert components["evidence_nodes"][0].role == "primary_evidence_segment_id"
    assert components["anchor_node"].metadata["context_segment_ids"] == (
        "case-1_S1",
    )


@pytest.mark.parametrize(
    ("field_name", "message"),
    [
        ("evidence_anchor", "evidence_anchor is required for graph conversion"),
        ("anchor_node", "anchor_node is required for graph conversion"),
    ],
)
def test_core_components_require_both_anchor_fields(field_name, message):
    values = {
        "case_id": "case-1",
        "evidence_anchor": "Source-facing passage",
        "evidence_nodes": ("evidence",),
        "anchor_node": "normalized_anchor",
    }
    values[field_name] = ""

    with pytest.raises(ValueError, match=message):
        TrimAnnotation(**values).to_core_components()
