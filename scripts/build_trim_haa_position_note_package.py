"""Build the deterministic TRIM-HAA position note package."""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_VERSION = "v0_2"
CREATED_AT = "2026-07-01T07:20:00+00:00"
ZIP_PATH = ROOT / "artifacts" / f"TRIM_HAA_position_note_{PACKAGE_VERSION}.zip"
ZIP_SHA_PATH = ROOT / "artifacts" / f"TRIM_HAA_position_note_{PACKAGE_VERSION}.zip.sha256"
MANIFEST_PATH = ROOT / "position_note" / "TRIM_HAA_position_note_v0_2_manifest.csv"
FIXED_ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


PACKAGE_FILES: tuple[dict[str, str], ...] = (
    {
        "artifact": "position_note/TRIM_HAA_position_note_v0_1.md",
        "status": "draft",
        "public_release_candidate": "no",
        "notes": "Working-paper draft; blockers unresolved.",
    },
    {
        "artifact": "position_note/TRIM_HAA_position_note_claim_boundaries.csv",
        "status": "draft",
        "public_release_candidate": "yes_after_review",
        "notes": "Claim-boundary table for public-language review.",
    },
    {
        "artifact": "position_note/TRIM_HAA_position_note_publication_blockers.md",
        "status": "draft",
        "public_release_candidate": "yes_after_review",
        "notes": "Publication blockers must be resolved before release.",
    },
    {
        "artifact": "position_note/TRIM_HAA_position_note_v0_1_review_response.md",
        "status": "draft",
        "public_release_candidate": "yes_after_review",
        "notes": "Reviewer-response memo for position-note hardening.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/README.md",
        "status": "draft",
        "public_release_candidate": "yes_after_review",
        "notes": "Walkthrough overview.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/source_packet.md",
        "status": "legal_review_required",
        "public_release_candidate": "no",
        "notes": "Translation status unresolved.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/source_provenance.md",
        "status": "draft",
        "public_release_candidate": "yes_after_review",
        "notes": "Source provenance and URLs.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/legal_and_translation_review.md",
        "status": "legal_review_required",
        "public_release_candidate": "yes_after_review",
        "notes": "Copyright blockers.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/source_segments.csv",
        "status": "legal_review_required",
        "public_release_candidate": "no",
        "notes": "Contains translated excerpt segments.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/annotation_instructions.md",
        "status": "draft",
        "public_release_candidate": "yes_after_review",
        "notes": "Local label and mechanism guide.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/author_analytic_record.csv",
        "status": "locked",
        "public_release_candidate": "yes_after_review",
        "notes": "Researcher-produced analytic demonstration; not human-subject data and not a gold standard.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/author_lock_manifest.csv",
        "status": "locked",
        "public_release_candidate": "yes_after_review",
        "notes": "Generated with TRIM-HAA locking utilities.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/ai_independent_record.csv",
        "status": "frozen",
        "public_release_candidate": "yes_after_review",
        "notes": "Independent model record; not a truth verdict.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/ai_raw_output.txt",
        "status": "frozen",
        "public_release_candidate": "provider_terms_review_required",
        "notes": "Exact model output; reproduction terms require review.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/prompts/in_a_grove_trim_haa_v0_1.txt",
        "status": "frozen",
        "public_release_candidate": "yes_after_review",
        "notes": "Prompt contains no secrets.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/prompt_manifest.csv",
        "status": "frozen",
        "public_release_candidate": "yes_after_review",
        "notes": "Prompt hash manifest.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/model_run_manifest.csv",
        "status": "frozen",
        "public_release_candidate": "development_artifact_only",
        "notes": "Model-run provenance; locally auditable but not externally reproducible from recorded metadata alone.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/outputs/validation_report.csv",
        "status": "generated",
        "public_release_candidate": "yes_after_review",
        "notes": "Core validation output.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/outputs/lock_verification_report.csv",
        "status": "generated",
        "public_release_candidate": "yes_after_review",
        "notes": "Author lock verification.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/outputs/field_comparison.csv",
        "status": "generated",
        "public_release_candidate": "yes_after_review",
        "notes": "Field-by-field comparison.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/outputs/evidence_comparison.csv",
        "status": "generated",
        "public_release_candidate": "yes_after_review",
        "notes": "Evidence overlap metrics.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/outputs/alternative_comparison.csv",
        "status": "generated",
        "public_release_candidate": "yes_after_review",
        "notes": "Alternative-pathway comparison.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/outputs/candidate_certainty_alternative_mismatch.md",
        "status": "generated",
        "public_release_candidate": "yes_after_review",
        "notes": "Author-defined review-question display; no truth verdict.",
    },
    {
        "artifact": "walkthrough/in_a_grove_v0_1/outputs/execution_summary.md",
        "status": "generated",
        "public_release_candidate": "yes_after_review",
        "notes": "Deterministic run summary.",
    },
)

MANIFEST_FIELDS = (
    "artifact",
    "version",
    "created_at",
    "sha256",
    "status",
    "public_release_candidate",
    "notes",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for entry in sorted(PACKAGE_FILES, key=lambda item: item["artifact"]):
        path = ROOT / entry["artifact"]
        if not path.exists():
            raise FileNotFoundError(path)
        rows.append(
            {
                "artifact": entry["artifact"],
                "version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "sha256": sha256_file(path),
                "status": entry["status"],
                "public_release_candidate": entry["public_release_candidate"],
                "notes": entry["notes"],
            }
        )
    return rows


def write_manifest(rows: list[dict[str, str]]) -> None:
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_zip(rows: list[dict[str, str]]) -> str:
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    files = [row["artifact"] for row in rows] + [str(MANIFEST_PATH.relative_to(ROOT))]
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative_path in sorted(files):
            path = ROOT / relative_path
            info = zipfile.ZipInfo(relative_path, date_time=FIXED_ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    digest = sha256_file(ZIP_PATH)
    ZIP_SHA_PATH.write_text(f"{digest}  {ZIP_PATH.name}\n", encoding="utf-8")
    return digest


def main() -> int:
    rows = build_manifest()
    write_manifest(rows)
    digest = write_zip(rows)
    print(f"{ZIP_PATH.relative_to(ROOT)} {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
