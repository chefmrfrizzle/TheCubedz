from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from research_core.cli import main

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "candidates" / "CANDIDATE-000001.json"
INVALID = ROOT / "tests" / "fixtures" / "CANDIDATE-invalid-nonsymmetric.json"


def test_cli_main_verifies_baseline():
    assert main(["verify", str(CANDIDATE), "--reproducible"]) == 0


def test_cli_main_rejects_invalid_candidate():
    assert main(["verify", str(INVALID), "--reproducible"]) == 1


def test_compatibility_script_runs_from_fresh_checkout():
    completed = subprocess.run(
        [sys.executable, "scripts/validate_candidate.py", str(CANDIDATE), "--reproducible"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "status: BASELINE_VERIFIED" in completed.stdout
