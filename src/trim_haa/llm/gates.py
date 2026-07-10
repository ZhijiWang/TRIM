"""Normalize pilot gate records and fail closed before restricted activity."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RIGHTS_PREPARATION_STATUSES = {
    "PASSED",
    "PASSED_WITH_DOWNSTREAM_GATES_BLOCKED",
}
PRIVATE_PACKET_PREPARATION_STATUSES = {
    "PASSED",
    "PASSED_WITH_CONTROLLED_ACCESS_ONLY",
}
EXECUTION_GATE_NAMES = (
    "provider_model_account",
    "runtime_settings",
    "pricing",
    "final_authorization",
    "human_coding",
    "model_execution",
)
BLOCKER_LABELS = {
    "provider_model_account": "provider/model/account account availability",
    "runtime_settings": "runtime settings",
    "pricing": "pricing",
    "final_authorization": "final authorization",
    "human_coding": "human coding",
    "model_execution": "model execution",
}


class GateBlockedError(RuntimeError):
    """Raised when a requested activity is not authorized by the gate snapshot."""


@dataclass(frozen=True)
class GateDecision:
    """Normalized, metadata-only decision derived from the public gate manifest."""

    statuses: dict[str, str]
    preparation_allowed: bool
    execution_allowed: bool
    decision: str
    blockers: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "statuses": dict(sorted(self.statuses.items())),
            "preparation_allowed": self.preparation_allowed,
            "execution_allowed": self.execution_allowed,
            "decision": self.decision,
            "blockers": list(self.blockers),
        }


def normalize_gate_manifest(manifest: dict[str, Any]) -> GateDecision:
    """Convert gate statuses into preparation and execution decisions."""

    entries = manifest.get("gates")
    if not isinstance(entries, list):
        raise ValueError("gate manifest requires a gates list")
    statuses = {
        str(entry.get("gate")): str(entry.get("status"))
        for entry in entries
        if isinstance(entry, dict) and entry.get("gate")
    }
    rights_ready = statuses.get("rights_evidence") in RIGHTS_PREPARATION_STATUSES
    packets_ready = statuses.get("controlled_private_packet_handling") in PRIVATE_PACKET_PREPARATION_STATUSES
    preparation_allowed = rights_ready and packets_ready
    blockers = tuple(
        BLOCKER_LABELS[name]
        for name in EXECUTION_GATE_NAMES
        if statuses.get(name) != "PASSED"
    )
    execution_allowed = preparation_allowed and not blockers
    return GateDecision(
        statuses=statuses,
        preparation_allowed=preparation_allowed,
        execution_allowed=execution_allowed,
        decision="EXECUTION_ALLOWED" if execution_allowed else "EXECUTION_BLOCKED",
        blockers=blockers,
    )


def load_gate_decision(path: str | Path) -> GateDecision:
    with Path(path).open(encoding="utf-8") as handle:
        return normalize_gate_manifest(json.load(handle))


def assert_human_coding_allowed(decision: GateDecision) -> None:
    if decision.statuses.get("human_coding") != "PASSED":
        raise GateBlockedError("human coding gate is not PASSED")
    if not decision.preparation_allowed:
        raise GateBlockedError("rights/private-packet preparation gates are not sufficient")


def assert_model_execution_allowed(decision: GateDecision) -> None:
    if not decision.execution_allowed:
        detail = ", ".join(decision.blockers) or "preparation gates"
        raise GateBlockedError(f"model execution is blocked: {detail}")
