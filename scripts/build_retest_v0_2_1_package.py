"""Build the v0.2.1 coder-facing retest package.

The ZIP is deterministic and intentionally excludes pilot results,
adjudication, tests, working notes, and expected labels.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


PACKAGE_NAME = "TRIM_retest_v0_2_1_coder_package.zip"
FIXED_ZIP_TIME = (2026, 6, 25, 0, 0, 0)

PACKAGE_FILES: tuple[str, ...] = (
    "docs/TRIM_codebook_v0_2_1.md",
    "docs/TRIM_Coding_Manual_v0_2_1_friction_locus.md",
    "docs/TRIM_Coding_Manual_v0_2_1_rationale_mechanism.md",
    "docs/discourse_level_guide_v0_2_1.md",
    "docs/retest_v0_2_1_coder_guide.md",
    "data/retest_v0_2_1_case_manifest.csv",
    "data/retest_v0_2_1_source_packet.md",
    "data/retest_v0_2_1_coding_template.csv",
    "data/retest_v0_2_1_question_log_template.csv",
    "data/retest_v0_2_1_practice_cases.md",
    "data/retest_v0_2_1_language_access_form.csv",
)

FORBIDDEN_PACKAGE_PATTERNS: tuple[str, ...] = (
    "primary_coder",
    "primary annotation",
    "adjudication_workbook",
    "adjudication outcome",
    "pilot_v0_2_0_results",
    "v0_2_0_usability_pilot",
    "substantive_demo_interpretations",
    "answer_key",
    "expected_label",
    "expected_function",
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
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=None,
        help="Output directory. Defaults to outputs/coder_packages.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    outdir = args.outdir or root / "outputs" / "coder_packages"
    outdir.mkdir(parents=True, exist_ok=True)
    zip_path = outdir / PACKAGE_NAME
    sums_path = outdir / "TRIM_retest_v0_2_1_coder_package.SHA256SUMS.txt"

    _assert_no_leakage(root)
    _write_zip(root, zip_path)
    _write_sums(root, zip_path, sums_path)
    print(zip_path)
    print(sums_path)
    return 0


def _write_zip(root: Path, zip_path: Path) -> None:
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in PACKAGE_FILES:
            source = root / relative
            data = source.read_bytes()
            info = ZipInfo(relative, FIXED_ZIP_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)


def _write_sums(root: Path, zip_path: Path, sums_path: Path) -> None:
    rows = [
        f"{_sha256(zip_path)}  {zip_path.name}",
    ]
    for relative in PACKAGE_FILES:
        rows.append(f"{_sha256(root / relative)}  {relative}")
    sums_path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def _assert_no_leakage(root: Path) -> None:
    for relative in PACKAGE_FILES:
        lowered_name = relative.lower()
        for pattern in FORBIDDEN_PACKAGE_PATTERNS:
            if pattern.lower() in lowered_name:
                raise ValueError(f"Forbidden package filename pattern: {relative}")
        text = (root / relative).read_text(encoding="utf-8").lower()
        for pattern in FORBIDDEN_PACKAGE_PATTERNS:
            if pattern.lower() in text:
                raise ValueError(
                    f"Forbidden package content pattern {pattern!r} in {relative}"
                )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
