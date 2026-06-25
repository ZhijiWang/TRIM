from pathlib import Path

from trim.vocabulary import (
    DISCOURSE_LEVELS,
    FRICTION_LOCI,
    FUNCTION_LABELS,
    LANGUAGE_ACCESS_MODES,
    RATIONALE_MECHANISMS,
    UNCERTAINTY_FLAGS,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_v0_2_1_codebook_lists_controlled_vocabularies():
    text = (PROJECT_ROOT / "docs" / "TRIM_codebook_v0_2_1.md").read_text(
        encoding="utf-8"
    )

    for vocabulary in (
        FUNCTION_LABELS,
        FRICTION_LOCI,
        RATIONALE_MECHANISMS,
        DISCOURSE_LEVELS,
        UNCERTAINTY_FLAGS,
        LANGUAGE_ACCESS_MODES,
    ):
        for value in vocabulary:
            assert f"`{value}`" in text


def test_context_inference_exclusion_examples_are_documented():
    text = (
        PROJECT_ROOT / "docs" / "TRIM_Coding_Manual_v0_2_1_friction_locus.md"
    ).read_text(encoding="utf-8")

    assert "Explicit-textual-operation exclusion" in text
    assert "Positive:" in text
    assert "Near miss:" in text
    assert "Counterfactual:" in text


def test_discourse_level_decision_tree_is_documented():
    text = (
        PROJECT_ROOT / "docs" / "discourse_level_guide_v0_2_1.md"
    ).read_text(encoding="utf-8")

    assert "Testimony/Frame Decision Tree" in text
    assert "`reported_speech`" in text
    assert "`frame_narrative`" in text
    assert "shared_context_ids" in text

