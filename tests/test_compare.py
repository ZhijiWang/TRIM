from pathlib import Path

from trim.compare import (
    broad_family_table,
    compare_case_pair,
    contested_cases_table,
    find_same_broad_family_different_signature,
    find_same_cue_different_function,
    find_same_function_different_signature,
    group_by_function,
    same_cue_table,
    same_function_table,
    signature_string,
)
from trim.io import annotations_to_dataframe, load_annotations


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _demo_frame():
    annotations = load_annotations(PROJECT_ROOT / "data" / "demo_annotations.csv")
    return annotations_to_dataframe(annotations)


def test_signature_string_uses_six_part_form():
    frame = _demo_frame()
    row = frame.loc[frame["case_id"] == "ZZ_XIANG_7"].iloc[0]

    assert signature_string(row) == (
        "operation_function / stabilizes / textual_anchor+ritual_sequence / "
        "intradiegetic / immediate / low"
    )


def test_group_by_function_returns_case_groups():
    grouped = group_by_function(_demo_frame())
    immediate = grouped.loc[
        grouped["function_label"] == "immediate_stabilization"
    ].iloc[0]

    assert immediate["case_count"] == 2
    assert "ZZ_XIANG_7" in immediate["case_ids"]
    assert "ZZ_MIN_1" in immediate["case_ids"]


def test_same_function_different_signature_expected_cases():
    table = find_same_function_different_signature(_demo_frame())

    immediate = table.loc[
        table["function_label"] == "immediate_stabilization"
    ].iloc[0]
    extended = table.loc[
        table["function_label"] == "extended_deliberation"
    ].iloc[0]

    assert immediate["signature_count"] == 2
    assert "ZZ_XIANG_7" in immediate["case_ids"]
    assert "ZZ_MIN_1" in immediate["case_ids"]
    assert extended["signature_count"] == 2
    assert "ZZ_XI_4" in extended["case_ids"]
    assert "ZZ_ZHUANG_22" in extended["case_ids"]
    assert "interpretive_payoff" not in table.columns
    assert immediate["comparison_prompt"] == (
        "Shared function label; differing threshold-rationale signatures. "
        "Interpret the substantive significance of the differing "
        "evidence-to-function pathways."
    )


def test_same_cue_different_function_includes_prophecy_cases():
    table = find_same_cue_different_function(_demo_frame())
    prophecy = table.loc[table["cue_family"] == "prophecy"].iloc[0]

    assert prophecy["function_count"] == 3
    assert "MAC_1_3" in prophecy["case_ids"]
    assert "MAC_4_1" in prophecy["case_ids"]
    assert "MAC_5_8" in prophecy["case_ids"]


def test_same_cue_filter_accepts_string():
    table = same_cue_table(_demo_frame(), cue_family_filter="prophecy")

    assert list(table["cue_family"]) == ["prophecy"]


def test_same_cue_filter_accepts_list():
    table = find_same_cue_different_function(
        _demo_frame(),
        cue_family_filter=["prophecy", "testimony"],
    )

    assert list(table["cue_family"]) == ["prophecy", "testimony"]


def test_broad_family_different_signature_includes_self_exculpatory_testimony():
    table = find_same_broad_family_different_signature(_demo_frame())
    testimony = table.loc[
        table["broad_function_family"] == "self-exculpatory testimony"
    ].iloc[0]

    assert testimony["signature_count"] == 2
    assert "GROVE_TAJOMARU" in testimony["case_ids"]
    assert "GROVE_MASAGO" in testimony["case_ids"]
    assert "interpretive_payoff" not in table.columns
    assert testimony["comparison_prompt"].startswith(
        "Shared broad function family; differing threshold-rationale signatures."
    )


def test_contested_cases_include_xi_4():
    table = contested_cases_table(_demo_frame())

    assert list(table["case_id"]) == ["ZZ_XI_4"]
    assert table.iloc[0]["alternative_signature"]


def test_compare_case_pair_flags_same_function_different_signature():
    comparison = compare_case_pair(_demo_frame(), "ZZ_XIANG_7", "ZZ_MIN_1")

    assert comparison["same_function"] is True
    assert comparison["same_cue"] is True
    assert comparison["same_signature"] is False
    assert "friction_locus" in comparison["difference_summary"]


def test_article_ready_table_aliases_match_find_functions():
    frame = _demo_frame()

    assert same_function_table(frame).equals(
        find_same_function_different_signature(frame)
    )
    assert same_cue_table(frame).equals(find_same_cue_different_function(frame))
    assert broad_family_table(frame).equals(
        find_same_broad_family_different_signature(frame)
    )
