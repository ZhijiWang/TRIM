from pathlib import Path
import hashlib
import subprocess
import sys
import zipfile

import pandas as pd

from trim.schema import ANNOTATION_FIELDS


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

