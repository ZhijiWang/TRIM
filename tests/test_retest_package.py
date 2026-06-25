from pathlib import Path
import hashlib
import shutil
import subprocess
import sys
import zipfile

import pandas as pd

from scripts.build_retest_v0_2_1_package import PACKAGE_FILES, semantic_steering_audit
from trim.schema import ANNOTATION_FIELDS
from trim.validator import (
    validate_retest_manifest,
    validate_shared_context_registry,
    validate_source_packet_segment_coverage,
)
from trim.vocabulary import (
    DISCOURSE_LEVELS,
    FRICTION_LOCI,
    FUNCTION_LABELS,
    RATIONALE_MECHANISMS,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_CASE_IDS = {
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


def test_retest_template_uses_canonical_schema_fields():
    template = pd.read_csv(
        PROJECT_ROOT / "data" / "retest_v0_2_1_coding_template.csv",
        dtype=str,
        keep_default_na=False,
    )

    assert tuple(template.columns) == ANNOTATION_FIELDS
    assert len(template) == 12
    assert set(template["case_id"]).isdisjoint(ORIGINAL_CASE_IDS)
    assert set(template["function_label"]) == {""}
    assert set(template["primary_evidence_segment_ids"]) == {""}


def test_retest_manifest_records_scope_language_and_segments():
    manifest = pd.read_csv(
        PROJECT_ROOT / "data" / "retest_v0_2_1_case_manifest.csv",
        dtype=str,
        keep_default_na=False,
    )

    assert len(manifest) == 12
    assert set(manifest["case_id"]).isdisjoint(ORIGINAL_CASE_IDS)
    assert "published_translation" in set(manifest["language_access_mode"])
    assert "direct_original_language_access" in set(manifest["language_access_mode"])
    assert "shared_narrative_field" in set(manifest["case_scope"])
    assert all(manifest["segment_ids"].str.contains("_S"))
    assert not (
        set(manifest["case_type"])
        & (DISCOURSE_LEVELS | FRICTION_LOCI | FUNCTION_LABELS | RATIONALE_MECHANISMS)
    )


def test_coder_facing_metadata_avoids_analytic_descriptors():
    manifest = pd.read_csv(
        PROJECT_ROOT / "data" / "retest_v0_2_1_case_manifest.csv",
        dtype=str,
        keep_default_na=False,
    )
    template = pd.read_csv(
        PROJECT_ROOT / "data" / "retest_v0_2_1_coding_template.csv",
        dtype=str,
        keep_default_na=False,
    )
    prohibited = {
        "reported_speech",
        "material_warrant",
        "recognition_testimony",
        "oracle_and_inquiry",
        "prophetic_interpretation",
        "omen_and_persuasion",
        "staged_testimony",
        "testimony_and_command",
        *FUNCTION_LABELS,
        *FRICTION_LOCI,
        *DISCOURSE_LEVELS,
        *RATIONALE_MECHANISMS,
    }

    combined = "\n".join(
        [
            manifest.to_csv(index=False),
            template[
                ["case_id", "case_label", "source", "language", "case_type"]
            ].to_csv(index=False),
        ]
    )

    assert not any(term in combined for term in prohibited)


def test_current_shared_context_registry_and_manifest_pass():
    manifest = pd.read_csv(
        PROJECT_ROOT / "data" / "retest_v0_2_1_case_manifest.csv",
        dtype=str,
        keep_default_na=False,
    )
    registry = pd.read_csv(
        PROJECT_ROOT / "data" / "retest_v0_2_1_shared_context_registry.csv",
        dtype=str,
        keep_default_na=False,
    )

    issues = [
        *validate_shared_context_registry(manifest, registry),
        *validate_retest_manifest(manifest, registry),
    ]

    assert issues == []


def test_source_packet_contains_every_formal_and_required_segment():
    manifest = pd.read_csv(
        PROJECT_ROOT / "data" / "retest_v0_2_1_case_manifest.csv",
        dtype=str,
        keep_default_na=False,
    )
    packet = (
        PROJECT_ROOT / "data" / "retest_v0_2_1_source_packet.md"
    ).read_text(encoding="utf-8")

    assert validate_source_packet_segment_coverage(manifest, packet) == []


def test_current_semantic_steering_audit_passes():
    audit = semantic_steering_audit(PROJECT_ROOT)

    assert audit["unreviewed_high_risk_count"] == 0
    assert audit["match_count"] == 0


def test_source_packet_case_descriptions_do_not_contain_function_labels():
    packet = (
        PROJECT_ROOT / "data" / "retest_v0_2_1_source_packet.md"
    ).read_text(encoding="utf-8")

    assert not any(function_label in packet for function_label in FUNCTION_LABELS)


def test_instructional_vocabulary_is_allowed_by_steering_audit():
    codebook = (
        PROJECT_ROOT / "docs" / "TRIM_codebook_v0_2_1.md"
    ).read_text(encoding="utf-8")
    audit = semantic_steering_audit(PROJECT_ROOT)

    assert "immediate_stabilization" in codebook
    assert audit["unreviewed_high_risk_count"] == 0


def test_inserted_expected_function_phrase_fails_package_generation(tmp_path):
    root = _copy_package_root(tmp_path)
    source_packet = root / "data" / "retest_v0_2_1_source_packet.md"
    source_packet.write_text(
        source_packet.read_text(encoding="utf-8")
        + "\nExpected_function: immediate_stabilization\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "build_retest_v0_2_1_package.py"),
            "--root",
            str(root),
            "--outdir",
            str(tmp_path / "out"),
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "expected_function" in result.stderr.lower()


def test_inserted_semantic_steering_phrase_fails_package_generation(tmp_path):
    root = _copy_package_root(tmp_path)
    source_packet = root / "data" / "retest_v0_2_1_source_packet.md"
    source_packet.write_text(
        source_packet.read_text(encoding="utf-8")
        + "\nThis passage stabilizes the omen.\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "build_retest_v0_2_1_package.py"),
            "--root",
            str(root),
            "--outdir",
            str(tmp_path / "out"),
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "semantic-steering audit failed" in result.stderr.lower()


def test_reproducible_coder_package_checksums(tmp_path):
    script = PROJECT_ROOT / "scripts" / "build_retest_v0_2_1_package.py"
    first = tmp_path / "first"
    second = tmp_path / "second"

    subprocess.run(
        [sys.executable, str(script), "--outdir", str(first)],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [sys.executable, str(script), "--outdir", str(second)],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    first_zip = first / "TRIM_retest_v0_2_1_coder_package.zip"
    second_zip = second / "TRIM_retest_v0_2_1_coder_package.zip"
    first_hash = _sha256(first_zip)
    second_hash = _sha256(second_zip)

    assert first_hash == second_hash
    sums = (
        first / "TRIM_retest_v0_2_1_coder_package.SHA256SUMS.txt"
    ).read_text(encoding="utf-8")
    assert f"{first_hash}  TRIM_retest_v0_2_1_coder_package.zip" in sums


def test_coder_package_leakage(tmp_path):
    script = PROJECT_ROOT / "scripts" / "build_retest_v0_2_1_package.py"
    subprocess.run(
        [sys.executable, str(script), "--outdir", str(tmp_path)],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    package = tmp_path / "TRIM_retest_v0_2_1_coder_package.zip"
    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        combined_text = "\n".join(
            archive.read(name).decode("utf-8")
            for name in names
            if name.endswith((".md", ".csv"))
        )

    forbidden = {
        *ORIGINAL_CASE_IDS,
        "primary_coder",
        "expected_function",
        "answer_key",
        "pilot_v0_2_0_results",
        "substantive_demo_interpretations",
    }
    assert not any("pilot_archive" in name for name in names)
    assert not any(pattern in combined_text for pattern in forbidden)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _copy_package_root(tmp_path: Path) -> Path:
    root = tmp_path / "root"
    for relative in PACKAGE_FILES:
        source = PROJECT_ROOT / relative
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return root
