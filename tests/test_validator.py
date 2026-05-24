import pandas as pd

from trim.signature import parse_signature
from trim.validator import (
    format_signature,
    validate_dataframe,
    validate_record,
    validate_signature,
    validation_report,
)


def _valid_record(**overrides):
    values = {
        "case_id": "case-1",
        "case_label": "demo case",
        "source": "demo",
        "function_label": "demo function",
        "evidence_anchor": "demo anchor",
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


def test_valid_single_mechanism():
    issues = validate_record(_valid_record(rationale_mechanism="supports"))

    assert _errors(issues) == []


def test_valid_compound_mechanism():
    issues = validate_record(_valid_record(rationale_mechanism="supports+extends"))

    assert _errors(issues) == []


def test_invalid_mechanism():
    issues = validate_record(_valid_record(rationale_mechanism="automatic_guess"))

    assert any(issue.field == "rationale_mechanism" for issue in _errors(issues))


def test_too_many_compound_mechanisms():
    issues = validate_record(
        _valid_record(rationale_mechanism="supports+extends+narrows")
    )

    assert any("no more than 2" in issue.message for issue in _errors(issues))


def test_duplicate_compound_mechanism():
    issues = validate_record(_valid_record(rationale_mechanism="extends+extends"))

    assert any("duplicate compound value" in issue.message for issue in _errors(issues))


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
