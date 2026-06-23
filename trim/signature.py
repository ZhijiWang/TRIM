"""Friction signature parsing and comparison utilities."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from trim.schema import TrimAnnotation
from trim.vocabulary import (
    COMPOUND_FIELDS,
    CONTROLLED_VOCABULARIES,
    validate_closed_value,
    validate_compound_value,
)


SIGNATURE_FIELDS: tuple[str, ...] = (
    "friction_locus",
    "rationale_mechanism",
    "epistemic_support",
    "discourse_level",
    "temporal_orientation",
    "uncertainty_flag",
)

FIELD_ALIASES: dict[str, str] = {
    "locus": "friction_locus",
    "friction": "friction_locus",
    "friction_locus": "friction_locus",
    "mechanism": "rationale_mechanism",
    "rationale": "rationale_mechanism",
    "rationale_mechanism": "rationale_mechanism",
    "support": "epistemic_support",
    "epistemic": "epistemic_support",
    "epistemic_support": "epistemic_support",
    "level": "discourse_level",
    "discourse": "discourse_level",
    "discourse_level": "discourse_level",
    "temporal": "temporal_orientation",
    "temporal_orientation": "temporal_orientation",
    "uncertainty": "uncertainty_flag",
    "uncertainty_flag": "uncertainty_flag",
}


@dataclass(frozen=True, slots=True)
class FrictionSignature:
    """The six controlled fields that make a TRIM friction signature."""

    friction_locus: str
    rationale_mechanism: str
    epistemic_support: str
    discourse_level: str
    temporal_orientation: str
    uncertainty_flag: str

    @classmethod
    def from_annotation(
        cls,
        annotation: TrimAnnotation | Mapping[str, Any],
    ) -> "FrictionSignature":
        if not isinstance(annotation, TrimAnnotation):
            annotation = TrimAnnotation.from_record(annotation)
        return cls(
            friction_locus=annotation.friction_locus,
            rationale_mechanism=annotation.rationale_mechanism,
            epistemic_support=annotation.epistemic_support,
            discourse_level=annotation.discourse_level,
            temporal_orientation=annotation.temporal_orientation,
            uncertainty_flag=annotation.uncertainty_flag,
        )

    @classmethod
    def parse(cls, text: str) -> "FrictionSignature":
        return parse_signature(text)

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def to_compact(self, separator: str = " / ") -> str:
        return separator.join(getattr(self, field_name) for field_name in SIGNATURE_FIELDS)

    def validate(self) -> list[str]:
        return [
            message
            for messages in validate_signature_values(self.to_dict()).values()
            for message in messages
        ]


def validate_signature_values(
    values: Mapping[str, Any],
    *,
    include_required: bool = True,
) -> dict[str, list[str]]:
    """Validate six signature fields through the canonical vocabulary helpers."""

    errors_by_field: dict[str, list[str]] = {}
    for field_name in SIGNATURE_FIELDS:
        value = _clean_value(values.get(field_name, ""))
        if not value and not include_required:
            continue

        if field_name in COMPOUND_FIELDS:
            errors = validate_compound_value(
                field_name,
                value,
                CONTROLLED_VOCABULARIES[field_name],
            )
        else:
            errors = validate_closed_value(
                field_name,
                value,
                CONTROLLED_VOCABULARIES[field_name],
            )
        if errors:
            errors_by_field[field_name] = errors
    return errors_by_field


def parse_signature(text: str) -> FrictionSignature:
    """Parse a named or compact friction signature string.

    Named form:
    ``friction_locus=...; rationale_mechanism=...; ...``

    Compact form:
    ``friction_locus / rationale_mechanism / epistemic_support / ...``
    """

    raw = str(text).strip()
    if not raw:
        raise ValueError("Signature text is empty.")

    if _looks_like_named_signature(raw):
        return _parse_named_signature(raw)
    return _parse_compact_signature(raw)


def signature_from_annotation(
    annotation: TrimAnnotation | Mapping[str, Any],
) -> FrictionSignature:
    return FrictionSignature.from_annotation(annotation)


def compare_annotations(
    left: TrimAnnotation | Mapping[str, Any] | FrictionSignature | str,
    right: TrimAnnotation | Mapping[str, Any] | FrictionSignature | str,
) -> dict[str, dict[str, str | bool]]:
    """Compare two human-coded friction signatures field by field."""

    left_signature = _coerce_signature(left)
    right_signature = _coerce_signature(right)
    return {
        field_name: {
            "left": getattr(left_signature, field_name),
            "right": getattr(right_signature, field_name),
            "match": getattr(left_signature, field_name)
            == getattr(right_signature, field_name),
        }
        for field_name in SIGNATURE_FIELDS
    }


def _coerce_signature(
    value: TrimAnnotation | Mapping[str, Any] | FrictionSignature | str,
) -> FrictionSignature:
    if isinstance(value, FrictionSignature):
        return value
    if isinstance(value, str):
        return parse_signature(value)
    return FrictionSignature.from_annotation(value)


def _looks_like_named_signature(text: str) -> bool:
    if "=" in text:
        return True
    lowered = text.lower()
    return any(f"{alias}:" in lowered for alias in FIELD_ALIASES)


def _parse_named_signature(text: str) -> FrictionSignature:
    pieces = re.split(r"\s*[;,]\s*", text)
    values: dict[str, str] = {}
    for piece in pieces:
        if not piece:
            continue
        if "=" in piece:
            raw_key, raw_value = piece.split("=", 1)
        elif ":" in piece:
            raw_key, raw_value = piece.split(":", 1)
        else:
            raise ValueError(f"Signature segment {piece!r} is not a key-value pair.")

        key = raw_key.strip().lower()
        field_name = FIELD_ALIASES.get(key)
        if field_name is None:
            raise ValueError(f"Unknown signature field {raw_key.strip()!r}.")
        values[field_name] = raw_value.strip()

    missing = [field_name for field_name in SIGNATURE_FIELDS if field_name not in values]
    if missing:
        raise ValueError(f"Signature is missing fields: {', '.join(missing)}.")
    return FrictionSignature(**{field_name: values[field_name] for field_name in SIGNATURE_FIELDS})


def _parse_compact_signature(text: str) -> FrictionSignature:
    if "/" in text:
        parts = [part.strip() for part in text.split("/")]
    elif "|" in text:
        parts = [part.strip() for part in text.split("|")]
    elif "::" in text:
        parts = [part.strip() for part in text.split("::")]
    elif ":" in text:
        parts = [part.strip() for part in text.split(":")]
    else:
        raise ValueError(
            "Compact signatures must separate the six signature fields with "
            "'/', '|', '::', or ':'."
        )

    if len(parts) != len(SIGNATURE_FIELDS):
        raise ValueError(
            f"Compact signatures require {len(SIGNATURE_FIELDS)} fields; "
            f"found {len(parts)}."
        )
    if any(not part for part in parts):
        raise ValueError("Compact signature contains an empty field.")
    return FrictionSignature(**dict(zip(SIGNATURE_FIELDS, parts, strict=True)))


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
