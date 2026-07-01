from pathlib import Path


ROOT = Path(__file__).parents[1]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_public_walkthrough_status_is_documented_without_overclaim():
    research_status = _read(ROOT / "docs" / "research_status.md")
    readme = _read(ROOT / "README.md")
    public_dir = ROOT / "examples" / "in_a_grove_walkthrough_public_v0_2"

    assert public_dir.is_dir()
    assert "Japanese-canonical public walkthrough v0.2" in research_status
    assert "locked author/model records and a frozen descriptive comparison" in research_status
    assert "representability demonstration and descriptive locked-record comparison" in research_status
    assert "frozen Japanese-canonical public walkthrough v0.2" in readme
    assert "locked author record, a frozen independent AI run, and a frozen descriptive comparison" in readme
    assert "not empirical validation" in (research_status + readme)
    assert "truth verdict" in (research_status + readme)
    assert "general claim about model behaviour" in research_status
