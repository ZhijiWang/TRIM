import pandas as pd

from trim.signature import parse_signature
from trim.validator import (
    format_signature,
    validate_dataframe,
    validate_record,
    validate_retest_manifest,
    validate_shared_context_registry,
    validate_signature,
    validation_report,
)


def _valid_record(**overrides):
    values = {
        "case_id": "case-1",
        "case_label": "demo case",
        "source": "demo",
        "function_label": "immediate_stabilization",
        "evidence_anchor": "demo anchor",
        "evidence_nodes": "first evidence|second evidence",
        "anchor_node": "demo anchor node",
        "friction_locus": "cue_function",
        "rationale_mechanism": "supports",
        "epistemic_support": "textual_anchor",
        "discourse_level": "intradiegetic",
        "temporal_orientation": "immediate",
        "uncertainty_flag": "low",
        "rationale_note": "Human coder identifies the dominant threshold here.",
        "alternative_signature": "",
        "coder_id": "coder-a",
    }
    values.update(overrides)
    return values


def _errors(issues):
    return [issue for issue in issues if issue.severity == "error"]


def _shared_manifest():
    return [
        {
            "case_id": "case-a",
            "case_scope": "supplied_related_cases",
            "language_access_mode": "direct_original_language_access",
            "shared_context_ids": "ctx-1",
            "cross_case_context_permitted": "yes",
            "required_context_segments": "case-b_S1",
            "segment_ids": "case-a_S1|case-a_S2",
        },
        {
            "case_id": "case-b",
            "case_scope": "local_passage",
            "language_access_mode": "direct_original_language_access",
            "shared_context_ids": "",
            "cross_case_context_permitted": "no",
            "required_context_segments": "",
            "segment_ids": "case-b_S1|case-b_S2",
        },
        {
            "case_id": "case-c",
            "case_scope": "local_passage",
            "language_access_mode": "direct_original_language_access",
            "shared_context_ids": "",
            "cross_case_context_permitted": "no",
            "required_context_segments": "",
            "segment_ids": "case-c_S1",
        },
    ]


def _shared_registry():
    return [
        {
            "shared_context_id": "ctx-1",
            "description": "Neutral context group",
            "member_case_ids": "case-a|case-b",
            "permitted_segment_ids": "case-a_S1|case-a_S2|case-b_S1|case-b_S2",
        }
    ]


def test_valid_single_mechanism():
    issues = validate_record(_valid_record(rationale_mechanism="supports"))

    assert _errors(issues) == []


def test_valid_compound_mechanism():
    issues = validate_record(_valid_record(rationale_mechanism="supports+extends"))

    assert _errors(issues) == []


def test_invalid_mechanism():
    issues = validate_record(_valid_record(rationale_mechanism="automatic_guess"))

    assert any(issue.field == "rationale_mechanism" for issue in _errors(issues))


def test_function_label_closed_list_includes_no_fit():
    assert _errors(validate_record(_valid_record(function_label="no_fit"))) == []

    issues = validate_record(_valid_record(function_label="local_guess"))

    assert any(issue.field == "function_label" for issue in _errors(issues))


def test_too_many_compound_mechanisms():
    issues = validate_record(
        _valid_record(rationale_mechanism="supports+extends+narrows")
    )

    assert any("no more than 2" in issue.message for issue in _errors(issues))


def test_duplicate_compound_mechanism():
    issues = validate_record(_valid_record(rationale_mechanism="extends+extends"))

    assert any("duplicate compound value" in issue.message for issue in _errors(issues))


def test_signature_record_and_dataframe_validation_use_same_compound_rules():
    signature = (
        "cue_function / extends+extends / textual_anchor / intradiegetic / "
        "immediate / low"
    )
    record = _valid_record(rationale_mechanism="extends+extends")

    standalone_errors = _errors(validate_signature(signature))
    direct_errors = parse_signature(signature).validate()
    record_errors = _errors(validate_record(record))
    dataframe_errors = _errors(validate_dataframe(pd.DataFrame([record])))

    expected_message = (
        "rationale_mechanism contains duplicate compound value 'extends'."
    )
    assert direct_errors == [expected_message]
    assert [issue.message for issue in standalone_errors] == [expected_message]
    assert [
        issue.message
        for issue in record_errors
        if issue.field == "rationale_mechanism"
    ] == [expected_message]
    assert [
        issue.message
        for issue in dataframe_errors
        if issue.field == "rationale_mechanism"
    ] == [expected_message]


def test_invalid_friction_locus():
    issues = validate_record(_valid_record(friction_locus="automatic_guess"))

    assert any(issue.field == "friction_locus" for issue in _errors(issues))


def test_missing_rationale_note():
    issues = validate_record(_valid_record(rationale_note=""))

    assert any(
        issue.field == "rationale_note" and issue.severity == "error"
        for issue in issues
    )
    assert not any(
        issue.field == "rationale_note" and issue.severity == "warning"
        for issue in issues
    )


def test_short_rationale_note_warns_without_quality_claim():
    issues = validate_record(_valid_record(rationale_note="Too short."))

    assert any(
        issue.message
        == (
            "rationale_note is too short to support review; minimum recommended "
            "length is 30 characters."
        )
        and issue.severity == "warning"
        for issue in issues
    )


def test_multilingual_contested_rationale_does_not_require_english_keywords():
    rationale = (
        "此处记录第二种阈值路径，因为时间层次与凭据关系都能解释证据到功能的转换。"
        "编码者保留两种结构，以便后续审议时比较它们的解释充分性与文本位置。"
    )
    issues = validate_record(
        _valid_record(
            rationale_note=rationale,
            alternative_signature=(
                "temporal_layering / extends / textual_anchor / "
                "commentarial_discourse / retrospective / medium"
            ),
        )
    )

    assert len(rationale) >= 60
    assert _errors(issues) == []


def test_too_short_contested_rationale_fails():
    rationale = "说明第二路径的文本依据与转换理由。" * 3
    issues = validate_record(
        _valid_record(
            rationale_note=rationale,
            alternative_signature=(
                "temporal_layering / extends / textual_anchor / "
                "commentarial_discourse / retrospective / medium"
            ),
        )
    )

    assert 30 <= len(rationale) < 60
    assert any(
        issue.field == "rationale_note"
        and issue.message
        == (
            "alternative_signature requires rationale_note documentation of "
            "at least 60 characters."
        )
        for issue in _errors(issues)
    )


def test_malformed_alternative_signature_fails():
    issues = validate_record(
        _valid_record(
            rationale_note=(
                "This rationale is intentionally long enough to document the "
                "second pathway without depending on any required keywords."
            ),
            alternative_signature=(
                "temporal_layering / extends / textual_anchor / retrospective"
            ),
        )
    )

    assert any(
        issue.field == "alternative_signature"
        and "require 6 fields" in issue.message
        for issue in _errors(issues)
    )


def test_evidence_nodes_require_at_least_one_nonempty_node():
    issues = validate_record(_valid_record(evidence_nodes=" | "))

    assert any(
        issue.field == "evidence_nodes"
        and issue.message.startswith(
            "evidence_nodes or primary_evidence_segment_ids requires"
        )
        for issue in _errors(issues)
    )


def test_primary_evidence_segments_are_limited_and_checked():
    issues = validate_record(
        _valid_record(
            status="retest_v0_2_1",
            language_access_mode="direct_original_language_access",
            case_scope="local_passage",
            cross_case_context_permitted="no",
            evidence_nodes="",
            primary_evidence_segment_ids="S1|S2|S3|S4",
        )
    )

    assert any(
        issue.field == "primary_evidence_segment_ids"
        and "one to three" in issue.message
        for issue in _errors(issues)
    )


def test_primary_and_context_segments_cannot_duplicate_or_overlap():
    issues = validate_record(
        _valid_record(
            status="retest_v0_2_1",
            language_access_mode="direct_original_language_access",
            case_scope="local_passage",
            cross_case_context_permitted="no",
            evidence_nodes="",
            primary_evidence_segment_ids="S1|S1",
            context_segment_ids="S1|S2|S2",
        )
    )

    assert any("duplicate segment IDs" in issue.message for issue in _errors(issues))
    assert any("both primary evidence and context" in issue.message for issue in _errors(issues))


def test_unknown_segment_ids_fail_when_known_segments_are_supplied():
    issues = validate_record(
        _valid_record(
            status="retest_v0_2_1",
            language_access_mode="direct_original_language_access",
            case_scope="local_passage",
            cross_case_context_permitted="no",
            evidence_nodes="",
            primary_evidence_segment_ids="S1|S9",
        ),
        known_segment_ids={"case-1": ["S1", "S2"]},
    )

    assert any("Unknown segment IDs" in issue.message for issue in _errors(issues))


def test_shared_context_required_segments_require_permission():
    issues = validate_record(
        _valid_record(
            status="retest_v0_2_1",
            language_access_mode="published_translation",
            case_scope="shared_narrative_field",
            shared_context_ids="cluster-1",
            cross_case_context_permitted="no",
            required_context_segments="other-case_S1",
            evidence_nodes="",
            primary_evidence_segment_ids="S1",
        )
    )

    assert any(
        issue.field == "cross_case_context_permitted"
        and "requires cross_case_context_permitted=yes" in issue.message
        for issue in _errors(issues)
    )


def test_multi_passage_single_case_rejects_cross_case_metadata():
    issues = validate_record(
        _valid_record(
            status="retest_v0_2_1",
            language_access_mode="direct_original_language_access",
            case_scope="multi_passage_single_case",
            shared_context_ids="ctx-1",
            cross_case_context_permitted="yes",
            required_context_segments="case-b_S1",
            evidence_nodes="",
            primary_evidence_segment_ids="S1",
        )
    )

    assert any(issue.field == "shared_context_ids" for issue in _errors(issues))
    assert any(
        issue.field == "cross_case_context_permitted"
        and "cross_case_context_permitted=no" in issue.message
        for issue in _errors(issues)
    )
    assert any(issue.field == "required_context_segments" for issue in _errors(issues))


def test_unknown_shared_context_id_fails_manifest_validation():
    manifest = _shared_manifest()
    manifest[0]["shared_context_ids"] = "missing-ctx"

    issues = validate_retest_manifest(manifest, _shared_registry())

    assert any("Unknown shared-context ID" in issue.message for issue in _errors(issues))


def test_unknown_shared_context_member_case_fails():
    registry = _shared_registry()
    registry[0]["member_case_ids"] = "case-a|missing-case"

    issues = validate_shared_context_registry(_shared_manifest(), registry)

    assert any("Unknown member case ID" in issue.message for issue in _errors(issues))


def test_unknown_shared_context_permitted_segment_fails():
    registry = _shared_registry()
    registry[0]["permitted_segment_ids"] = "case-a_S1|missing-segment"

    issues = validate_shared_context_registry(_shared_manifest(), registry)

    assert any("Unknown permitted segment ID" in issue.message for issue in _errors(issues))


def test_required_context_segment_outside_declared_group_fails():
    manifest = _shared_manifest()
    manifest[0]["required_context_segments"] = "case-c_S1"

    issues = validate_retest_manifest(manifest, _shared_registry())

    assert any("outside the declared shared-context group" in issue.message for issue in _errors(issues))


def test_cross_case_context_with_permission_no_fails():
    manifest = _shared_manifest()
    manifest[0]["cross_case_context_permitted"] = "no"

    issues = validate_retest_manifest(manifest, _shared_registry())

    assert any("cross_case_context_permitted=no" in issue.message for issue in _errors(issues))


def test_shared_narrative_field_without_registry_entry_fails():
    manifest = _shared_manifest()
    manifest[0]["case_scope"] = "shared_narrative_field"
    manifest[0]["shared_context_ids"] = ""

    issues = validate_retest_manifest(manifest, _shared_registry())

    assert any("requires shared_context_ids" in issue.message for issue in _errors(issues))


def test_valid_shared_context_case_passes_registry_validation():
    issues = [
        *validate_shared_context_registry(_shared_manifest(), _shared_registry()),
        *validate_retest_manifest(_shared_manifest(), _shared_registry()),
    ]

    assert _errors(issues) == []


def test_local_primary_and_permitted_shared_context_segments_validate():
    record = _valid_record(
        case_id="case-a",
        status="retest_v0_2_1",
        language_access_mode="direct_original_language_access",
        case_scope="supplied_related_cases",
        shared_context_ids="ctx-1",
        cross_case_context_permitted="yes",
        required_context_segments="case-b_S1",
        evidence_nodes="",
        primary_evidence_segment_ids="case-a_S1",
        context_segment_ids="case-b_S1",
    )

    issues = validate_record(
        record,
        manifest_metadata=_shared_manifest(),
        shared_context_registry=_shared_registry(),
    )

    assert _errors(issues) == []


def test_annotation_context_segment_from_unrelated_case_fails():
    record = _valid_record(
        case_id="case-a",
        status="retest_v0_2_1",
        language_access_mode="direct_original_language_access",
        case_scope="supplied_related_cases",
        shared_context_ids="ctx-1",
        cross_case_context_permitted="yes",
        required_context_segments="case-b_S1",
        evidence_nodes="",
        primary_evidence_segment_ids="case-a_S1",
        context_segment_ids="case-c_S1",
    )

    issues = validate_record(
        record,
        manifest_metadata=_shared_manifest(),
        shared_context_registry=_shared_registry(),
    )

    assert any("unpermitted context segment" in issue.message for issue in _errors(issues))


def test_low_uncertainty_with_alternative_signature_warns():
    issues = validate_record(
        _valid_record(
            uncertainty_flag="low",
            rationale_note=(
                "This rationale documents a complete alternate pathway with "
                "enough detail for review while preserving the preferred one."
            ),
            alternative_signature=(
                "temporal_layering / extends / textual_anchor / "
                "commentarial_discourse / retrospective / medium"
            ),
        )
    )

    assert any(
        issue.field == "uncertainty_flag"
        and issue.severity == "warning"
        and "alternative_signature" in issue.message
        for issue in issues
    )


def test_evidence_anchor_and_anchor_node_are_both_required():
    missing_evidence_anchor = validate_record(
        _valid_record(evidence_anchor="")
    )
    missing_anchor_node = validate_record(_valid_record(anchor_node=""))

    assert any(
        issue.field == "evidence_anchor" for issue in _errors(missing_evidence_anchor)
    )
    assert any(
        issue.field == "anchor_node" for issue in _errors(missing_anchor_node)
    )


def test_valid_full_signature():
    signature = (
        "cue_function / supports / textual_anchor / intradiegetic / "
        "immediate / low"
    )

    parsed = parse_signature(signature)
    issues = validate_signature(signature)

    assert parsed.friction_locus == "cue_function"
    assert parsed.rationale_mechanism == "supports"
    assert issues == []


def test_invalid_full_signature():
    signature = "cue_function / supports / textual_anchor / intradiegetic / low"

    issues = validate_signature(signature)

    assert len(issues) == 1
    assert issues[0].field == "signature"


def test_invalid_full_signature_value():
    signature = (
        "cue_function / automatic_guess / textual_anchor / intradiegetic / "
        "immediate / low"
    )

    issues = validate_signature(signature)

    assert any(issue.field == "rationale_mechanism" for issue in _errors(issues))


def test_corrected_extradiegetic_spelling_is_valid():
    issues = validate_record(_valid_record(discourse_level="extradiegetic"))

    assert _errors(issues) == []


def test_old_discourse_level_spelling_is_invalid():
    old_spelling = "extra" + "gdiegetic"
    issues = validate_record(_valid_record(discourse_level=old_spelling))

    assert any(issue.field == "discourse_level" for issue in _errors(issues))


def test_field_name_is_not_valid_discourse_level_value():
    issues = validate_record(_valid_record(discourse_level="discourse_level"))

    assert any(issue.field == "discourse_level" for issue in _errors(issues))


def test_format_signature():
    signature = format_signature(_valid_record(rationale_mechanism="supports+extends"))

    assert signature == (
        "cue_function / supports+extends / textual_anchor / intradiegetic / "
        "immediate / low"
    )


def test_dataframe_validation_helpers():
    frame = pd.DataFrame(
        [
            _valid_record(),
            _valid_record(case_id="case-2", friction_locus="automatic_guess"),
        ]
    )

    issues = validate_dataframe(frame)
    report = validation_report(frame)

    assert any(issue.case_id == "case-2" for issue in _errors(issues))
    assert list(report.columns) == ["case_id", "field", "severity", "message"]


def test_question_log_validation_requires_provisional_resolution_fields():
    from trim.validator import validate_question_log_record

    issues = validate_question_log_record(
        {
            "question_id": "Q1",
            "case_id": "case-1",
            "question_type": "interpretive",
            "question_text": "Does a complete alternate pathway remain viable?",
            "provisional_resolution": "Use preferred pathway and record alternative.",
            "did_question_change_code": "yes",
            "blocking_or_nonblocking": "nonblocking",
            "requires_manual_revision": "uncertain",
            "coder_id": "coder_b",
        }
    )

    assert _errors(issues) == []


def test_question_log_rejects_unknown_controlled_values():
    from trim.validator import validate_question_log_record

    issues = validate_question_log_record(
        {
            "question_id": "Q1",
            "case_id": "case-1",
            "question_type": "private_hunch",
            "question_text": "Question",
            "provisional_resolution": "Resolution",
            "did_question_change_code": "maybe",
            "blocking_or_nonblocking": "soft",
            "requires_manual_revision": "sometimes",
            "coder_id": "coder_b",
        }
    )

    assert {
        issue.field
        for issue in _errors(issues)
    } >= {
        "question_type",
        "did_question_change_code",
        "blocking_or_nonblocking",
        "requires_manual_revision",
    }
