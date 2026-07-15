"""Self-contained tests shipped with the core-only Python sdist."""

from __future__ import annotations

import csv
import json
import subprocess
import sys

from trim_haa import (
    TrimHAAAnnotation,
    compare_annotations,
    lock_annotation,
    validate_core_record,
    verify_locked_annotation,
)
from trim_haa.locking import LOCK_MANIFEST_FIELDS
from trim_haa.schema import CORE_FIELDS


def _annotation(*, annotation_id: str, actor_id: str, actor_type: str, stage: str) -> TrimHAAAnnotation:
    return TrimHAAAnnotation(
        annotation_id=annotation_id,
        case_id="SDIST_SYNTHETIC_CASE",
        actor_id=actor_id,
        actor_type=actor_type,
        annotation_stage=stage,
        primary_evidence_segment_ids=("SYNTHETIC_SEGMENT",),
        function_label="synthetic_label",
        rationale_mechanism="synthetic_mechanism",
        uncertainty_flag="medium",
        rationale_note="Invented non-source text for a distribution smoke test.",
        alternative_pathway_present="no",
        status="locked",
    )


def test_core_record_lock_and_comparison_round_trip():
    human = _annotation(
        annotation_id="SDIST_HUMAN",
        actor_id="SYNTHETIC_HUMAN",
        actor_type="human",
        stage="human_pre",
    )
    model = _annotation(
        annotation_id="SDIST_MODEL",
        actor_id="SYNTHETIC_MODEL",
        actor_type="model",
        stage="ai_independent",
    )

    assert validate_core_record(human) == []
    lock = lock_annotation(
        human,
        lock_manifest_id="SDIST_LOCK",
        locked_at="2026-01-01T00:00:00Z",
        locked_by="sdist-test",
    )
    assert verify_locked_annotation(human, lock)
    assert compare_annotations(human, model)["label"]["match"] is True


def test_module_cli_works_with_self_contained_records(tmp_path):
    human = _annotation(
        annotation_id="SDIST_CLI_HUMAN",
        actor_id="SYNTHETIC_HUMAN",
        actor_type="human",
        stage="human_pre",
    )
    model = _annotation(
        annotation_id="SDIST_CLI_MODEL",
        actor_id="SYNTHETIC_MODEL",
        actor_type="model",
        stage="ai_independent",
    )
    lock = lock_annotation(
        human,
        lock_manifest_id="SDIST_CLI_LOCK",
        locked_at="2026-01-01T00:00:00Z",
        locked_by="sdist-test",
    )
    human_path = tmp_path / "human.csv"
    model_path = tmp_path / "model.csv"
    lock_path = tmp_path / "lock.csv"
    for path, record, fields in (
        (human_path, human.to_csv_record(), CORE_FIELDS),
        (model_path, model.to_csv_record(), CORE_FIELDS),
        (lock_path, lock.to_record(), LOCK_MANIFEST_FIELDS),
    ):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerow(record)

    for arguments in (
        ("version",),
        ("validate", str(human_path)),
        ("verify-lock", str(human_path), str(lock_path)),
    ):
        result = subprocess.run(
            [sys.executable, "-m", "trim_haa", *arguments],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        assert result.returncode == 0, result.stderr

    compared = subprocess.run(
        [sys.executable, "-m", "trim_haa", "compare", str(human_path), str(model_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert compared.returncode == 0, compared.stderr
    assert json.loads(compared.stdout)["label"]["match"] is True
