from pathlib import Path

import pandas as pd

from trim.intercoder import (
    cohen_kappa_if_two_coders,
    contested_disagreement_report,
    disagreement_table,
    pairwise_agreement,
    percent_agreement,
    pivot_coder_annotations,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _coded_rows():
    return pd.DataFrame(
        [
            {
                "case_id": "ZZ_XIANG_7",
                "case_label": "Xiang 7",
                "coder_id": "coder_a",
                "function_label": "immediate_stabilization",
                "friction_locus": "operation_function",
                "rationale_mechanism": "stabilizes",
                "temporal_orientation": "immediate",
                "uncertainty_flag": "low",
            },
            {
                "case_id": "ZZ_XIANG_7",
                "case_label": "Xiang 7",
                "coder_id": "coder_b",
                "function_label": "immediate_stabilization",
                "friction_locus": "operation_function",
                "rationale_mechanism": "stabilizes",
                "temporal_orientation": "immediate",
                "uncertainty_flag": "low",
            },
            {
                "case_id": "ZZ_MIN_1",
                "case_label": "Min 1",
                "coder_id": "coder_a",
                "function_label": "immediate_stabilization",
                "friction_locus": "warrant_attribution",
                "rationale_mechanism": "stabilizes+projects",
                "temporal_orientation": "prospective",
                "uncertainty_flag": "medium",
            },
            {
                "case_id": "ZZ_MIN_1",
                "case_label": "Min 1",
                "coder_id": "coder_b",
                "function_label": "extended_deliberation",
                "friction_locus": "warrant_relation",
                "rationale_mechanism": "extends",
                "temporal_orientation": "recursive",
                "uncertainty_flag": "medium",
            },
        ]
    )


def test_pivot_coder_annotations():
    pivot = pivot_coder_annotations(_coded_rows(), "function_label")

    assert list(pivot.columns) == ["coder_a", "coder_b"]
    assert pivot.loc["ZZ_XIANG_7", "coder_a"] == "immediate_stabilization"
    assert pivot.loc["ZZ_MIN_1", "coder_b"] == "extended_deliberation"


def test_percent_agreement():
    agreement = percent_agreement(_coded_rows(), "function_label")

    assert agreement == 0.5


def test_pairwise_agreement():
    table = pairwise_agreement(_coded_rows(), "function_label")
    row = table.iloc[0]

    assert row["coder_id_1"] == "coder_a"
    assert row["coder_id_2"] == "coder_b"
    assert row["comparable_cases"] == 2
    assert row["agreements"] == 1
    assert row["percent_agreement"] == 0.5


def test_cohen_kappa_if_two_coders_is_optional():
    result = cohen_kappa_if_two_coders(_coded_rows(), "function_label")

    assert result["field"] == "function_label"
    assert result["coder_ids"] == ["coder_a", "coder_b"]
    assert result["comparable_cases"] == 2
    assert "kappa" in result
    assert "warning" in result


def test_cohen_kappa_warns_for_wrong_coder_count():
    frame = pd.concat(
        [
            _coded_rows(),
            pd.DataFrame(
                [
                    {
                        "case_id": "ZZ_XIANG_7",
                        "coder_id": "coder_c",
                        "function_label": "immediate_stabilization",
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

    result = cohen_kappa_if_two_coders(frame, "function_label")

    assert result["kappa"] is None
    assert result["warning"] == "Cohen's kappa requires exactly two coders."


def test_disagreement_table():
    table = disagreement_table(
        _coded_rows(),
        ["function_label", "friction_locus", "uncertainty_flag"],
    )

    assert set(table["field"]) == {"function_label", "friction_locus"}
    assert set(table["case_id"]) == {"ZZ_MIN_1"}
    assert all(
        "coder_a=" in value and "coder_b=" in value
        for value in table["coder_values"]
    )


def test_contested_disagreement_report_leaves_human_review_columns_blank():
    report = contested_disagreement_report(_coded_rows())

    assert "locatable?" in report.columns
    assert "rationale-coherent?" in report.columns
    assert "resists simple refinement?" in report.columns
    assert set(report["locatable?"]) == {""}
    assert "ZZ_MIN_1" in set(report["case_id"])


def test_single_coder_demo_data_does_not_produce_agreement_claims():
    frame = pd.read_csv(PROJECT_ROOT / "data" / "demo_annotations.csv", dtype=str)

    assert pd.isna(percent_agreement(frame, "function_label"))
    assert pairwise_agreement(frame, "function_label").empty


def test_second_coder_template_has_no_annotation_values():
    template = pd.read_csv(
        PROJECT_ROOT / "data" / "demo_annotations_second_coder_template.csv",
        dtype=str,
        keep_default_na=False,
    )

    assert len(template) == 10
    assert set(template["coder_id"]) == {"second_coder"}
    assert set(template["case_id"]) == {
        "ZZ_XIANG_7",
        "ZZ_MIN_1",
        "ZZ_XI_4",
        "ZZ_ZHUANG_22",
        "MAC_1_3",
        "MAC_4_1",
        "MAC_5_8",
        "GROVE_TAJOMARU",
        "GROVE_MASAGO",
        "GROVE_TAKEHIRO",
    }
    annotation_columns = [
        "function_label",
        "friction_locus",
        "rationale_mechanism",
        "temporal_orientation",
        "uncertainty_flag",
    ]
    assert all((template[column] == "").all() for column in annotation_columns)
