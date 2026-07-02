"""Run the deterministic TRIM-HAA In a Grove author-only walkthrough."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from trim_haa.comparison import copied_phrase_overlap, normalised_token_overlap, segment_set_metrics
from trim_haa.hashing import sha256_file, sha256_text
from trim_haa.locking import LOCK_MANIFEST_FIELDS, create_lock_record, verify_locked_annotation
from trim_haa.schema import CORE_FIELDS, TrimHAAAnnotation
from trim_haa.validator import validate_core_record


ROOT = PROJECT_ROOT / "examples" / "in_a_grove_walkthrough"
OUTPUTS = ROOT / "outputs"
AUTHOR_LOCKED_AT = "2026-07-01T05:20:00+00:00"
AI_RUN_TIMESTAMP = "2026-07-01T05:40:00+00:00"
PROMPT_CREATED_AT = "2026-07-01T05:30:00+00:00"
AUTHOR_LOCK_PATH = ROOT / "author_lock_manifest.csv"
PROMPT_MANIFEST_PATH = ROOT / "prompt_manifest.csv"
MODEL_RUN_MANIFEST_PATH = ROOT / "model_run_manifest.csv"


def main() -> int:
    run_walkthrough()
    return 0


def run_walkthrough() -> dict[str, Any]:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    source_segments = _read_csv(ROOT / "source_segments.csv")
    author = TrimHAAAnnotation.from_record(_read_csv(ROOT / "author_analytic_record.csv")[0])
    ai = TrimHAAAnnotation.from_record(_read_csv(ROOT / "ai_independent_record.csv")[0])

    source_packet_hash = sha256_file(ROOT / "source_packet.md")
    instruction_set_hash = sha256_file(ROOT / "annotation_instructions.md")
    prompt_hash = sha256_file(ROOT / "prompts" / "in_a_grove_trim_haa_v0_1.txt")
    ai_output_hash = sha256_file(ROOT / "ai_raw_output.txt")

    _write_author_lock(author, source_packet_hash, instruction_set_hash)
    _write_prompt_manifest(prompt_hash)
    _write_model_run_manifest(prompt_hash, source_packet_hash, instruction_set_hash, ai_output_hash)

    lock_record = _read_csv(AUTHOR_LOCK_PATH)[0]
    lock_verified = verify_locked_annotation(author, lock_record)

    validation_rows = _validation_rows(author, ai)
    _write_csv(OUTPUTS / "validation_report.csv", ["annotation_id", "field", "severity", "message"], validation_rows)

    lock_rows = [
        {
            "annotation_id": author.annotation_id,
            "lock_manifest_id": lock_record["lock_manifest_id"],
            "lock_verified": str(lock_verified),
            "locked_at": lock_record["locked_at"],
            "canonical_record_sha256": lock_record["canonical_record_sha256"],
            "source_packet_sha256": source_packet_hash,
            "instruction_set_sha256": instruction_set_hash,
        }
    ]
    _write_csv(
        OUTPUTS / "lock_verification_report.csv",
        [
            "annotation_id",
            "lock_manifest_id",
            "lock_verified",
            "locked_at",
            "canonical_record_sha256",
            "source_packet_sha256",
            "instruction_set_sha256",
        ],
        lock_rows,
    )

    field_rows = _field_comparison(author, ai)
    _write_csv(
        OUTPUTS / "field_comparison.csv",
        ["field", "author_value", "ai_value", "same"],
        field_rows,
    )

    evidence_rows = _evidence_comparison(author, ai, source_segments)
    _write_csv(
        OUTPUTS / "evidence_comparison.csv",
        [
            "author_segments",
            "ai_segments",
            "shared_segments",
            "author_unique_segments",
            "ai_unique_segments",
            "exact_match",
            "jaccard",
        ],
        evidence_rows,
    )

    alternative_rows = _alternative_comparison(author, ai)
    _write_csv(
        OUTPUTS / "alternative_comparison.csv",
        [
            "author_alternative_present",
            "ai_alternative_present",
            "author_alternative_mechanism",
            "ai_alternative_mechanism",
            "author_alternative_note",
            "ai_alternative_note",
            "ai_retains_alternative",
        ],
        alternative_rows,
    )

    candidate_status = _candidate_status(ai)
    candidate_markdown = _candidate_markdown(
        author,
        ai,
        source_segments,
        evidence_rows[0],
        candidate_status,
        prompt_hash,
        ai_output_hash,
    )
    (OUTPUTS / "candidate_certainty_alternative_mismatch.md").write_text(
        candidate_markdown,
        encoding="utf-8",
    )

    summary = _summary(
        validation_rows,
        lock_verified,
        candidate_status,
        source_packet_hash,
        instruction_set_hash,
        prompt_hash,
        ai_output_hash,
    )
    (OUTPUTS / "execution_summary.md").write_text(summary, encoding="utf-8")
    return {
        "validation_rows": validation_rows,
        "lock_verified": lock_verified,
        "candidate_status": candidate_status,
    }


def _validation_rows(author: TrimHAAAnnotation, ai: TrimHAAAnnotation) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for record in (author, ai):
        for issue in validate_core_record(record):
            rows.append(issue.to_dict())
    return rows


def _write_author_lock(author: TrimHAAAnnotation, source_packet_hash: str, instruction_set_hash: str) -> None:
    lock = create_lock_record(
        author,
        lock_manifest_id="LOCK_IAG_V01_AUTHOR_PRE",
        locked_at=AUTHOR_LOCKED_AT,
        locked_by="AUTHOR_ANALYTIC",
        notes=(
            "researcher-produced analytic demonstration; not human-subject data and not a gold standard; "
            "author_record_version=v0_1;prompt_independent=true;"
            f"source_packet_sha256={source_packet_hash};instruction_set_sha256={instruction_set_hash}"
        ),
    )
    _write_csv(AUTHOR_LOCK_PATH, list(LOCK_MANIFEST_FIELDS), [lock.to_record()])


def _write_prompt_manifest(prompt_hash: str) -> None:
    _write_csv(
        PROMPT_MANIFEST_PATH,
        [
            "prompt_template_id",
            "prompt_version",
            "prompt_purpose",
            "prompt_text_path",
            "prompt_sha256",
            "created_at",
            "frozen",
            "notes",
        ],
        [
            {
                "prompt_template_id": "IAG_TRIM_HAA_V0_1",
                "prompt_version": "v0_1",
                "prompt_purpose": "Independent TRIM-HAA Core annotation for In a Grove walkthrough.",
                "prompt_text_path": "prompts/in_a_grove_trim_haa_v0_1.txt",
                "prompt_sha256": prompt_hash,
                "created_at": PROMPT_CREATED_AT,
                "frozen": "yes",
                "notes": "Prompt provides frozen source packet and local label/mechanism guide; no hidden system prompt included.",
            }
        ],
    )


def _write_model_run_manifest(
    prompt_hash: str,
    source_packet_hash: str,
    instruction_set_hash: str,
    ai_output_hash: str,
) -> None:
    _write_csv(
        MODEL_RUN_MANIFEST_PATH,
        [
            "model_run_id",
            "provider",
            "model_name",
            "model_version_or_date",
            "run_timestamp",
            "prompt_template_id",
            "prompt_hash",
            "system_prompt_hash",
            "temperature_or_sampling",
            "retry_count",
            "regenerated_output",
            "tool_access",
            "conversation_context_description",
            "source_packet_hash",
            "instruction_set_hash",
            "output_file",
            "output_sha256",
            "notes",
        ],
        [
            {
                "model_run_id": "IAG_MODEL_RUN_V0_1",
                "provider": "OpenAI",
                "model_name": "Codex session model",
                "model_version_or_date": "2026-07-01",
                "run_timestamp": AI_RUN_TIMESTAMP,
                "prompt_template_id": "IAG_TRIM_HAA_V0_1",
                "prompt_hash": prompt_hash,
                "system_prompt_hash": "unavailable",
                "temperature_or_sampling": "unavailable",
                "retry_count": "0",
                "regenerated_output": "no",
                "tool_access": "none for model output generation",
                "conversation_context_description": "Author-only technical walkthrough in PR #15; no human-subject data.",
                "source_packet_hash": source_packet_hash,
                "instruction_set_hash": instruction_set_hash,
                "output_file": "ai_raw_output.txt",
                "output_sha256": ai_output_hash,
                "notes": (
                    "Output is a submitted justificatory record, not hidden model reasoning. "
                    "The model artifact is locally auditable but not externally reproducible from the recorded metadata alone; "
                    "exact public model identifier, provider-side system configuration, sampling configuration, and reconstructable session context are unavailable."
                ),
            }
        ],
    )


def _field_comparison(author: TrimHAAAnnotation, ai: TrimHAAAnnotation) -> list[dict[str, str]]:
    fields = (
        "function_label",
        "rationale_mechanism",
        "uncertainty_flag",
        "rationale_note",
        "alternative_pathway_present",
        "alternative_mechanism",
        "alternative_note",
    )
    rows = []
    for field in fields:
        author_value = getattr(author, field)
        ai_value = getattr(ai, field)
        rows.append(
            {
                "field": field,
                "author_value": author_value,
                "ai_value": ai_value,
                "same": str(author_value == ai_value),
            }
        )
    rows.append(
        {
            "field": "rationale_note_token_overlap",
            "author_value": f"{normalised_token_overlap(author.rationale_note, ai.rationale_note):.6f}",
            "ai_value": f"{copied_phrase_overlap(author.rationale_note, ai.rationale_note):.6f}",
            "same": "not_applicable",
        }
    )
    rows.append(
        {
            "field": "walkthrough_result",
            "author_value": "structured disagreement: unresolved_agency, contrast_or_tension, medium uncertainty, alternative retained",
            "ai_value": "structured disagreement: self_inflicted_death, direct_action, low uncertainty, no alternative retained",
            "same": "False",
        }
    )
    rows.append(
        {
            "field": "candidate_status_interpretation",
            "author_value": "not a gold standard or adjudication",
            "ai_value": "author-defined review-rule trigger; not an independently validated mismatch",
            "same": "not_applicable",
        }
    )
    return rows


def _evidence_comparison(
    author: TrimHAAAnnotation,
    ai: TrimHAAAnnotation,
    source_segments: list[dict[str, str]],
) -> list[dict[str, str]]:
    known_segments = {row["segment_id"] for row in source_segments}
    author_set = set(author.primary_evidence_segment_ids)
    ai_set = set(ai.primary_evidence_segment_ids)
    if not author_set <= known_segments or not ai_set <= known_segments:
        missing = sorted((author_set | ai_set) - known_segments)
        raise ValueError(f"Unknown evidence segment IDs: {missing}")
    metrics = segment_set_metrics(author.primary_evidence_segment_ids, ai.primary_evidence_segment_ids)
    return [
        {
            "author_segments": "|".join(author.primary_evidence_segment_ids),
            "ai_segments": "|".join(ai.primary_evidence_segment_ids),
            "shared_segments": "|".join(sorted(author_set & ai_set)),
            "author_unique_segments": "|".join(sorted(author_set - ai_set)),
            "ai_unique_segments": "|".join(sorted(ai_set - author_set)),
            "exact_match": str(metrics["exact_match"]),
            "jaccard": f"{metrics['jaccard']:.6f}",
        }
    ]


def _alternative_comparison(author: TrimHAAAnnotation, ai: TrimHAAAnnotation) -> list[dict[str, str]]:
    return [
        {
            "author_alternative_present": author.alternative_pathway_present,
            "ai_alternative_present": ai.alternative_pathway_present,
            "author_alternative_mechanism": author.alternative_mechanism,
            "ai_alternative_mechanism": ai.alternative_mechanism,
            "author_alternative_note": author.alternative_note,
            "ai_alternative_note": ai.alternative_note,
            "ai_retains_alternative": str(ai.alternative_pathway_present == "yes"),
        }
    ]


def _candidate_status(ai: TrimHAAAnnotation) -> str:
    ai_text = " ".join(
        [
            ai.rationale_note.lower(),
            ai.alternative_note.lower(),
            "|".join(ai.primary_evidence_segment_ids).lower(),
        ]
    )
    acknowledges_unidentified_actor = "iag-sam-012" in ai_text or "someone" in ai_text or "unidentified" in ai_text
    if ai.uncertainty_flag == "low" and ai.alternative_pathway_present == "no" and not acknowledges_unidentified_actor:
        return "candidate_visible"
    if ai.uncertainty_flag == "low" and ai.alternative_pathway_present == "yes":
        return "candidate_not_visible"
    return "insufficient_information"


def _segment_lookup(source_segments: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["segment_id"]: row for row in source_segments}


def _segments(ids: list[str] | tuple[str, ...] | set[str], source_segments: list[dict[str, str]]) -> str:
    lookup = _segment_lookup(source_segments)
    lines = []
    for segment_id in ids:
        text = lookup.get(segment_id, {}).get("segment_text", "")
        lines.append(f"- `{segment_id}`: {text}")
    return "\n".join(lines) if lines else "- none"


def _candidate_markdown(
    author: TrimHAAAnnotation,
    ai: TrimHAAAnnotation,
    source_segments: list[dict[str, str]],
    evidence_row: dict[str, str],
    candidate_status: str,
    prompt_hash: str,
    ai_output_hash: str,
) -> str:
    shared = [item for item in evidence_row["shared_segments"].split("|") if item]
    author_unique = [item for item in evidence_row["author_unique_segments"].split("|") if item]
    ai_unique = [item for item in evidence_row["ai_unique_segments"].split("|") if item]
    ai_distinguishes = "no"
    if "someone" in ai.rationale_note.lower() or "unidentified" in ai.rationale_note.lower() or ai.alternative_pathway_present == "yes":
        ai_distinguishes = "yes"

    return "\n".join(
        [
            "# Review Question Generated: Candidate Certainty-Closure Tension",
            "",
            f"Display status: `{candidate_status}`",
            "",
            "`candidate_visible` is a walkthrough display status. It means that the configured author-defined review condition was satisfied. It does not establish that the packet objectively contains a competing causal account or that the inspected record is erroneous.",
            "",
            "This display describes a candidate certainty-closure tension: a record reports low uncertainty and no alternative while omitting or not addressing a packet-anchored element that the walkthrough has designated for review as potentially relevant to interpretive closure.",
            "",
            "The status is not an adjudicated property of the model record. It does not prove that an alternative interpretation is required. It does not prove that low uncertainty is inappropriate. It does not prove model error. It does not prove overconfidence. It generates a review question.",
            "",
            "## AI Record",
            "",
            f"- Function label: `{ai.function_label}`",
            f"- Uncertainty: `{ai.uncertainty_flag}`",
            f"- Rationale mechanism: `{ai.rationale_mechanism}`",
            f"- Alternative present: `{ai.alternative_pathway_present}`",
            f"- Alternative note: {ai.alternative_note or 'none'}",
            "- Selected evidence:",
            _segments(ai.primary_evidence_segment_ids, source_segments),
            f"- Rationale note: {ai.rationale_note}",
            "",
            "## Author Analytic Record",
            "",
            "Researcher-produced analytic demonstration; not human-subject data and not a gold standard.",
            "",
            f"- Function label: `{author.function_label}`",
            f"- Uncertainty: `{author.uncertainty_flag}`",
            f"- Rationale mechanism: `{author.rationale_mechanism}`",
            f"- Alternative present: `{author.alternative_pathway_present}`",
            f"- Alternative note: {author.alternative_note or 'none'}",
            "- Selected evidence:",
            _segments(author.primary_evidence_segment_ids, source_segments),
            f"- Rationale note: {author.rationale_note}",
            "",
            "## Evidence Overlap",
            "",
            "- Shared evidence:",
            _segments(shared, source_segments),
            "- Evidence unique to author record:",
            _segments(author_unique, source_segments),
            "- Evidence unique to AI record:",
            _segments(ai_unique, source_segments),
            "",
            "## Alternative Handling",
            "",
            f"- AI record retains an alternative: `{ai.alternative_pathway_present == 'yes'}`",
            f"- AI rationale explicitly distinguishes or excludes the alternative: `{ai_distinguishes}`",
            "- Packet segment designated by the walkthrough for review as potentially relevant to interpretive closure:",
            _segments(["IAG-SAM-012"], source_segments),
            "- Procedural finding: IAG-SAM-012 was present in the packet and the prompt required explicit alternative assessment, so the absence of an alternative in the AI record cannot be attributed to missing input or a missing response field.",
            "- Open evaluation question: whether IAG-SAM-012 warranted retaining an alternative remains open to independent evaluation.",
            "",
            "## External Cultural Claim Audit",
            "",
            "- AI external cultural claim: none recorded.",
            "- Packet-supported: not applicable.",
            "- Separately marked: not applicable.",
            "",
            "## Neutral Interpretive Note",
            "",
            "The AI record foregrounds the self-stabbing report with low uncertainty and no alternative pathway. The same packet also includes an unidentified later action involving removal of the small sword. That later removal does not automatically establish that someone else caused the death; self-inflicted death and unresolved later intervention may coexist. TRIM-HAA makes this candidate closure question visible for subsequent independent evaluation without deciding which interpretation is correct.",
            "",
            "## Provenance",
            "",
            f"- Prompt SHA-256: `{prompt_hash}`",
            f"- AI raw output SHA-256: `{ai_output_hash}`",
            "",
        ]
    )


def _summary(
    validation_rows: list[dict[str, str]],
    lock_verified: bool,
    candidate_status: str,
    source_packet_hash: str,
    instruction_set_hash: str,
    prompt_hash: str,
    ai_output_hash: str,
) -> str:
    return "\n".join(
        [
            "# In a Grove Walkthrough Execution Summary",
            "",
            "- Walkthrough type: independent record audit only.",
            "- Human-subject data created: no.",
            "- Human-post records created: no.",
            "- Control records created: no.",
            f"- Validation issue count: {len(validation_rows)}",
            f"- Author lock verified: {lock_verified}",
            f"- Review question display status: `{candidate_status}`",
            "- `candidate_visible` means the configured author-defined review rule was triggered; it is not an independently validated mismatch.",
            "- Walkthrough result: structured disagreement across final label, selected evidence, mechanism, uncertainty, and alternative handling.",
            "- Procedural finding: IAG-SAM-012 was present in the packet and the prompt required explicit alternative assessment; whether the segment warranted retaining an alternative remains open.",
            f"- Source packet SHA-256: `{source_packet_hash}`",
            f"- Instruction-set SHA-256: `{instruction_set_hash}`",
            f"- Prompt SHA-256: `{prompt_hash}`",
            f"- AI raw output SHA-256: `{ai_output_hash}`",
            "",
        ]
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
