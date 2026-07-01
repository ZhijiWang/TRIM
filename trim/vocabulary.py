"""Controlled vocabularies for TRIM annotations."""

from __future__ import annotations

from typing import Iterable


FUNCTION_LABELS: frozenset[str] = frozenset(
    {
        "immediate_stabilization",
        "extended_deliberation",
        "ambition_trigger_authorization",
        "false_security",
        "retrospective_trap",
        "self_justification",
        "self_defence_self_accusation",
        "epistemic_suspension",
        "no_fit",
    }
)

FRICTION_LOCI: frozenset[str] = frozenset(
    {
        "cue_function",
        "warrant_attribution",
        "warrant_relation",
        "operation_function",
        "boundary_setting",
        "temporal_layering",
        "perspective_assignment",
        "context_inference",
    }
)

RATIONALE_MECHANISMS: frozenset[str] = frozenset(
    {
        "supports",
        "contradicts",
        "overrides",
        "qualifies",
        "reframes",
        "stabilizes",
        "extends",
        "reactivates",
        "suspends",
        "projects",
        "authorizes",
        "narrows",
    }
)

EPISTEMIC_SUPPORT_VALUES: frozenset[str] = frozenset(
    {
        "textual_anchor",
        "internal_sequence",
        "ritual_sequence",
        "narrative_context",
        "scholarly_apparatus",
        "parallel_case",
        "metadata_context",
        "external_historical_context",
        "coder_inference",
    }
)

DISCOURSE_LEVELS: frozenset[str] = frozenset(
    {
        "intradiegetic",
        "extradiegetic",
        "frame_narrative",
        "dramatic_present",
        "reported_speech",
        "commentarial_discourse",
    }
)

TEMPORAL_ORIENTATIONS: frozenset[str] = frozenset(
    {
        "prospective",
        "immediate",
        "retrospective",
        "recursive",
        "suspended",
        "prospective-retrospective",
    }
)

UNCERTAINTY_FLAGS: frozenset[str] = frozenset({"low", "medium", "high"})

LANGUAGE_ACCESS_MODES: frozenset[str] = frozenset(
    {
        "direct_original_language_access",
        "published_translation",
        "project_authored_close_support",
        "summary_mediated",
        "mixed",
    }
)

CASE_SCOPES: frozenset[str] = frozenset(
    {
        "local_passage",
        "multi_passage_single_case",
        "complete_work",
        "supplied_related_cases",
        "shared_narrative_field",
    }
)

YES_NO_VALUES: frozenset[str] = frozenset({"yes", "no"})

QUESTION_TYPES: frozenset[str] = frozenset(
    {
        "definitional",
        "interpretive",
        "procedural",
        "packet_level",
        "other",
    }
)

QUESTION_STATUS_VALUES: frozenset[str] = frozenset({"blocking", "nonblocking"})

QUESTION_REVISION_VALUES: frozenset[str] = frozenset({"yes", "no", "uncertain"})

DISAGREEMENT_CATEGORIES: frozenset[str] = frozenset(
    {
        "raw_disagreement",
        "compatible_difference",
        "codebook_ambiguity",
        "substantive_pathway_variation",
        "insufficient_evidence",
        "coder_error",
        "unresolved_legitimate_alternatives",
        "near_complete_alignment",
    }
)

CONTROLLED_VOCABULARIES: dict[str, frozenset[str]] = {
    "function_label": FUNCTION_LABELS,
    "friction_locus": FRICTION_LOCI,
    "rationale_mechanism": RATIONALE_MECHANISMS,
    "epistemic_support": EPISTEMIC_SUPPORT_VALUES,
    "discourse_level": DISCOURSE_LEVELS,
    "temporal_orientation": TEMPORAL_ORIENTATIONS,
    "uncertainty_flag": UNCERTAINTY_FLAGS,
    "language_access_mode": LANGUAGE_ACCESS_MODES,
    "case_scope": CASE_SCOPES,
    "cross_case_context_permitted": YES_NO_VALUES,
    "did_question_change_code": YES_NO_VALUES,
    "blocking_or_nonblocking": QUESTION_STATUS_VALUES,
    "requires_manual_revision": QUESTION_REVISION_VALUES,
    "question_type": QUESTION_TYPES,
    "disagreement_category": DISAGREEMENT_CATEGORIES,
}

COMPOUND_FIELDS: frozenset[str] = frozenset(
    {"rationale_mechanism", "epistemic_support"}
)


def allowed_values(field_name: str) -> tuple[str, ...]:
    """Return sorted allowed values for a controlled field."""

    return tuple(sorted(CONTROLLED_VOCABULARIES[field_name]))


def split_compound_value(value: str, separator: str = "+") -> tuple[str, ...]:
    """Split a controlled compound value without interpreting it."""

    return tuple(part.strip() for part in str(value).split(separator))


def validate_closed_value(
    field_name: str,
    value: str,
    allowed: Iterable[str],
) -> list[str]:
    """Validate a single closed-vocabulary value."""

    text = str(value).strip()
    allowed_set = set(allowed)
    if not text:
        return [f"{field_name} is required."]
    if text not in allowed_set:
        return [
            f"{field_name} value {text!r} is not controlled vocabulary. "
            f"Allowed values: {', '.join(sorted(allowed_set))}."
        ]
    return []


def validate_compound_value(
    field_name: str,
    value: str,
    allowed: Iterable[str],
    max_parts: int = 2,
) -> list[str]:
    """Validate a one- or two-part controlled value joined by ``+``."""

    text = str(value).strip()
    allowed_set = set(allowed)
    if not text:
        return [f"{field_name} is required."]

    parts = split_compound_value(text)
    errors: list[str] = []
    if any(not part for part in parts):
        errors.append(f"{field_name} contains an empty compound value.")
    if len(parts) > max_parts:
        errors.append(
            f"{field_name} contains {len(parts)} values; no more than "
            f"{max_parts} are allowed."
        )

    seen: set[str] = set()
    for part in parts:
        if not part:
            continue
        if part in seen:
            errors.append(
                f"{field_name} contains duplicate compound value {part!r}."
            )
        seen.add(part)
        if part not in allowed_set:
            errors.append(
                f"{field_name} value {part!r} is not controlled vocabulary. "
                f"Allowed values: {', '.join(sorted(allowed_set))}."
            )
    return errors
