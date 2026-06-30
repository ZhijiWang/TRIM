from pathlib import Path
import tomllib


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "0.2.2"


def test_unreleased_version_metadata_is_consistent():
    pyproject = tomllib.loads(
        (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    citation = (PROJECT_ROOT / "CITATION.cff").read_text(encoding="utf-8")
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    changelog = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert pyproject["project"]["version"] == EXPECTED_VERSION
    assert f'version: "{EXPECTED_VERSION}"' in citation
    assert "date-released:" not in citation
    assert f"Current source version: {EXPECTED_VERSION} (unreleased)." in readme
    assert f"## {EXPECTED_VERSION} - Unreleased" in changelog


def test_codebook_filename_and_heading_match_package_version():
    codebook = PROJECT_ROOT / "docs" / "TRIM_codebook_v0_2_2.md"
    old_codebook = PROJECT_ROOT / "docs" / "TRIM_codebook_v0_1_2.md"

    assert codebook.exists()
    assert not old_codebook.exists()
    assert codebook.read_text(encoding="utf-8").startswith(
        "# TRIM Codebook v0.2.2"
    )


def test_reliability_extra_declares_scikit_learn_without_core_dependency():
    pyproject = tomllib.loads(
        (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert pyproject["project"]["optional-dependencies"]["reliability"] == [
        "scikit-learn"
    ]
    assert "scikit-learn" not in pyproject["project"]["dependencies"]
