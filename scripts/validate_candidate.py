#!/usr/bin/env python3
"""Compatibility entry point for the versioned research-core validator.

A fresh clone can run this file directly without first installing the package:

    python scripts/validate_candidate.py candidates/CANDIDATE-000001.json
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from research_core.cli import main  # noqa: E402

if __name__ == "__main__":
    candidate = sys.argv[1:2]
    flags = sys.argv[2:]
    raise SystemExit(main(["verify", *candidate, *flags]))
