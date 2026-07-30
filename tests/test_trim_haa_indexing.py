import ast
import hashlib
from pathlib import Path

import pytest

import trim_haa
from trim_haa import (
    STRICT_INDEXING_API_VERSION,
    DuplicateIdentifierError,
    IdentifierIndexError,
    InvalidIdentifierError,
    strict_annotation_index,
)
from trim_haa.provenance import annotation_index
from trim_haa.schema import TrimHAAAnnotation


ROOT = Path(__file__).parents[1]
PROVENANCE_SHA256 = "92e075aa74afd0661fb6446c1253863883b651df735aaec0ec073638af0fdd14"


def _annotation(
    annotation_id="A1",
    *,
    case_id="C1",
    rationale_note="Synthetic rationale.",
):
    return TrimHAAAnnotation(
        annotation_id=annotation_id,
        case_id=case_id,
        actor_id="H01",
        actor_type="human",
        annotation_stage="human_pre",
        primary_evidence_segment_ids="S1",
        function_label="label_a",
        rationale_mechanism="supports",
        uncertainty_flag="medium",
        rationale_note=rationale_note,
        alternative_pathway_present="no",
        status="locked",
    )


def test_strict_index_accepts_one_dataclass_record():
    record = _annotation()

    result = strict_annotation_index([record])

    assert result == {"A1": record}
    assert result["A1"] is record


def test_strict_index_accepts_mappings_and_preserves_insertion_order():
    records = [
        _annotation("A2", case_id="C2").to_record(),
        _annotation("A1", case_id="C1").to_record(),
        _annotation("A3", case_id="C3").to_record(),
    ]

    result = strict_annotation_index(records)

    assert list(result) == ["A2", "A1", "A3"]
    assert all(isinstance(record, TrimHAAAnnotation) for record in result.values())
    assert records[0]["annotation_id"] == "A2"


@pytest.mark.parametrize(
    "records, first_position, second_position",
    [
        ([_annotation("DUP"), _annotation("DUP")], 0, 1),
        (
            [
                _annotation("DUP", rationale_note="First synthetic rationale."),
                _annotation("DUP", rationale_note="Conflicting synthetic rationale."),
            ],
            0,
            1,
        ),
        (
            [_annotation("DUP", case_id="C1"), _annotation("DUP", case_id="C2")],
            0,
            1,
        ),
        ([_annotation("DUP"), _annotation("OTHER"), _annotation("DUP")], 0, 2),
    ],
)
def test_strict_index_rejects_all_duplicate_forms(
    records, first_position, second_position
):
    with pytest.raises(DuplicateIdentifierError) as caught:
        strict_annotation_index(records)

    assert caught.value.identifier_type == "annotation_id"
    assert caught.value.identifier == "DUP"
    assert caught.value.first_position == first_position
    assert caught.value.second_position == second_position


def test_strict_index_rejects_duplicate_from_generator():
    records = (_annotation(identifier) for identifier in ("A1", "A2", "A1"))

    with pytest.raises(DuplicateIdentifierError) as caught:
        strict_annotation_index(records)

    assert (caught.value.first_position, caught.value.second_position) == (0, 2)


@pytest.mark.parametrize(
    "record",
    [
        _annotation(""),
        _annotation("   "),
        {"case_id": "C-MISSING"},
    ],
)
def test_strict_index_rejects_empty_whitespace_and_missing_ids(record):
    with pytest.raises(InvalidIdentifierError) as caught:
        strict_annotation_index([record])

    assert caught.value.identifier_type == "annotation_id"
    assert caught.value.position == 0


def test_exceptions_are_structured_and_do_not_expose_record_content():
    secret_rationale = "DO_NOT_EXPOSE_SYNTHETIC_RATIONALE"
    records = [
        _annotation("DUP", case_id="C-FIRST", rationale_note=secret_rationale),
        _annotation("DUP", case_id="C-SECOND", rationale_note=secret_rationale),
    ]

    with pytest.raises(DuplicateIdentifierError) as caught:
        strict_annotation_index(records)

    error = caught.value
    assert isinstance(error, IdentifierIndexError)
    assert error.first_case_id == "C-FIRST"
    assert error.second_case_id == "C-SECOND"
    assert "DUP" in str(error)
    assert "0" in str(error) and "1" in str(error)
    assert "C-FIRST" in str(error) and "C-SECOND" in str(error)
    assert secret_rationale not in str(error)
    assert secret_rationale not in repr(vars(error))


def test_legacy_and_strict_duplicate_behavior_differ_only_as_documented():
    first = _annotation("DUP", rationale_note="First.")
    second = _annotation("DUP", rationale_note="Second.")

    assert annotation_index([first, second])["DUP"] is second
    with pytest.raises(DuplicateIdentifierError):
        strict_annotation_index([first, second])


def test_frozen_legacy_source_hash_remains_exact():
    digest = hashlib.sha256(
        (ROOT / "src" / "trim_haa" / "provenance.py").read_bytes()
    ).hexdigest()

    assert digest == PROVENANCE_SHA256


def test_strict_api_is_public_without_removing_existing_exports():
    assert STRICT_INDEXING_API_VERSION == "1"
    assert trim_haa.strict_annotation_index is strict_annotation_index
    assert trim_haa.DuplicateIdentifierError is DuplicateIdentifierError
    for existing_name in (
        "AssistanceProvenance",
        "LockRecord",
        "TrimHAAAnnotation",
        "ValidationIssue",
        "ValidationReport",
        "compare_annotations",
        "lock_annotation",
        "validate_core_record",
        "validate_core_records",
        "validate_dataset",
        "validate_provenance_record",
        "verify_locked_annotation",
    ):
        assert existing_name in trim_haa.__all__


def test_active_nonfrozen_modules_do_not_import_or_call_legacy_index():
    violations = []
    source_root = ROOT / "src" / "trim_haa"
    for path in sorted(source_root.glob("*.py")):
        if path.name == "provenance.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "trim_haa.provenance":
                if any(alias.name == "annotation_index" for alias in node.names):
                    violations.append(f"{path.name}:{node.lineno}:legacy import")
            if isinstance(node, ast.Call):
                function = node.func
                if isinstance(function, ast.Name) and function.id == "annotation_index":
                    violations.append(f"{path.name}:{node.lineno}:legacy call")
                if isinstance(function, ast.Attribute) and function.attr == "annotation_index":
                    violations.append(f"{path.name}:{node.lineno}:legacy attribute call")

    assert violations == []
