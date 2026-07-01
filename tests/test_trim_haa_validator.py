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
        self_reported_revision_reason="mixed_or_unclear",
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


def test_stage_condition_matrix_rejects_human_post_without_exposure():
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
        function_label="label_a",
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
        ai_output_exposed="none",
        exposure_order="none",
        interface_condition="independent",
        changed_label="no",
        changed_primary_evidence="no",
        changed_rationale_mechanism="no",
        changed_uncertainty="no",
        changed_alternative="no",
        self_reported_revision_reason="not_applicable",
        lock_status="locked",
    )

    report = validate_dataset([pre, post], [prov])
    fields = {issue.field for issue in report.errors}

    assert "ai_output_exposed" in fields
    assert "exposure_order" in fields
    assert "interface_condition" in fields


def test_control_record_with_ai_exposure_is_error():
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
    control = TrimHAAAnnotation(
        annotation_id="CONTROL",
        case_id="C1",
        parent_annotation_id="PRE",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_second_pass_control",
        primary_evidence_segment_ids="S1",
        function_label="label_a",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="Control rationale.",
        alternative_pathway_present="no",
        status="locked",
    )
    prov = AssistanceProvenance(
        annotation_id="CONTROL",
        parent_annotation_id="PRE",
        case_id="C1",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_second_pass_control",
        pre_ai_annotation_locked="yes",
        ai_output_exposed="full_core_record",
        exposure_order="control_second_pass",
        interface_condition="control_review",
        changed_label="no",
        changed_primary_evidence="no",
        changed_rationale_mechanism="no",
        changed_uncertainty="no",
        changed_alternative="no",
        self_reported_revision_reason="changed_after_rereading_not_ai",
        lock_status="locked",
    )

    report = validate_dataset([pre, control], [prov])

    assert any(issue.field == "ai_output_exposed" for issue in report.errors)


def test_other_revision_reason_requires_note():
    prov = AssistanceProvenance(
        annotation_id="POST",
        case_id="C1",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_post_ai",
        pre_ai_annotation_locked="yes",
        ai_output_exposed="full_core_record",
        exposure_order="human_first",
        interface_condition="ai_review",
        changed_label="no",
        changed_primary_evidence="no",
        changed_rationale_mechanism="no",
        changed_uncertainty="no",
        changed_alternative="no",
        self_reported_revision_reason="other",
        lock_status="locked",
    )

    report = validate_dataset([], [prov])

    assert any(issue.field == "self_reported_revision_note" for issue in report.errors)


def test_human_pre_with_exposure_metadata_is_error():
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
    prov = AssistanceProvenance(
        annotation_id="PRE",
        case_id="C1",
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_pre",
        pre_ai_annotation_locked="not_applicable",
        ai_output_exposed="full_core_record",
        exposure_order="none",
        interface_condition="independent",
        exposed_ai_annotation_id="AI",
        exposed_model_run_id="RUN",
        changed_label="not_applicable",
        changed_primary_evidence="not_applicable",
        changed_rationale_mechanism="not_applicable",
        changed_uncertainty="not_applicable",
        changed_alternative="not_applicable",
        self_reported_revision_reason="not_applicable",
        lock_status="locked",
    )

    report = validate_dataset([pre], [prov])
    fields = {issue.field for issue in report.errors}

    assert "ai_output_exposed" in fields
    assert "exposed_ai_annotation_id" in fields


def test_ai_independent_with_exposure_metadata_is_error():
    ai = TrimHAAAnnotation(
        annotation_id="AI",
        case_id="C1",
        actor_id="AI_MODEL",
        actor_type="model",
        annotation_stage="ai_independent",
        primary_evidence_segment_ids="S1",
        function_label="label_a",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note="AI rationale.",
        alternative_pathway_present="no",
        status="locked",
    )
    prov = AssistanceProvenance(
        annotation_id="AI",
        case_id="C1",
        actor_id="AI_MODEL",
        actor_type="model",
        annotation_stage="ai_independent",
        pre_ai_annotation_locked="not_applicable",
        ai_output_exposed="label_only",
        exposure_order="none",
        interface_condition="independent",
        model_provider="OpenAI",
        model_name="gpt-test",
        model_version_or_date="test-version",
        prompt_template_id="PROMPT",
        prompt_hash="a" * 64,
        model_run_id="RUN",
        retry_count="0",
        regenerated_output="no",
        exposed_ai_annotation_id="AI",
        exposed_model_run_id="RUN",
        changed_label="not_applicable",
        changed_primary_evidence="not_applicable",
        changed_rationale_mechanism="not_applicable",
        changed_uncertainty="not_applicable",
        changed_alternative="not_applicable",
        self_reported_revision_reason="not_applicable",
        lock_status="locked",
    )

    report = validate_dataset([ai], [prov])
    fields = {issue.field for issue in report.errors}

    assert "ai_output_exposed" in fields
    assert "exposed_ai_annotation_id" in fields
