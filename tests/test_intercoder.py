from pathlib import Path
import subprocess
import sys

import pandas as pd

from trim.intercoder import (
    apply_disagreement_categories,
    cohen_kappa_if_two_coders,
    compatible_single_compound_value,
    compound_value_metrics,
    contested_disagreement_report,
    disagreement_table,
    pairwise_agreement,
    pairwise_compound_agreement,
    pairwise_segment_agreement,
    percent_agreement,
    primary_context_segment_overlap,
    pivot_coder_annotations,
    segment_set_metrics,
    stratified_pairwise_agreement,
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


def test_compound_value_metrics_preserve_primary_and_set_distinctions():
    reordered = compound_value_metrics(
        "authorizes+reframes",
        "reframes+authorizes",
    )
    partial = compound_value_metrics(
        "authorizes+reframes",
        "authorizes+projects",
    )

    assert reordered == {
        "exact_set_agreement": True,
        "primary_agreement": False,
        "any_overlap_agreement": True,
        "jaccard_overlap": 1.0,
    }
    assert partial["exact_set_agreement"] is False
    assert partial["primary_agreement"] is True
    assert partial["any_overlap_agreement"] is True
    assert partial["jaccard_overlap"] == 1 / 3


def test_pairwise_compound_agreement_reports_multiple_views():
    frame = pd.DataFrame(
        [
            {
                "case_id": "case-1",
                "coder_id": "coder_a",
                "rationale_mechanism": "authorizes+reframes",
            },
            {
                "case_id": "case-1",
                "coder_id": "coder_b",
                "rationale_mechanism": "reframes+authorizes",
            },
            {
                "case_id": "case-2",
                "coder_id": "coder_a",
                "rationale_mechanism": "stabilizes+projects",
            },
            {
                "case_id": "case-2",
                "coder_id": "coder_b",
                "rationale_mechanism": "stabilizes",
            },
        ]
    )

    row = pairwise_compound_agreement(
        frame,
        "rationale_mechanism",
    ).iloc[0]

    assert row["comparable_cases"] == 2
    assert row["exact_set_agreement"] == 0.5
    assert row["primary_agreement"] == 0.5
    assert row["compatible_single_compound_agreement"] == 1.0
    assert row["any_overlap_agreement"] == 1.0
    assert row["mean_jaccard_overlap"] == 0.75


def test_compatible_single_compound_value_reports_containment():
    assert compatible_single_compound_value("authorizes", "authorizes+reframes")
    assert compatible_single_compound_value("reframes+authorizes", "authorizes")
    assert not compatible_single_compound_value("extends", "authorizes+reframes")


def test_segment_set_metrics_and_pairwise_segment_agreement():
    frame = pd.DataFrame(
        [
            {
                "case_id": "case-1",
                "coder_id": "coder_a",
                "primary_evidence_segment_ids": "S1|S2",
            },
            {
                "case_id": "case-1",
                "coder_id": "coder_b",
                "primary_evidence_segment_ids": "S2|S3",
            },
            {
                "case_id": "case-2",
                "coder_id": "coder_a",
                "primary_evidence_segment_ids": "S4",
            },
            {
                "case_id": "case-2",
                "coder_id": "coder_b",
                "primary_evidence_segment_ids": "S4",
            },
        ]
    )

    assert segment_set_metrics("S1|S2", "S2|S3")["jaccard_overlap"] == 1 / 3
    row = pairwise_segment_agreement(frame).iloc[0]

    assert row["comparable_cases"] == 2
    assert row["exact_set_agreement"] == 0.5
    assert row["any_overlap_agreement"] == 1.0


def test_primary_context_segment_overlap_reports_cross_role_overlap():
    frame = pd.DataFrame(
        [
            {
                "case_id": "case-1",
                "coder_id": "coder_a",
                "primary_evidence_segment_ids": "S1|S2",
                "context_segment_ids": "S3",
            },
            {
                "case_id": "case-1",
                "coder_id": "coder_b",
                "primary_evidence_segment_ids": "S2|S3",
                "context_segment_ids": "S1",
            },
        ]
    )

    row = primary_context_segment_overlap(frame).iloc[0]

    assert row["primary_jaccard_overlap"] == 1 / 3
    assert row["context_jaccard_overlap"] == 0.0
    assert row["cross_role_overlap"] == "S1|S3"


def test_compound_value_metrics_require_nonempty_values():
    try:
        compound_value_metrics("", "supports")
    except ValueError as exc:
        assert "non-empty" in str(exc)
    else:
        raise AssertionError("Expected ValueError for an empty compound value.")


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
    assert set(table["raw_disagreement"]) == {"yes"}


def test_apply_disagreement_categories_preserves_raw_rows():
    table = disagreement_table(_coded_rows(), ["function_label"])
    categorized = apply_disagreement_categories(
        table,
        {"ZZ_MIN_1": "substantive_pathway_variation"},
    )
    row = categorized.iloc[0]

    assert row["raw_disagreement"] == "yes"
    assert row["adjudicated_substantive_pathway_variation"] == "yes"
    assert row["disagreement_category"] == "substantive_pathway_variation"


def test_stratified_pairwise_agreement_reports_language_and_scope():
    frame = _coded_rows()
    frame["language_access_mode"] = "direct_original_language_access"
    frame["case_scope"] = [
        "local_passage",
        "local_passage",
        "shared_narrative_field",
        "shared_narrative_field",
    ]

    table = stratified_pairwise_agreement(frame, "function_label")

    assert {"language_access_mode", "case_scope"} <= set(table["stratum_field"])


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


def test_intercoder_demo_runs_directly(tmp_path):
    script = PROJECT_ROOT / "examples" / "run_intercoder_demo.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "intercoder_report:" in result.stdout
