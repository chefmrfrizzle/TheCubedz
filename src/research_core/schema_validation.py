from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]


def validate_candidate_schema(candidate: dict[str, Any]) -> list[str]:
    schema = json.loads((ROOT / "src" / "core" / "candidate.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(candidate), key=lambda item: list(item.absolute_path))]
