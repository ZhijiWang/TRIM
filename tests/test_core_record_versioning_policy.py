import hashlib
from pathlib import Path
import tomllib

from trim_haa.indexing import STRICT_INDEXING_API_VERSION
from trim_haa.schema import CORE_FIELDS


ROOT = Path(__file__).parents[1]
POLICY = ROOT / "docs" / "core_record_versioning_policy.md"
ADR = ROOT / "docs" / "adr" / "ADR_core_record_versioning.md"
PROVENANCE_SHA256 = "92e075aa74afd0661fb6446c1253863883b651df735aaec0ec073638af0fdd14"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_core_record_versioning_policy_decisions_are_consistent():
    policy = _read(POLICY)
    adr = _read(ADR)

    for document in (policy, adr):
        assert "`core_record_version`" in document
        assert 'version `"1"`' in document
        assert "legacy-unversioned" in document
        assert "`trim_haa.compat.legacy_unversioned`" in document

    assert '`STRICT_INDEXING_API_VERSION == "1"`' in policy
    assert "Indexing API version `\"1\"` and Core record" in policy
    assert "Accepted for future implementation." in adr


def test_policy_and_adr_are_linked_from_documentation():
    index = _read(ROOT / "docs" / "index.md")
    strict_design = _read(ROOT / "docs" / "versioned_strict_indexing_design.md")
    audit = _read(ROOT / "docs" / "active_identifier_indexing_audit.md")

    assert "(core_record_versioning_policy.md)" in index
    assert "(adr/ADR_core_record_versioning.md)" in index
    assert "(core_record_versioning_policy.md)" in strict_design
    assert "(core_record_versioning_policy.md)" in audit
    assert "(../core_record_versioning_policy.md)" in _read(ADR)


def test_phase_one_establishes_legacy_boundary_before_core_version_one():
    policy = _read(POLICY)
    adr = _read(ADR)

    assert "### Phase 1: dispatch and compatibility boundary" in policy
    assert "`trim_haa.compat.legacy_unversioned`, or an equivalent explicitly" in policy
    assert "every existing public and internal Core reader or" in policy
    assert (
        "Phase 2 MUST NOT begin until every Phase 1 compatibility-boundary and routing"
        in policy
    )
    assert 'Core version `"1"` MUST NOT be added to any production schema' in policy
    assert "entrypoint can accept missing version metadata" in policy
    assert "Phase 1 prerequisites to Core version" in adr
    assert "Phase 2 MUST NOT begin while an active non-frozen entrypoint" in adr


def test_design_does_not_prematurely_change_runtime_boundaries():
    project = tomllib.loads(_read(ROOT / "pyproject.toml"))

    assert "core_record_version" not in CORE_FIELDS
    assert STRICT_INDEXING_API_VERSION == "1"
    assert project["project"]["version"] == "0.3.0a1"
    assert not (ROOT / "src" / "trim_haa" / "compat").exists()
    assert (
        hashlib.sha256((ROOT / "src" / "trim_haa" / "provenance.py").read_bytes()).hexdigest()
        == PROVENANCE_SHA256
    )
