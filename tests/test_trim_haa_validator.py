from trim_haa.provenance import AssistanceProvenance
from trim_haa.schema import TrimHAAAnnotation
from trim_haa.validator import validate_dataset


def test_changed_flag_consistency_warning():
    pre = TrimHAAAnnotation(
        annotation_id="PRE",
        case_id="C1",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_pre",
        primary_evidence_segment_ids="S1",
        function_label="label_a",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="Pre rationale.",
        alternative_pathway_present="no",
        status="locked",
    )
    post = TrimHAAAnnotation(
        annotation_id="POST",
        case_id="C1",
        parent_annotation_id="PRE",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_post_ai",
        primary_evidence_segment_ids="S1",
        function_label="label_b",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="Post rationale.",
        alternative_pathway_present="no",
        status="locked",
    )
    prov = AssistanceProvenance(
        annotation_id="POST",
        parent_annotation_id="PRE",
        case_id="C1",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_post_ai",
        pre_ai_annotation_locked="yes",
        ai_output_exposed="full_core_record",
        exposure_order="human_first",
        interface_condition="ai_review",
        changed_label="no",
        changed_primary_evidence="not_applicable",
        changed_rationale_mechanism="not_applicable",
        changed_uncertainty="not_applicable",
        changed_alternative="not_applicable",
        adoption_type="unclear",
        lock_status="locked",
    )

    report = validate_dataset([pre, post], [prov])

    assert any(issue.field == "changed_label" for issue in report.warnings)


def test_high_copied_phrase_overlap_warning():
    pre = TrimHAAAnnotation(
        annotation_id="PRE",
        case_id="C1",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_pre",
        primary_evidence_segment_ids="S1",
        function_label="label_a",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="Pre rationale is distinct.",
        alternative_pathway_present="no",
        status="locked",
    )
    ai = TrimHAAAnnotation(
        annotation_id="AI",
        case_id="C1",
        actor_id="AI",
        actor_type="model",
        annotation_stage="ai_independent",
        primary_evidence_segment_ids="S1",
        function_label="label_a",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="This exact copied phrase appears inside the rationale.",
        alternative_pathway_present="no",
        status="locked",
    )
    post = TrimHAAAnnotation(
        annotation_id="POST",
        case_id="C1",
        parent_annotation_id="PRE",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_post_ai",
        primary_evidence_segment_ids="S1",
        function_label="label_a",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="This exact copied phrase appears inside the rationale.",
        alternative_pathway_present="no",
        status="locked",
    )

    report = validate_dataset([pre, ai, post])

    assert any(issue.field == "rationale_note" for issue in report.warnings)

