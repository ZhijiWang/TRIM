"""OpenAI planning adapter with no client, transport, authentication, or network code."""

from __future__ import annotations

import re
from typing import Any

from .provider import ExecutionBlockedError


HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
REQUIRED_PASSED_GATES = (
    "provider_model_account",
    "runtime_settings",
    "pricing",
    "final_authorization",
    "human_coding",
    "model_execution",
)
FORBIDDEN_PUBLIC_FIELDS = {
    "api_key",
    "authorization_header",
    "bearer_token",
    "content",
    "copyrighted_excerpt",
    "credential",
    "credentials",
    "model_visible_source_content",
    "packet_text",
    "password",
    "private_packet_content",
    "prompt",
    "prompt_text",
    "raw_prompt",
    "secret",
    "source_text",
}


def _find_forbidden_fields(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = str(key).lower()
            if normalized in FORBIDDEN_PUBLIC_FIELDS:
                found.add(normalized)
            found.update(_find_forbidden_fields(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_forbidden_fields(item))
    return found


def assert_provider_preconditions(
    request_envelope: dict[str, Any],
    *,
    gate_statuses: dict[str, str],
    runtime_settings: dict[str, Any],
    request_preserved: bool,
    private_packet_access_authorization: str | None,
) -> None:
    """Reject the first missing future-execution requirement without side effects."""

    forbidden = _find_forbidden_fields(request_envelope)
    if forbidden:
        raise ExecutionBlockedError(f"public request object contains forbidden fields: {sorted(forbidden)}")
    for gate in REQUIRED_PASSED_GATES:
        if gate_statuses.get(gate) != "PASSED":
            raise ExecutionBlockedError(f"required gate is not PASSED: {gate}")
    if runtime_settings.get("account_availability_status") != "AVAILABLE_VERIFIED":
        raise ExecutionBlockedError("account availability is unverified")
    if runtime_settings.get("record_status") != "FROZEN_VERIFIED":
        raise ExecutionBlockedError("runtime settings record is not frozen and verified")
    if runtime_settings.get("provider_transmission_authorization_status") != "PASSED":
        raise ExecutionBlockedError("provider transmission authorization is absent")
    if runtime_settings.get("final_authorization_status") != "PASSED":
        raise ExecutionBlockedError("final authorization is absent")
    if runtime_settings.get("execution_allowed") is not True:
        raise ExecutionBlockedError("runtime settings prohibit execution")
    if request_envelope.get("transmission_authorized") is not True:
        raise ExecutionBlockedError("request envelope is not authorized for transmission")
    if request_envelope.get("transmitted") is not False:
        raise ExecutionBlockedError("request envelope must be untransmitted before a call")
    if request_envelope.get("request_preserved") is not True or not request_preserved:
        raise ExecutionBlockedError("request preservation has not completed")
    if not private_packet_access_authorization:
        raise ExecutionBlockedError("private-packet access authorization is absent")
    if not HASH_RE.fullmatch(str(request_envelope.get("source_packet_hash", ""))):
        raise ExecutionBlockedError("source packet hash is absent or invalid")
    if not HASH_RE.fullmatch(str(request_envelope.get("request_byte_hash", ""))):
        raise ExecutionBlockedError("request byte hash is absent or invalid")


class BlockedOpenAIAdapter:
    """A no-call implementation that can never reach a provider in this PR."""

    network_enabled = False

    def send_request(
        self,
        request_envelope: dict[str, Any],
        *,
        gate_statuses: dict[str, str],
        runtime_settings: dict[str, Any],
        request_preserved: bool,
        private_packet_access_authorization: str | None,
    ) -> Any:
        assert_provider_preconditions(
            request_envelope,
            gate_statuses=gate_statuses,
            runtime_settings=runtime_settings,
            request_preserved=request_preserved,
            private_packet_access_authorization=private_packet_access_authorization,
        )
        raise ExecutionBlockedError("no provider network implementation exists in the no-call scaffold")
