"""Metadata-only disagreement comparison for synthetic annotation payloads."""

from __future__ import annotations

from typing import Any

from trim_haa.llm.hashing import canonical_json_bytes, sha256_bytes


EXCLUDED_AUTOMATED_FIELDS = {
    "actor_type",
    "analyst_id_pseudonym",
    "analyst_role",
    "case_id",
    "coding_session_id",
    "coder_comments",
    "exposure_status",
    "free_text_rationale",
    "manual_version",
    "notes",
    "record_id",
    "record_type",
    "review_of_record_hash",
    "review_of_record_id",
    "self_record_status",
    "source_packet_hash",
    "timestamp",
    "unresolved_ambiguity",
}


def _is_missing(value: Any) -> bool:
    return value is None or value == "" or value == []


def _supported_categories(payload: dict[str, Any]) -> tuple[str, ...]:
    return tuple(
        sorted(
            item.get("category")
            for item in payload.get("candidate_loci", [])
            if isinstance(item, dict) and item.get("state") == "candidate_supported" and item.get("category")
        )
    )


def _confidence_signature(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "uncertainty": payload.get("uncertainty"),
        "candidate_confidence": {
            item.get("category"): item.get("confidence")
            for item in payload.get("candidate_loci", [])
            if isinstance(item, dict) and item.get("category")
        },
    }


def compare_annotations(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare payload structure without copying source-facing values or coder comments."""

    if len(payloads) < 2:
        raise ValueError("at least two annotation payloads are required")
    included_fields = sorted(set().union(*(payload.keys() for payload in payloads)) - EXCLUDED_AUTOMATED_FIELDS - {"record_hash"})
    field_disagreements = [
        field
        for field in included_fields
        if len({canonical_json_bytes(payload.get(field)) for payload in payloads}) > 1
    ]
    missing_value_disagreements = [
        field
        for field in included_fields
        if len({_is_missing(payload.get(field)) for payload in payloads}) > 1
    ]
    category_sets = [_supported_categories(payload) for payload in payloads]
    category_set_agreement = len(set(category_sets)) == 1
    selected_sets = [set(payload.get("selected_evidence", [])) for payload in payloads]
    union = set().union(*selected_sets)
    intersection = set.intersection(*selected_sets) if selected_sets else set()
    confidence_signatures = [_confidence_signature(payload) for payload in payloads]
    confidence_disagreement = len({canonical_json_bytes(value) for value in confidence_signatures}) > 1
    summary: dict[str, Any] = {
        "record_count": len(payloads),
        "exact_agreement": not field_disagreements,
        "field_disagreements": field_disagreements,
        "missing_value_disagreements": missing_value_disagreements,
        "category_set_agreement": category_set_agreement,
        "category_sets": [list(value) for value in category_sets],
        "multi_label_overlap": {
            "field": "selected_evidence",
            "intersection_count": len(intersection),
            "union_count": len(union),
            "exact_set_agreement": len({tuple(sorted(value)) for value in selected_sets}) == 1,
        },
        "confidence_disagreement": confidence_disagreement,
        "excluded_fields": sorted(EXCLUDED_AUTOMATED_FIELDS),
        "adjudication_required": bool(field_disagreements or not category_set_agreement or confidence_disagreement),
    }
    summary["disagreement_summary_hash"] = sha256_bytes(canonical_json_bytes(summary))
    return summary
