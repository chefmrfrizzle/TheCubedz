from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    """Encode JSON deterministically for content-addressed artifacts."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def scientific_payload(result: dict[str, Any]) -> dict[str, Any]:
    """Return the result fields whose scientific meaning must remain stable.

    Runtime clocks, interpreter versions, and source-control metadata are excluded.
    """
    return {
        "schema_version": result["schema_version"],
        "candidate": result["candidate"],
        "validator": result["validator"],
        "checks": result["checks"],
        "assessment": result["assessment"],
        "warnings": result["warnings"],
        "errors": result["errors"],
        "limitations": result["limitations"],
    }
