from __future__ import annotations

import json
import re
from hashlib import sha256
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = {
    "task": "research-task.schema.json",
    "capability": "capability-envelope.schema.json",
    "run": "agent-run.schema.json",
    "evidence": "evidence-bundle.schema.json",
    "promotion": "promotion-decision.schema.json",
}
CANONICAL_WRITE_ROOTS = (
    PurePosixPath("candidates"),
    PurePosixPath("artifacts/results"),
    PurePosixPath("data/ledger"),
    PurePosixPath("refs/heads/main"),
)


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _normalized_path(value: str) -> PurePosixPath:
    return PurePosixPath(value.replace("\\", "/").lstrip("/"))


def _is_within(path: PurePosixPath, root: PurePosixPath) -> bool:
    return path == root or root in path.parents


def validate_control_document(kind: str, document: dict[str, Any], *, now: datetime | None = None) -> list[str]:
    if kind not in SCHEMAS:
        return [f"unknown control document kind: {kind}"]
    schema = json.loads((ROOT / "src" / "core" / SCHEMAS[kind]).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]
    if errors:
        return errors

    if kind == "task" and "HUMAN_PROMOTION" not in document["required_gates"]:
        errors.append("required_gates: HUMAN_PROMOTION is mandatory")
    if kind == "task":
        paths = [item["path"] for item in document["inputs"]]
        if len(paths) != len(set(paths)):
            errors.append("inputs: paths must be unique")

    if kind == "capability":
        issued_at = _parse_time(document["issued_at"])
        expires_at = _parse_time(document["expires_at"])
        current = now or datetime.now(UTC)
        if expires_at <= issued_at:
            errors.append("expires_at: capability must expire after it is issued")
        if expires_at <= current:
            errors.append("expires_at: capability has expired")
        if document["network"]["mode"] == "DENY" and document["network"]["destinations"]:
            errors.append("network.destinations: DENY mode requires an empty destination list")
        if document["network"]["mode"] == "ALLOWLIST" and not document["network"]["destinations"]:
            errors.append("network.destinations: ALLOWLIST mode requires at least one destination")
        for field in ("read_paths", "write_paths"):
            for raw_path in document[field]:
                if raw_path.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", raw_path) or "\x00" in raw_path:
                    errors.append(f"{field}: paths must be workspace-relative ({raw_path})")
                path = _normalized_path(raw_path)
                if ".." in path.parts:
                    errors.append(f"{field}: traversal is forbidden ({raw_path})")
        for raw_path in document["write_paths"]:
            path = _normalized_path(raw_path)
            if any(_is_within(path, root) for root in CANONICAL_WRITE_ROOTS):
                errors.append(f"write_paths: canonical path is forbidden ({raw_path})")

    if kind == "run":
        if _parse_time(document["finished_at"]) < _parse_time(document["started_at"]):
            errors.append("finished_at: run cannot finish before it starts")

    if kind == "promotion":
        if document["reviewed_by"]["id"] == document["proposed_by"]["id"]:
            errors.append("reviewed_by: proposer cannot approve their own work")

    if kind == "evidence":
        unsigned = {key: value for key, value in document.items() if key != "bundle_digest"}
        canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        expected = f"sha256:{sha256(canonical).hexdigest()}"
        if document["bundle_digest"] != expected:
            errors.append("bundle_digest: does not match the canonical evidence manifest")

    return errors


def load_and_validate_control(kind: str, path: Path, *, now: datetime | None = None) -> tuple[dict[str, Any], list[str]]:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    document = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    return document, validate_control_document(kind, document, now=now)
