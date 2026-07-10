"""Provider-neutral interface for the deliberately disconnected scaffold."""

from __future__ import annotations

from typing import Any, Protocol


class ExecutionBlockedError(RuntimeError):
    """Raised when any provider-execution precondition is absent or blocked."""


class ProviderAdapter(Protocol):
    """Future provider adapter contract; implementations receive preserved metadata."""

    def send_request(
        self,
        request_envelope: dict[str, Any],
        *,
        gate_statuses: dict[str, str],
        runtime_settings: dict[str, Any],
        request_preserved: bool,
        private_packet_access_authorization: str | None,
    ) -> Any:
        """Attempt a future call or fail closed before any network operation."""
