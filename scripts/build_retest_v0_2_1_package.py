"""Build the v0.2.1 coder-facing retest package.

The ZIP is deterministic and intentionally excludes pilot results,
adjudication, tests, working notes, and expected labels.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

PROJECT_ROOT_FOR_IMPORT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT_FOR_IMPORT))

from trim.validator import (
    validate_retest_manifest,
    validate_shared_context_registry,
    validate_source_packet_segment_coverage,
    validate_source_text_provenance,
)
from trim.vocabulary import (
    DISCOURSE_LEVELS,
    EPISTEMIC_SUPPORT_VALUES,
    FRICTION_LOCI,
    FUNCTION_LABELS,
    RATIONALE_MECHANISMS,
)


PACKAGE_NAME = "TRIM_retest_v0_2_1_coder_package.zip"
FIXED_ZIP_TIME = (2026, 6, 25, 0, 0, 0)

PACKAGE_FILES: tuple[str, ...] = (
    "docs/TRIM_codebook_v0_2_1.md",
    "docs/TRIM_Coding_Manual_v0_2_1_friction_locus.md",
    "docs/TRIM_Coding_Manual_v0_2_1_rationale_mechanism.md",
    "docs/discourse_level_guide_v0_2_1.md",
    "docs/retest_v0_2_1_coder_guide.md",
    "data/retest_v0_2_1_case_manifest.csv",
    "data/retest_v0_2_1_shared_context_registry.csv",
    "data/retest_v0_2_1_source_packet.md",
    "data/retest_v0_2_1_source_text_provenance.csv",
    "data/retest_v0_2_1_coding_template.csv",
    "data/retest_v0_2_1_question_log_template.csv",
    "data/retest_v0_2_1_practice_cases.md",
    "data/retest_v0_2_1_language_access_form.csv",
)

INSTRUCTIONAL_FILES: frozenset[str] = frozenset(
    {
        "docs/TRIM_codebook_v0_2_1.md",
        "docs/TRIM_Coding_Manual_v0_2_1_friction_locus.md",
        "docs/TRIM_Coding_Manual_v0_2_1_rationale_mechanism.md",
        "docs/discourse_level_guide_v0_2_1.md",
        "docs/retest_v0_2_1_coder_guide.md",
    }
)

CASE_SPECIFIC_FILES: frozenset[str] = frozenset(
    file_path for file_path in PACKAGE_FILES if file_path not in INSTRUCTIONAL_FILES
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

PROHIBITED_ANALYTIC_PATTERNS: tuple[str, ...] = (
    r"\breinterpret(?:s|ed|ing)?\b",
    r"\brefram(?:e|es|ed|ing)\b",
    r"\bauthoriz(?:e|es|ed|ing|ation)\b",
    r"\bstabili[sz](?:e|es|ed|ing|ation)\b",
    r"\bconfirm(?:s|ed|ing|ation)?\b",
    r"\bconvert(?:s|ed|ing)?\b",
    r"\bsuspend(?:s|ed|ing)?\b",
    r"\bexpos(?:e|es|ed|ing)\b",
    r"\brecognition chain\b",
    r"\baccumulated testimony\b",
    r"\bpractical force\b",
    r"\bself-justifying\b",
    r"\baction-guiding\b",
    r"\bwarrant\b",
    r"\bframing\b",
    r"\binterpretive operation\b",
    r"\bprophetic_interpretation\b",
    r"\bomen_and_persuasion\b",
    r"\bmaterial_warrant\b",
    r"\brecognition_testimony\b",
    r"\boracle_and_inquiry\b",
    r"\bstaged_testimony\b",
    r"\btestimony_and_command\b",
)

ANSWER_BEARING_PATTERNS: tuple[str, ...] = (
    "expected_function",
    "expected_label",
    "answer_key",
    "correct_function",
    "gold_label",
)

STEERING_ALLOWLIST: tuple[dict[str, str], ...] = ()


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
    audit_json_path = outdir / "TRIM_retest_v0_2_1_semantic_steering_audit.json"
    audit_text_path = outdir / "TRIM_retest_v0_2_1_semantic_steering_audit.txt"

    _assert_no_leakage(root)
    _assert_manifest_integrity(root)
    audit = semantic_steering_audit(root)
    _write_steering_reports(audit, audit_json_path, audit_text_path)
    _assert_no_unreviewed_steering(audit)
    _write_zip(root, zip_path)
    _write_sums(root, zip_path, sums_path, [audit_json_path, audit_text_path])
    print(zip_path)
    print(sums_path)
    print(audit_text_path)
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


def _write_sums(
    root: Path,
    zip_path: Path,
    sums_path: Path,
    audit_paths: list[Path],
) -> None:
    rows = [
        f"{_sha256(zip_path)}  {zip_path.name}",
    ]
    for relative in PACKAGE_FILES:
        rows.append(f"{_sha256(root / relative)}  {relative}")
    for audit_path in audit_paths:
        rows.append(f"{_sha256(audit_path)}  {audit_path.name}")
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


def _assert_manifest_integrity(root: Path) -> None:
    manifest = _read_csv(root / "data" / "retest_v0_2_1_case_manifest.csv")
    registry = _read_csv(root / "data" / "retest_v0_2_1_shared_context_registry.csv")
    provenance = _read_csv(root / "data" / "retest_v0_2_1_source_text_provenance.csv")
    source_packet = (root / "data" / "retest_v0_2_1_source_packet.md").read_text(
        encoding="utf-8"
    )
    issues = [
        *validate_shared_context_registry(manifest, registry),
        *validate_retest_manifest(manifest, registry),
        *validate_source_packet_segment_coverage(manifest, source_packet),
        *validate_source_text_provenance(manifest, provenance, source_packet),
    ]
    if issues:
        details = "\n".join(
            f"[{issue.severity}] {issue.case_id} {issue.field}: {issue.message}"
            for issue in issues
        )
        raise ValueError(f"Retest manifest integrity failed:\n{details}")


def semantic_steering_audit(root: Path) -> dict[str, object]:
    """Return a machine-readable semantic-steering audit for coder files."""

    matches: list[dict[str, object]] = []
    provenance = _read_csv(root / "data" / "retest_v0_2_1_source_text_provenance.csv")
    provenance_by_segment = {
        row["segment_id"]: row for row in provenance if row.get("segment_id")
    }
    source_quote_lines = _source_quote_lines(
        (root / "data" / "retest_v0_2_1_source_packet.md").read_text(
            encoding="utf-8"
        )
    )
    controlled_terms = sorted(
        set(FUNCTION_LABELS)
        | set(FRICTION_LOCI)
        | set(DISCOURSE_LEVELS)
        | set(RATIONALE_MECHANISMS)
        | set(EPISTEMIC_SUPPORT_VALUES)
    )
    for relative in CASE_SPECIFIC_FILES:
        path = root / relative
        lines = path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            lowered = line.lower()
            for term in controlled_terms:
                if term.lower() in lowered:
                    matches.append(
                        _audit_match(
                            relative,
                            line_number,
                            term,
                            "controlled_term",
                            line,
                            source_quote_lines,
                            provenance_by_segment,
                        )
                    )
            for pattern in PROHIBITED_ANALYTIC_PATTERNS:
                if re.search(pattern, line, flags=re.IGNORECASE):
                    matches.append(
                        _audit_match(
                            relative,
                            line_number,
                            pattern,
                            "analytic_descriptor",
                            line,
                            source_quote_lines,
                            provenance_by_segment,
                        )
                    )
            for pattern in ANSWER_BEARING_PATTERNS:
                if pattern.lower() in lowered:
                    matches.append(
                        _audit_match(
                            relative,
                            line_number,
                            pattern,
                            "answer_bearing_phrase",
                            line,
                            source_quote_lines,
                            provenance_by_segment,
                        )
                    )

    allowlisted = 0
    unreviewed = 0
    verified_source = 0
    neutral_metadata = 0
    answer_bearing = 0
    for match in matches:
        if match.get("reason") == "verified_source_quotation":
            match["status"] = "allowlisted"
            match["category"] = "verified_source_text_match"
            allowlisted += 1
            verified_source += 1
        elif _is_allowlisted(match):
            match["status"] = "allowlisted"
            allowlisted += 1
        elif match["category"] == "answer_bearing_phrase":
            match["status"] = "unreviewed_high_risk"
            answer_bearing += 1
            unreviewed += 1
        else:
            match["status"] = "unreviewed_high_risk"
            unreviewed += 1

    return {
        "instructional_files": sorted(INSTRUCTIONAL_FILES),
        "case_specific_files": sorted(CASE_SPECIFIC_FILES),
        "allowlist_entries": list(STEERING_ALLOWLIST),
        "match_count": len(matches),
        "allowlisted_match_count": allowlisted,
        "verified_source_text_match_count": verified_source,
        "neutral_metadata_match_count": neutral_metadata,
        "unreviewed_project_authored_analytic_match_count": unreviewed - answer_bearing,
        "answer_bearing_phrase_count": answer_bearing,
        "unreviewed_high_risk_count": unreviewed,
        "matches": matches,
    }


def _write_steering_reports(
    audit: dict[str, object],
    audit_json_path: Path,
    audit_text_path: Path,
) -> None:
    audit_json_path.write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    lines = [
        "TRIM v0.2.1 semantic-steering audit",
        f"match_count: {audit['match_count']}",
        f"allowlisted_match_count: {audit['allowlisted_match_count']}",
        f"verified_source_text_match_count: {audit['verified_source_text_match_count']}",
        f"neutral_metadata_match_count: {audit['neutral_metadata_match_count']}",
        (
            "unreviewed_project_authored_analytic_match_count: "
            f"{audit['unreviewed_project_authored_analytic_match_count']}"
        ),
        f"answer_bearing_phrase_count: {audit['answer_bearing_phrase_count']}",
        f"unreviewed_high_risk_count: {audit['unreviewed_high_risk_count']}",
        "",
    ]
    matches = audit["matches"]
    if not matches:
        lines.append("No case-specific semantic-steering matches detected.")
    else:
        for match in matches:  # pragma: no cover - exercised by failure tests
            lines.append(
                "{file}:{line} [{category}/{status}] {pattern}: {excerpt}".format(
                    **match
                )
            )
    audit_text_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _assert_no_unreviewed_steering(audit: dict[str, object]) -> None:
    if int(audit["unreviewed_high_risk_count"]):
        matches = audit["matches"]
        details = "\n".join(
            "{file}:{line} {pattern}: {excerpt}".format(**match)
            for match in matches
            if match["status"] == "unreviewed_high_risk"
        )
        raise ValueError(f"Semantic-steering audit failed:\n{details}")


def _audit_match(
    file_path: str,
    line_number: int,
    pattern: str,
    category: str,
    line: str,
    source_quote_lines: dict[tuple[str, int], str],
    provenance_by_segment: dict[str, dict[str, str]],
) -> dict[str, object]:
    match = {
        "file": file_path,
        "line": line_number,
        "pattern": pattern,
        "category": category,
        "excerpt": line.strip(),
        "status": "unreviewed_high_risk",
    }
    segment_id = source_quote_lines.get((file_path, line_number))
    provenance = provenance_by_segment.get(segment_id or "")
    if segment_id and provenance:
        match.update(
            {
                "segment_id": segment_id,
                "edition_or_translation": provenance["edition_or_translation"],
                "source": provenance["source"],
                "reason": "verified_source_quotation",
            }
        )
    return match


def _is_allowlisted(match: dict[str, object]) -> bool:
    for entry in STEERING_ALLOWLIST:
        if (
            entry.get("file") == match["file"]
            and entry.get("pattern") == match["pattern"]
            and entry.get("excerpt") == match["excerpt"]
        ):
            return True
    return False


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _source_quote_lines(source_packet_text: str) -> dict[tuple[str, int], str]:
    """Map source-packet line numbers inside Source text blocks to segment IDs."""

    segment_by_line: dict[tuple[str, int], str] = {}
    current_segment: str | None = None
    in_source_text = False
    file_path = "data/retest_v0_2_1_source_packet.md"
    for line_number, line in enumerate(source_packet_text.splitlines(), start=1):
        heading = re.match(r"^#### `([^`]+)`\s*$", line)
        if heading:
            current_segment = heading.group(1)
            in_source_text = False
            continue
        if current_segment is None:
            continue
        if line.strip() == "Source text:":
            in_source_text = True
            continue
        if line.startswith("Navigation note:"):
            in_source_text = False
            continue
        if in_source_text and line.strip():
            segment_by_line[(file_path, line_number)] = current_segment
    return segment_by_line


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
