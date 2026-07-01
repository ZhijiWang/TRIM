from pathlib import Path


ROOT = Path(__file__).parents[1]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_public_text_layer_status_is_documented_without_completed_walkthrough_claim():
    research_status = _read(ROOT / "docs" / "research_status.md")
    readme = _read(ROOT / "README.md")
    public_dir = ROOT / "examples" / "in_a_grove_walkthrough_public_v0_2"

    assert public_dir.is_dir()
    assert "Japanese-canonical, English-gloss public walkthrough text layer is under author review" in research_status
    assert "contains no new annotation records and is not yet frozen" in research_status
    assert "draft Japanese-canonical public text layer" in readme
    assert "no new annotation records" in readme
    assert "completed Japanese-canonical walkthrough" not in (research_status + readme).lower()
