"""Fail-closed, exact-model metadata inspection for the frozen pilot candidate.

This source-checkout-only module can retrieve one model metadata object.  It has
no inference transport and never accepts prompt or source content.
"""

from __future__ import annotations

import importlib.metadata
import json
import platform
import re
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Callable


PROVIDER = "OpenAI"
FROZEN_CANDIDATE_MODEL = "gpt-5.4-mini"
MODEL_METADATA_ENDPOINT_CLASS = "GET /v1/models/{model}"
MODEL_METADATA_URL = "https://api.openai.com/v1/models/gpt-5.4-mini"
_MAX_RESPONSE_BYTES = 65_536
_SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"(?i)Bearer\s+[A-Za-z0-9._-]+"),
    re.compile(r"(?i)Authorization\s*[:=]\s*[^\s,;]+"),
)


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Keep the credential pinned to the exact configured metadata URL."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


def _open_without_redirect(request: urllib.request.Request, *, timeout: int):
    return urllib.request.build_opener(_NoRedirectHandler()).open(request, timeout=timeout)


@dataclass(frozen=True)
class MetadataAuditResult:
    """Allowlisted, non-secret result of one exact-model metadata attempt."""

    audit_status: str
    provider: str
    requested_model_identifier: str
    metadata_endpoint_class: str
    request_timestamp: str | None
    credential_present: bool
    credential_committed: bool
    metadata_request_performed: bool
    http_result_class: str
    account_access_result: str
    returned_model_identifier: str | None
    provider_owned_by: str | None
    provider_owned_by_suppressed: bool
    error_class: str | None
    error_message_summary: str | None
    inference_performed: bool
    responses_api_called: bool
    prompt_transmitted: bool
    private_content_transmitted: bool
    private_packet_accessed: bool
    python_version: str
    operating_system_class: str
    sdk_version: str

    def public_dict(self) -> dict[str, Any]:
        """Return only the explicitly allowlisted public metadata fields."""

        return asdict(self)


def redact_sensitive_text(value: str, *, limit: int = 240) -> str:
    """Remove credential-like material from a bounded error summary."""

    redacted = value
    for pattern in _SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return " ".join(redacted.split())[:limit]


def _safe_owned_by(value: Any) -> tuple[str | None, bool]:
    if value == "openai":
        return "openai", False
    return None, value is not None


def _base_result(**overrides: Any) -> MetadataAuditResult:
    try:
        sdk_version = importlib.metadata.version("openai")
    except importlib.metadata.PackageNotFoundError:
        sdk_version = "not_installed"
    values: dict[str, Any] = {
        "audit_status": "BLOCKED_PROVIDER_ERROR",
        "provider": PROVIDER,
        "requested_model_identifier": FROZEN_CANDIDATE_MODEL,
        "metadata_endpoint_class": MODEL_METADATA_ENDPOINT_CLASS,
        "request_timestamp": None,
        "credential_present": False,
        "credential_committed": False,
        "metadata_request_performed": False,
        "http_result_class": "NOT_ATTEMPTED",
        "account_access_result": "BLOCKED_PROVIDER_ERROR",
        "returned_model_identifier": None,
        "provider_owned_by": None,
        "provider_owned_by_suppressed": False,
        "error_class": None,
        "error_message_summary": None,
        "inference_performed": False,
        "responses_api_called": False,
        "prompt_transmitted": False,
        "private_content_transmitted": False,
        "private_packet_accessed": False,
        "python_version": platform.python_version(),
        "operating_system_class": platform.system() or sys.platform,
        "sdk_version": sdk_version,
    }
    values.update(overrides)
    return MetadataAuditResult(**values)


def audit_exact_model_metadata(
    api_key: str | None,
    *,
    opener: Callable[..., Any] | None = None,
    timestamp: str | None = None,
) -> MetadataAuditResult:
    """Retrieve metadata for only ``gpt-5.4-mini``, or fail closed.

    The credential is used only to construct the authorization header in memory.
    It is never included in the returned result or in an error summary.
    """

    if not api_key:
        return _base_result(
            audit_status="BLOCKED_NO_CREDENTIAL_AVAILABLE",
            account_access_result="BLOCKED_NO_CREDENTIAL_AVAILABLE",
        )

    request_timestamp = timestamp or datetime.now(timezone.utc).isoformat(timespec="seconds")
    request = urllib.request.Request(
        MODEL_METADATA_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )
    open_request = opener or _open_without_redirect

    try:
        with open_request(request, timeout=10) as response:
            status = int(response.status)
            raw = response.read(_MAX_RESPONSE_BYTES + 1)
        if len(raw) > _MAX_RESPONSE_BYTES:
            raise ValueError("provider metadata response exceeded the audit byte limit")
        payload = json.loads(raw.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("provider metadata response was not a JSON object")
        returned_model = payload.get("id")
        object_type = payload.get("object")
        owned_by, suppressed = _safe_owned_by(payload.get("owned_by"))
        if status == 200 and returned_model == FROZEN_CANDIDATE_MODEL and object_type == "model":
            return _base_result(
                audit_status="METADATA_ACCESS_VERIFIED_INFERENCE_NOT_AUTHORIZED",
                request_timestamp=request_timestamp,
                credential_present=True,
                metadata_request_performed=True,
                http_result_class="SUCCESS",
                account_access_result="EXACT_MODEL_METADATA_ACCESS_VERIFIED",
                returned_model_identifier=returned_model,
                provider_owned_by=owned_by,
                provider_owned_by_suppressed=suppressed,
            )
        return _base_result(
            audit_status="BLOCKED_MODEL_NOT_ACCESSIBLE",
            request_timestamp=request_timestamp,
            credential_present=True,
            metadata_request_performed=True,
            http_result_class="UNEXPECTED_METADATA_RESPONSE",
            account_access_result="EXACT_MODEL_METADATA_NOT_VERIFIED",
            returned_model_identifier=(
                returned_model if returned_model == FROZEN_CANDIDATE_MODEL else None
            ),
            provider_owned_by=owned_by,
            provider_owned_by_suppressed=suppressed,
            error_class="MetadataResponseMismatch",
            error_message_summary="exact-model metadata response did not match the frozen candidate",
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            audit_status = "BLOCKED_AUTHENTICATION_FAILED"
            result_class = "AUTHENTICATION_FAILURE"
            access_result = "AUTHENTICATION_FAILED"
        elif exc.code == 404:
            audit_status = "BLOCKED_MODEL_NOT_ACCESSIBLE"
            result_class = "MODEL_NOT_ACCESSIBLE"
            access_result = "EXACT_MODEL_NOT_ACCESSIBLE"
        elif exc.code == 429:
            audit_status = "BLOCKED_PROVIDER_ERROR"
            result_class = "RATE_LIMITED"
            access_result = "BLOCKED_PROVIDER_ERROR"
        else:
            audit_status = "BLOCKED_PROVIDER_ERROR"
            result_class = "PROVIDER_ERROR"
            access_result = "BLOCKED_PROVIDER_ERROR"
        return _base_result(
            audit_status=audit_status,
            request_timestamp=request_timestamp,
            credential_present=True,
            metadata_request_performed=True,
            http_result_class=result_class,
            account_access_result=access_result,
            error_class="HTTPError",
            error_message_summary=f"provider metadata request returned HTTP {exc.code}",
        )
    except (urllib.error.URLError, TimeoutError) as exc:
        return _base_result(
            audit_status="BLOCKED_PROVIDER_ERROR",
            request_timestamp=request_timestamp,
            credential_present=True,
            metadata_request_performed=True,
            http_result_class="NETWORK_ERROR",
            account_access_result="BLOCKED_PROVIDER_ERROR",
            error_class=type(exc).__name__,
            error_message_summary="provider metadata network request failed",
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        return _base_result(
            audit_status="BLOCKED_PROVIDER_ERROR",
            request_timestamp=request_timestamp,
            credential_present=True,
            metadata_request_performed=True,
            http_result_class="INVALID_METADATA_RESPONSE",
            account_access_result="BLOCKED_PROVIDER_ERROR",
            error_class=type(exc).__name__,
            error_message_summary="provider metadata response could not be safely validated",
        )
