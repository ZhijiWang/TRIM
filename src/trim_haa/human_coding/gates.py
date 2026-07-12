"""Human-coding-specific authorization checks with no provider dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from trim_haa.llm.gates import PRIVATE_PACKET_PREPARATION_STATUSES, RIGHTS_PREPARATION_STATUSES


class HumanCodingBlockedError(RuntimeError):
    """Raised before any coding session when a human-coding precondition is absent."""


@dataclass(frozen=True)
class HumanCodingGateDecision:
    decision: str
    preparation_gates_sufficient: bool
    coding_allowed: bool
    blockers: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "preparation_gates_sufficient": self.preparation_gates_sufficient,
            "coding_allowed": self.coding_allowed,
            "blockers": list(self.blockers),
        }


def evaluate_human_coding_gate(
    *,
    rights_gate_status: str,
    private_packet_gate_status: str,
    packet_hash_verification_status: str,
    coding_environment_verified: bool,
    coder_eligible: bool,
    coder_training_status: str,
    coder_authorization_status: str,
    session_authorization_status: str,
    packet_access_authorization_reference: str | None,
    final_authorization_status: str,
    human_coding_gate_status: str,
    record_locking_ready: bool,
) -> HumanCodingGateDecision:
    """Evaluate only direct human-coding prerequisites from public metadata."""

    blockers: list[str] = []
    rights_ready = rights_gate_status in RIGHTS_PREPARATION_STATUSES
    packets_ready = private_packet_gate_status in PRIVATE_PACKET_PREPARATION_STATUSES
    if not rights_ready:
        blockers.append("rights evidence preparation gate insufficient")
    if not packets_ready:
        blockers.append("controlled private-packet preparation gate insufficient")
    if not coding_environment_verified:
        blockers.append("coding environment unverified")
    if not coder_eligible:
        blockers.append("coder eligibility false")
    if coder_training_status != "PASSED_DOCUMENTED":
        blockers.append("coder training incomplete")
    if coder_authorization_status != "PASSED":
        blockers.append("coder authorization absent")
    if session_authorization_status != "PASSED" or packet_access_authorization_reference in {
        None,
        "",
        "synthetic_not_authorized",
    }:
        blockers.append("session authorization absent")
    if packet_hash_verification_status != "VERIFIED":
        blockers.append("packet hash verification not performed")
    if final_authorization_status != "PASSED":
        blockers.append("final authorization blocked")
    if human_coding_gate_status != "PASSED":
        blockers.append("human-coding gate blocked")
    if not record_locking_ready:
        blockers.append("record-locking readiness unverified")
    coding_allowed = not blockers
    return HumanCodingGateDecision(
        decision="HUMAN_CODING_ALLOWED" if coding_allowed else "HUMAN_CODING_BLOCKED",
        preparation_gates_sufficient=rights_ready and packets_ready,
        coding_allowed=coding_allowed,
        blockers=tuple(blockers),
    )


def assert_human_coding_allowed(decision: HumanCodingGateDecision) -> None:
    if not decision.coding_allowed:
        raise HumanCodingBlockedError(f"human coding is blocked: {', '.join(decision.blockers)}")
