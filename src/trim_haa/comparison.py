"""Descriptive pre/AI/post comparison utilities for TRIM-HAA."""

from __future__ import annotations

import unicodedata
from collections import Counter
from typing import Any, Callable, Mapping

from trim_haa.schema import TrimHAAAnnotation, clean_text, coerce_segment_ids


def coerce_annotation(record: TrimHAAAnnotation | Mapping[str, Any]) -> TrimHAAAnnotation:
    if isinstance(record, TrimHAAAnnotation):
        return record
    return TrimHAAAnnotation.from_record(record)


def segment_set_metrics(left: Any, right: Any) -> dict[str, bool | float]:
    left_set = set(coerce_segment_ids(left))
    right_set = set(coerce_segment_ids(right))
    if not left_set and not right_set:
        return {
            "exact_match": True,
            "jaccard": 1.0,
            "intersection_count": 0,
            "union_count": 0,
        }
    intersection = left_set & right_set
    union = left_set | right_set
    return {
        "exact_match": left_set == right_set,
        "jaccard": len(intersection) / len(union) if union else 1.0,
        "intersection_count": len(intersection),
        "union_count": len(union),
    }


def label_change(pre: Any, ai: Any, post: Any) -> dict[str, Any]:
    pre = coerce_annotation(pre)
    ai = coerce_annotation(ai)
    post = coerce_annotation(post)
    return {
        "pre_label": pre.function_label,
        "ai_label": ai.function_label,
        "post_label": post.function_label,
        "label_changed": pre.function_label != post.function_label,
        "label_adopted_from_ai": (
            pre.function_label != ai.function_label
            and post.function_label == ai.function_label
        ),
    }


def evidence_comparison(pre: Any, ai: Any, post: Any) -> dict[str, Any]:
    pre = coerce_annotation(pre)
    ai = coerce_annotation(ai)
    post = coerce_annotation(post)
    pre_set = set(pre.primary_evidence_segment_ids)
    ai_set = set(ai.primary_evidence_segment_ids)
    post_set = set(post.primary_evidence_segment_ids)
    pre_ai = segment_set_metrics(pre_set, ai_set)
    pre_post = segment_set_metrics(pre_set, post_set)
    post_ai = segment_set_metrics(post_set, ai_set)
    evidence_added = sorted(post_set - pre_set)
    evidence_removed = sorted(pre_set - post_set)
    incorporated_ai_segments = sorted((post_set - pre_set) & ai_set)
    removed_pre_segments = sorted(pre_set - post_set)
    retained_pre_segments = sorted(pre_set & post_set)
    new_non_ai_segments = sorted((post_set - pre_set) - ai_set)
    evidence_convergence_increased = post_ai["jaccard"] > pre_ai["jaccard"]
    return {
        "pre_ai_primary_exact_match": pre_ai["exact_match"],
        "pre_ai_primary_jaccard": pre_ai["jaccard"],
        "pre_post_primary_exact_match": pre_post["exact_match"],
        "pre_post_primary_jaccard": pre_post["jaccard"],
        "post_ai_primary_exact_match": post_ai["exact_match"],
        "post_ai_primary_jaccard": post_ai["jaccard"],
        "evidence_added": "|".join(evidence_added),
        "evidence_removed": "|".join(evidence_removed),
        "evidence_adopted_from_ai": "|".join(incorporated_ai_segments),
        "incorporated_ai_segments": "|".join(incorporated_ai_segments),
        "removed_pre_segments": "|".join(removed_pre_segments),
        "retained_pre_segments": "|".join(retained_pre_segments),
        "new_non_ai_segments": "|".join(new_non_ai_segments),
        "ai_evidence_incorporated": bool(incorporated_ai_segments),
        "evidence_convergence_increased": evidence_convergence_increased,
        "evidence_adoption": bool(incorporated_ai_segments)
        and evidence_convergence_increased,
        "evidential_displacement": bool(removed_pre_segments)
        and bool(incorporated_ai_segments),
    }


def mechanism_comparison(pre: Any, ai: Any, post: Any) -> dict[str, Any]:
    pre = coerce_annotation(pre)
    ai = coerce_annotation(ai)
    post = coerce_annotation(post)
    return {
        "pre_mechanism": pre.rationale_mechanism,
        "ai_mechanism": ai.rationale_mechanism,
        "post_mechanism": post.rationale_mechanism,
        "mechanism_changed": pre.rationale_mechanism != post.rationale_mechanism,
        "mechanism_adopted_from_ai": (
            pre.rationale_mechanism != ai.rationale_mechanism
            and post.rationale_mechanism == ai.rationale_mechanism
        ),
    }


def uncertainty_comparison(pre: Any, post: Any) -> dict[str, str]:
    pre = coerce_annotation(pre)
    post = coerce_annotation(post)
    rank = {"low": 0, "medium": 1, "high": 2}
    pre_rank = rank.get(pre.uncertainty_flag)
    post_rank = rank.get(post.uncertainty_flag)
    if pre_rank is None or post_rank is None or pre_rank == post_rank:
        direction = "unchanged"
    elif post_rank > pre_rank:
        direction = "increased"
    else:
        direction = "decreased"
    return {
        "pre_uncertainty": pre.uncertainty_flag,
        "post_uncertainty": post.uncertainty_flag,
        "uncertainty_shift": direction,
    }


def alternative_comparison(pre: Any, ai: Any, post: Any) -> dict[str, Any]:
    pre = coerce_annotation(pre)
    ai = coerce_annotation(ai)
    post = coerce_annotation(post)
    note_overlap = normalised_token_overlap(post.alternative_note, ai.alternative_note)
    return {
        "alternative_present_pre": pre.alternative_pathway_present,
        "alternative_present_ai": ai.alternative_pathway_present,
        "alternative_present_post": post.alternative_pathway_present,
        "alternative_suppressed": pre.has_alternative and not post.has_alternative,
        "alternative_generated": not pre.has_alternative and post.has_alternative,
        "alternative_mechanism_changed": (
            pre.alternative_mechanism != post.alternative_mechanism
        ),
        "alternative_mechanism_adopted_from_ai": (
            pre.alternative_mechanism != ai.alternative_mechanism
            and post.alternative_mechanism == ai.alternative_mechanism
            and bool(post.alternative_mechanism)
        ),
        "alternative_note_exact_match_ai": (
            bool(post.alternative_note) and post.alternative_note == ai.alternative_note
        ),
        "alternative_note_token_overlap_ai": note_overlap,
        "alternative_changed_without_suppression": (
            pre.has_alternative
            and post.has_alternative
            and (
                pre.alternative_mechanism != post.alternative_mechanism
                or pre.alternative_note != post.alternative_note
            )
        ),
    }


def normalised_tokens(text: str) -> list[str]:
    """Return dependency-free Unicode lexical units.

    Latin and numeric runs remain word tokens. Characters from scripts that do
    not conventionally use spaces (including Han and kana) become individual
    lexical units so meaningful text cannot collapse to an empty token stream.
    """

    normalised = unicodedata.normalize("NFKC", clean_text(text).casefold())
    tokens: list[str] = []
    word_buffer: list[str] = []

    def flush_word() -> None:
        if word_buffer:
            tokens.append("".join(word_buffer))
            word_buffer.clear()

    for character in normalised:
        category = unicodedata.category(character)
        if category.startswith(("L", "N")) and category != "Lo":
            word_buffer.append(character)
        elif category.startswith("M") and word_buffer:
            word_buffer.append(character)
        elif category == "Lo":
            flush_word()
            tokens.append(character)
        else:
            flush_word()
    flush_word()
    return tokens


def normalised_token_overlap(left: str, right: str) -> float:
    left_text = clean_text(left)
    right_text = clean_text(right)
    left_tokens = Counter(normalised_tokens(left))
    right_tokens = Counter(normalised_tokens(right))
    if not left_tokens and not right_tokens:
        return 1.0 if not left_text and not right_text else 0.0
    if not left_tokens or not right_tokens:
        return 0.0
    intersection = sum((left_tokens & right_tokens).values())
    union = sum((left_tokens | right_tokens).values())
    return intersection / union if union else 0.0


def copied_phrase_overlap(left: str, right: str, n: int = 4) -> float:
    left_tokens = normalised_tokens(left)
    right_tokens = normalised_tokens(right)
    if len(left_tokens) < n or len(right_tokens) < n:
        return 0.0
    left_phrases = set(zip(*(left_tokens[i:] for i in range(n)), strict=False))
    right_phrases = set(zip(*(right_tokens[i:] for i in range(n)), strict=False))
    if not left_phrases or not right_phrases:
        return 0.0
    return len(left_phrases & right_phrases) / len(left_phrases | right_phrases)


def semantic_similarity_stub(left: str, right: str) -> None:
    """Interface placeholder; callers may supply their own embedding model."""

    return None


def rationale_comparison(
    pre_or_post: Any,
    ai: Any,
    *,
    semantic_similarity_fn: Callable[[str, str], float] | None = None,
) -> dict[str, Any]:
    record = coerce_annotation(pre_or_post)
    ai = coerce_annotation(ai)
    semantic_similarity = (
        semantic_similarity_fn(record.rationale_note, ai.rationale_note)
        if semantic_similarity_fn
        else None
    )
    return {
        "exact_text_match": record.rationale_note == ai.rationale_note,
        "normalised_token_overlap": normalised_token_overlap(
            record.rationale_note, ai.rationale_note
        ),
        "copied_phrase_overlap": copied_phrase_overlap(
            record.rationale_note, ai.rationale_note
        ),
        "semantic_similarity": semantic_similarity,
    }


def independent_convergence(
    human_pre: Any,
    ai: Any,
    field: str,
) -> bool:
    human_pre = coerce_annotation(human_pre)
    ai = coerce_annotation(ai)
    return getattr(human_pre, field) == getattr(ai, field)


def exposure_associated_convergence(pre: Any, ai: Any, post: Any, field: str) -> bool:
    pre = coerce_annotation(pre)
    ai = coerce_annotation(ai)
    post = coerce_annotation(post)
    if field == "primary_evidence_segment_ids":
        return (
            segment_set_metrics(post.primary_evidence_segment_ids, ai.primary_evidence_segment_ids)[
                "jaccard"
            ]
            > segment_set_metrics(pre.primary_evidence_segment_ids, ai.primary_evidence_segment_ids)[
                "jaccard"
            ]
        )
    return getattr(pre, field) != getattr(ai, field) and getattr(post, field) == getattr(ai, field)


def pathway_change(pre: Any, ai: Any, post: Any) -> dict[str, Any]:
    label = label_change(pre, ai, post)
    evidence = evidence_comparison(pre, ai, post)
    mechanism = mechanism_comparison(pre, ai, post)
    uncertainty = uncertainty_comparison(pre, post)
    alternative = alternative_comparison(pre, ai, post)
    return {
        "label_changed": label["label_changed"],
        "label_adopted_from_ai": label["label_adopted_from_ai"],
        "primary_evidence_changed": not evidence["pre_post_primary_exact_match"],
        "ai_evidence_incorporated": evidence["ai_evidence_incorporated"],
        "evidence_convergence_increased": evidence["evidence_convergence_increased"],
        "evidence_adoption": evidence["evidence_adoption"],
        "evidential_displacement": evidence["evidential_displacement"],
        "mechanism_changed": mechanism["mechanism_changed"],
        "mechanism_adopted_from_ai": mechanism["mechanism_adopted_from_ai"],
        "uncertainty_shift": uncertainty["uncertainty_shift"],
        "alternative_suppressed": alternative["alternative_suppressed"],
        "alternative_generated": alternative["alternative_generated"],
    }


def compare_annotations(left: Any, right: Any) -> dict[str, Any]:
    """Compare two independent TRIM-HAA annotations without a truth verdict."""

    left = coerce_annotation(left)
    right = coerce_annotation(right)
    evidence = segment_set_metrics(
        left.primary_evidence_segment_ids,
        right.primary_evidence_segment_ids,
    )
    return {
        "left_annotation_id": left.annotation_id,
        "right_annotation_id": right.annotation_id,
        "label": {
            "left": left.function_label,
            "right": right.function_label,
            "match": left.function_label == right.function_label,
        },
        "evidence": {
            "left": "|".join(left.primary_evidence_segment_ids),
            "right": "|".join(right.primary_evidence_segment_ids),
            **evidence,
        },
        "mechanism": {
            "left": left.rationale_mechanism,
            "right": right.rationale_mechanism,
            "match": left.rationale_mechanism == right.rationale_mechanism,
        },
        "uncertainty": {
            "left": left.uncertainty_flag,
            "right": right.uncertainty_flag,
            "match": left.uncertainty_flag == right.uncertainty_flag,
        },
        "alternative": {
            "left_present": left.alternative_pathway_present,
            "right_present": right.alternative_pathway_present,
            "match": (
                left.alternative_pathway_present
                == right.alternative_pathway_present
            ),
            "left_mechanism": left.alternative_mechanism,
            "right_mechanism": right.alternative_mechanism,
        },
        "rationale": rationale_comparison(left, right),
    }


def compare_pre_ai_post(pre: Any, ai: Any, post: Any) -> dict[str, Any]:
    rationale = rationale_comparison(post, ai)
    return {
        **label_change(pre, ai, post),
        **evidence_comparison(pre, ai, post),
        **mechanism_comparison(pre, ai, post),
        **uncertainty_comparison(pre, post),
        **alternative_comparison(pre, ai, post),
        "rationale_overlap": rationale["normalised_token_overlap"],
        "copied_phrase_overlap": rationale["copied_phrase_overlap"],
        **pathway_change(pre, ai, post),
    }


def compare_pre_control(pre: Any, control: Any) -> dict[str, Any]:
    pre = coerce_annotation(pre)
    control = coerce_annotation(control)
    evidence = segment_set_metrics(
        pre.primary_evidence_segment_ids,
        control.primary_evidence_segment_ids,
    )
    return {
        "pre_to_control_label_changed": pre.function_label != control.function_label,
        "pre_to_control_primary_jaccard": evidence["jaccard"],
        "pre_to_control_mechanism_changed": (
            pre.rationale_mechanism != control.rationale_mechanism
        ),
        "pre_to_control_uncertainty_shift": uncertainty_comparison(pre, control)[
            "uncertainty_shift"
        ],
        "pre_to_control_alternative_changed": (
            pre.alternative_pathway_present != control.alternative_pathway_present
        ),
    }


def ai_associated_change_summary(pre: Any, ai: Any, post: Any, control: Any | None = None) -> dict[str, Any]:
    """Return descriptive post-AI change and optional second-pass contrast."""

    post_change = compare_pre_ai_post(pre, ai, post)
    summary = {
        "pre_to_post_ai_change": any(
            bool(post_change[key])
            for key in (
                "label_changed",
                "primary_evidence_changed",
                "mechanism_changed",
                "alternative_suppressed",
                "alternative_generated",
            )
        )
        or post_change["uncertainty_shift"] != "unchanged",
    }
    if control is not None:
        control_change = compare_pre_control(pre, control)
        summary.update(control_change)
        summary["descriptive_ai_associated_label_change_minus_control"] = (
            int(bool(post_change["label_changed"]))
            - int(bool(control_change["pre_to_control_label_changed"]))
        )
    return summary
