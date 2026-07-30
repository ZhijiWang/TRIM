import hashlib
from pathlib import Path
import tomllib

from trim_haa.indexing import STRICT_INDEXING_API_VERSION
from trim_haa.schema import CORE_FIELDS


ROOT = Path(__file__).parents[1]
BOUNDARY = ROOT / "docs" / "repository_maintenance_boundary.md"
ADR = ROOT / "docs" / "adr" / "ADR_repository_maintenance_boundary.md"
PROVENANCE_SHA256 = "92e075aa74afd0661fb6446c1253863883b651df735aaec0ec073638af0fdd14"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_maintenance_documents_exist_and_are_linked():
    assert BOUNDARY.is_file()
    assert ADR.is_file()

    index = _read(ROOT / "docs" / "index.md")
    assert "(repository_maintenance_boundary.md)" in index
    assert "(adr/ADR_repository_maintenance_boundary.md)" in index


def test_readme_describes_the_current_unversioned_boundary():
    readme = _read(ROOT / "README.md")

    assert "current Core records are legacy-unversioned" in readme
    assert 'Core version `"1"` is not implemented' in readme
    assert 'MUST NOT add `core_record_version="1"`' in readme
    assert 'Core version `"1"` is active' not in readme


def test_runtime_and_frozen_version_boundaries_remain_unchanged():
    project = tomllib.loads(_read(ROOT / "pyproject.toml"))

    assert "core_record_version" not in CORE_FIELDS
    assert not (ROOT / "src" / "trim_haa" / "compat").exists()
    assert STRICT_INDEXING_API_VERSION == "1"
    assert project["project"]["version"] == "0.3.0a1"
    assert (
        hashlib.sha256(
            (ROOT / "src" / "trim_haa" / "provenance.py").read_bytes()
        ).hexdigest()
        == PROVENANCE_SHA256
    )


def test_boundary_records_maintenance_reopening_and_research_limits():
    boundary = _read(BOUNDARY)

    for heading in (
        "## 4. Maintenance-mode definition",
        "## 5. Reopening triggers",
        "## 6. Non-triggers",
        "## 9. Deferred-work register",
        "## 10. Closure verdict",
    ):
        assert heading in boundary

    assert "This is a software-infrastructure verdict only." in boundary
    assert "READY_FOR_INFRASTRUCTURE_MAINTENANCE_MODE" in boundary
    assert 'Core version `"1"` is not implemented' in boundary
    assert "Phase 1 is not implemented" in boundary
    assert "does not establish" in boundary
    assert "authorization to execute a study" in boundary
    assert "Empirical execution is not authorized" in boundary
    assert 'Core version `"1"` is implemented' not in boundary
    assert "Phase 1 is implemented" not in boundary
    assert "Empirical validation exists." not in boundary
    assert "Execution is authorized." not in boundary
