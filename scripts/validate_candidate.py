#!/usr/bin/env python3
"""Minimal candidate validator.

This deliberately validates only repository structure/basic matrix consistency.
It is NOT a general-relativity solver.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def validate(candidate: dict) -> list[str]:
    errors: list[str] = []
    required = {
        "candidate_id",
        "version",
        "title",
        "status",
        "coordinates",
        "metric",
        "parameters",
        "assumptions",
        "references",
        "provenance",
    }
    missing = sorted(required - candidate.keys())
    if missing:
        errors.append(f"missing required keys: {', '.join(missing)}")
        return errors

    coords = candidate["coordinates"]
    components = candidate["metric"].get("components")
    if not isinstance(components, list):
        errors.append("metric.components must be a matrix/list")
        return errors

    n = len(coords)
    if len(components) != n or any(not isinstance(row, list) or len(row) != n for row in components):
        errors.append(f"metric.components must be {n}x{n} for {n} coordinates")

    if components and len(components) == n:
        for i in range(n):
            for j in range(n):
                if components[i][j] != components[j][i]:
                    errors.append(f"metric is not symmetric at ({i},{j})")
                    return errors

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/validate_candidate.py path/to/candidate.json")
        return 2

    path = Path(sys.argv[1])
    candidate = json.loads(path.read_text())
    errors = validate(candidate)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALID: basic candidate structure and metric shape checks passed")
    print("NOTE: this does not establish mathematical or physical validity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
