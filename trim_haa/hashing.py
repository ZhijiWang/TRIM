"""Hashing utilities for TRIM-HAA prompts, source packets, and outputs."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def sha256_text(text: str) -> str:
    """Return the SHA-256 hash of exact UTF-8 text."""

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str | Path) -> str:
    """Return the SHA-256 hash of a file."""

    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def looks_like_sha256(value: str) -> bool:
    return bool(SHA256_PATTERN.fullmatch(str(value).strip().lower()))

