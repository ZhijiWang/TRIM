"""TRIM-HAA: provenance-aware human-AI annotation audit tools."""

from trim_haa.comparison import compare_annotations
from trim_haa.locking import (
    LockRecord,
    lock_annotation,
    verify_locked_annotation,
)
from trim_haa.provenance import AssistanceProvenance
from trim_haa.schema import TrimHAAAnnotation
from trim_haa.validator import (
    ValidationIssue,
    ValidationReport,
    validate_core_record,
    validate_core_records,
    validate_dataset,
    validate_provenance_record,
)

__version__ = "0.3.0a1"

__all__ = [
    "__version__",
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
]
