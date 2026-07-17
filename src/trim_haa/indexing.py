"""Fail-closed indexing APIs for new TRIM-HAA development."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from trim_haa.schema import TrimHAAAnnotation

STRICT_INDEXING_API_VERSION = "1"


class IdentifierIndexError(ValueError):
    """Base exception for invalid identifiers in strict indexes."""


class InvalidIdentifierError(IdentifierIndexError):
    """Raised when a record has no usable identifier."""

    def __init__(
        self,
        *,
        identifier_type: str,
        position: int,
        case_id: str,
    ) -> None:
        self.identifier_type = identifier_type
        self.position = position
        self.case_id = case_id
        super().__init__(
            f"{identifier_type} must be non-empty at position {position} "
            f"(case_id={case_id!r})."
        )


class DuplicateIdentifierError(IdentifierIndexError):
    """Raised when strict indexing encounters the same identifier twice."""

    def __init__(
        self,
        *,
        identifier_type: str,
        identifier: str,
        first_position: int,
        second_position: int,
        first_case_id: str,
        second_case_id: str,
    ) -> None:
        self.identifier_type = identifier_type
        self.identifier = identifier
        self.first_position = first_position
        self.second_position = second_position
        self.first_case_id = first_case_id
        self.second_case_id = second_case_id
        super().__init__(
            f"Duplicate {identifier_type} {identifier!r} at positions "
            f"{first_position} and {second_position} "
            f"(case_ids {first_case_id!r} and {second_case_id!r})."
        )


def strict_annotation_index(
    records: Iterable[TrimHAAAnnotation | Mapping[str, Any]],
) -> dict[str, TrimHAAAnnotation]:
    """Index annotations in input order and reject empty or duplicate IDs.

    Positions in structured exceptions are zero-based input positions. Exception
    state includes identifiers and case IDs only; full annotation content is
    deliberately excluded.
    """

    index: dict[str, TrimHAAAnnotation] = {}
    positions: dict[str, int] = {}
    for position, record in enumerate(records):
        annotation = (
            record
            if isinstance(record, TrimHAAAnnotation)
            else TrimHAAAnnotation.from_record(record)
        )
        identifier = annotation.annotation_id
        if not identifier:
            raise InvalidIdentifierError(
                identifier_type="annotation_id",
                position=position,
                case_id=annotation.case_id,
            )
        if identifier in index:
            first = index[identifier]
            raise DuplicateIdentifierError(
                identifier_type="annotation_id",
                identifier=identifier,
                first_position=positions[identifier],
                second_position=position,
                first_case_id=first.case_id,
                second_case_id=annotation.case_id,
            )
        index[identifier] = annotation
        positions[identifier] = position
    return index


__all__ = [
    "STRICT_INDEXING_API_VERSION",
    "DuplicateIdentifierError",
    "IdentifierIndexError",
    "InvalidIdentifierError",
    "strict_annotation_index",
]
