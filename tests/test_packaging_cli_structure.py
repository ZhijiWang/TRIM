import hashlib
import os
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path
from shutil import copyfile


ROOT = Path(__file__).parents[1]
SOURCE_CHECKOUT_MESSAGE = (
    "This command requires a TRIM-HAA source checkout.\n"
    "Install-package commands available here are: validate, verify-lock, compare, and version."
)


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    return subprocess.run(
        list(args),
        cwd=cwd or ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _one_line(text: str) -> str:
    return " ".join(text.split())


def test_public_python_api_and_version_exist():
    import trim_haa
    from trim_haa import (
        TrimHAAAnnotation,
        compare_annotations,
        lock_annotation,
        validate_core_record,
        validate_provenance_record,
        verify_locked_annotation,
    )

    assert trim_haa.__version__ == "0.3.0a1"
    assert "TrimHAAAnnotation" in trim_haa.__all__
    assert TrimHAAAnnotation
    assert validate_core_record
    assert validate_provenance_record
    assert lock_annotation
    assert verify_locked_annotation
    assert compare_annotations


def test_cli_help_version_validate_verify_and_compare():
    help_result = _run("trim-haa", "--help")
    assert help_result.returncode == 0
    assert "validate" in help_result.stdout
    assert "verify-lock" in help_result.stdout
    assert "compare" in help_result.stdout
    assert "version" in help_result.stdout
    help_text = _one_line(help_result.stdout)
    assert "Run the author-only walkthrough from a source checkout." in help_text
    assert "Run the synthetic dry-run workflow from a source checkout." in help_text

    module_help = _run(sys.executable, "-m", "trim_haa", "--help")
    assert module_help.returncode == 0
    assert "verify-lock" in module_help.stdout

    version = _run("trim-haa", "version")
    assert version.returncode == 0
    assert "0.3.0a1" in version.stdout

    valid = _run("trim-haa", "validate", "tests/fixtures/trim_haa/core_valid.csv")
    assert valid.returncode == 0
    assert "errors=0" in valid.stdout

    invalid = _run("trim-haa", "validate", "tests/fixtures/trim_haa/core_invalid.csv")
    assert invalid.returncode != 0
    assert "errors=" in invalid.stdout

    verified = _run(
        "trim-haa",
        "verify-lock",
        "tests/fixtures/trim_haa/core_valid.csv",
        "tests/fixtures/trim_haa/lock_valid.csv",
    )
    assert verified.returncode == 0
    assert "verification=passed" in verified.stdout

    tampered = _run(
        "trim-haa",
        "verify-lock",
        "tests/fixtures/trim_haa/core_valid.csv",
        "tests/fixtures/trim_haa/lock_tampered.csv",
    )
    assert tampered.returncode != 0
    assert "verification=failed" in tampered.stdout

    compared = _run(
        "trim-haa",
        "compare",
        "examples/in_a_grove_walkthrough/author_analytic_record.csv",
        "examples/in_a_grove_walkthrough/ai_independent_record.csv",
    )
    assert compared.returncode == 0
    assert "truth" not in compared.stdout.lower()
    assert "verdict" not in compared.stdout.lower()


def test_cli_run_walkthrough_succeeds():
    result = _run("trim-haa", "run-walkthrough")

    assert result.returncode == 0


def test_source_checkout_commands_fail_clearly_outside_checkout(tmp_path):
    for command in ("run-walkthrough", "run-synthetic"):
        result = _run("trim-haa", command, cwd=tmp_path)
        combined = result.stdout + result.stderr

        assert result.returncode != 0
        assert SOURCE_CHECKOUT_MESSAGE in combined
        assert "Traceback" not in combined


def test_repository_structure_and_legacy_absence():
    assert (ROOT / "src" / "trim_haa").is_dir()
    assert not (ROOT / "trim_haa").exists()
    assert not (ROOT / "trim").exists()
    assert (ROOT / "examples" / "synthetic_dry_run" / "valid").is_dir()
    assert (ROOT / "examples" / "synthetic_dry_run" / "invalid").is_dir()
    assert (ROOT / "examples" / "in_a_grove_walkthrough").is_dir()
    assert (ROOT / "research" / "position_note").is_dir()
    assert (ROOT / "research" / "future_human_study" / "ethics_drafts").is_dir()
    assert (ROOT / "research" / "future_human_study" / "pilot_protocol").is_dir()
    assert (ROOT / "artifacts" / "position_note").is_dir()
    assert (ROOT / "artifacts" / "future_human_study").is_dir()
    assert (ROOT / "docs" / "legacy_removal_inventory.csv").exists()


def test_readme_and_future_study_status_boundaries():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "docs" / "quickstart.md").read_text(encoding="utf-8")
    index = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
    research_status = (ROOT / "docs" / "research_status.md").read_text(encoding="utf-8")
    future = (ROOT / "research" / "future_human_study" / "README.md").read_text(
        encoding="utf-8"
    )

    assert readme.startswith("# TRIM-HAA")
    assert "sole active project" not in readme.lower()
    assert "It is no longer part of the active package" in readme
    assert "does not contain empirical human validation" in readme
    assert "## Installed-Package CLI" in readme
    assert "## Source-Checkout Demonstrations" in readme
    assert "The walkthrough source packet is not distributed inside the wheel." in readme
    assert "Installed-package functionality" in index
    assert "Source-checkout-only demonstrations" in index
    assert "Use the installed-package CLI" in quickstart
    assert "Source-checkout-only demonstrations" in quickstart
    assert "standalone for record validation, lock verification, provenance handling, and comparison" in research_status
    assert "Demonstrations remain repository-bound" in research_status
    assert "Deferred future human-subject study" in future
    assert "No ethics approval has been obtained" in future
    assert "not executable for recruitment" in future


def test_frozen_artifact_hashes_after_relocation():
    artifacts = ROOT / "artifacts"
    assert _sha256(artifacts / "position_note" / "TRIM_HAA_position_note_v0_1.zip") == "eae1c50f329a70fba02640aa07475b2fd985eaafaf2ac17bbe69630427c83433"
    assert _sha256(artifacts / "position_note" / "TRIM_HAA_position_note_v0_2.zip") == "cc734bff299a3193f6467c494b560a87ae35c5ed3de25a26457de878e1d4d94e"
    assert _sha256(artifacts / "future_human_study" / "TRIM_HAA_pilot_ethics_package_v0_1.zip") == "d09edd46b3c463f8c8c163058d6cbe084691bb044113efff7bb3d35e8c72bb69"
    assert _sha256(artifacts / "future_human_study" / "TRIM_HAA_pilot_ethics_package_v0_2.zip") == "8a0961033ea87beaa1733fce461b21ea388c74e889ebf29b2212db70671d29b0"
    assert _sha256(artifacts / "future_human_study" / "TRIM_HAA_pilot_ethics_package_v0_3.zip") == "3d3fcbdd7b5b9a23abe2982a815d4ab4c06c9bf592915bed1938f61584b721f2"


def test_research_boundaries_remain_visible():
    position_note = (ROOT / "research" / "position_note" / "TRIM_HAA_position_note_v0_1.md").read_text(encoding="utf-8").lower()
    walkthrough_readme = (ROOT / "examples" / "in_a_grove_walkthrough" / "README.md").read_text(encoding="utf-8").lower()
    future = (ROOT / "research" / "future_human_study" / "README.md").read_text(encoding="utf-8").lower()
    public_v02 = ROOT / "examples" / "in_a_grove_walkthrough_public_v0_2"
    public_author_records = list(public_v02.glob("author_record_v*/author_analytic_record.csv"))
    public_ai_records = list(public_v02.glob("ai_run_v*/ai_independent_record.csv"))

    assert "representation is not detection" in position_note
    assert "author-only" in walkthrough_readme
    assert "not human-subject data" in walkthrough_readme
    assert "no ethics approval has been obtained" in future
    assert public_author_records == [
        public_v02 / "author_record_v0_1" / "author_analytic_record.csv"
    ]
    assert public_ai_records == [
        public_v02 / "ai_run_v0_1" / "ai_independent_record.csv"
    ]
    assert list(public_v02.glob("ai_run_v*/model_run_manifest.csv")) == [
        public_v02 / "ai_run_v0_1" / "model_run_manifest.csv"
    ]
    assert not (public_v02 / "outputs").exists()
    assert not (public_v02 / "comparison").exists()


def test_version_and_pandas_dependency_classification_are_consistent():
    import trim_haa

    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    reporting = (ROOT / "src" / "trim_haa" / "reporting.py").read_text(encoding="utf-8")
    src_imports = [
        path
        for path in (ROOT / "src" / "trim_haa").glob("*.py")
        if "import pandas" in path.read_text(encoding="utf-8")
        or "from pandas" in path.read_text(encoding="utf-8")
    ]

    assert pyproject["project"]["version"] == "0.3.0a1"
    assert trim_haa.__version__ == "0.3.0a1"
    assert 'version: "0.3.0a1"' in citation
    assert pyproject["project"]["dependencies"] == []
    assert pyproject["project"]["optional-dependencies"]["reporting"] == ["pandas"]
    assert "pandas" in pyproject["project"]["optional-dependencies"]["test"]
    assert src_imports == [ROOT / "src" / "trim_haa" / "reporting.py"]
    assert "trim_haa.reporting requires the optional pandas dependency" in reporting


def test_built_wheel_boundary_and_clean_install_smoke(tmp_path):
    dist = tmp_path / "dist"
    build = _run(sys.executable, "-m", "build", "--wheel", "--outdir", str(dist))
    assert build.returncode == 0, build.stderr
    wheel = next(dist.glob("trim_haa-0.3.0a1-py3-none-any.whl"))

    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
    assert any(name.startswith("trim_haa/") for name in names)
    for excluded in ("research/", "examples/", "artifacts/", "tests/", "ethics/", "trim/"):
        assert not any(name.startswith(excluded) for name in names)
    assert not any("source_packet" in name for name in names)
    assert not any("TRIM_HAA_position_note" in name for name in names)

    venv = tmp_path / "venv"
    assert _run(sys.executable, "-m", "venv", str(venv)).returncode == 0
    python = venv / "bin" / "python"
    cli = venv / "bin" / "trim-haa"
    assert _run(str(python), "-m", "pip", "install", str(wheel), cwd=tmp_path).returncode == 0

    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    core = fixtures / "core_valid.csv"
    lock = fixtures / "lock_valid.csv"
    left = fixtures / "author_analytic_record.csv"
    right = fixtures / "ai_independent_record.csv"
    copyfile(ROOT / "tests" / "fixtures" / "trim_haa" / "core_valid.csv", core)
    copyfile(ROOT / "tests" / "fixtures" / "trim_haa" / "lock_valid.csv", lock)
    copyfile(ROOT / "examples" / "in_a_grove_walkthrough" / "author_analytic_record.csv", left)
    copyfile(ROOT / "examples" / "in_a_grove_walkthrough" / "ai_independent_record.csv", right)

    imported = _run(str(python), "-c", "import trim_haa; print(trim_haa.__version__)", cwd=tmp_path)
    assert imported.returncode == 0
    assert imported.stdout.strip() == "0.3.0a1"
    assert _run(str(cli), "--help", cwd=tmp_path).returncode == 0
    assert _run(str(cli), "version", cwd=tmp_path).stdout.strip() == "0.3.0a1"
    assert _run(str(cli), "validate", str(core), cwd=tmp_path).returncode == 0
    assert _run(str(cli), "verify-lock", str(core), str(lock), cwd=tmp_path).returncode == 0
    compared = _run(str(cli), "compare", str(left), str(right), cwd=tmp_path)
    assert compared.returncode == 0
    assert "truth" not in compared.stdout.lower()
    for command in ("run-walkthrough", "run-synthetic"):
        result = _run(str(cli), command, cwd=tmp_path)
        combined = result.stdout + result.stderr
        assert result.returncode != 0
        assert SOURCE_CHECKOUT_MESSAGE in combined
        assert "Traceback" not in combined
