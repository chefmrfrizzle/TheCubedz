#!/usr/bin/env python3
"""Install TheCubedz research tools into a repository-local environment."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MINIMUM_PYTHON = (3, 12)
MINIMUM_NODE = (20, 9)


def run(command: list[str], *, dry_run: bool) -> None:
    print(f"+ {' '.join(command)}")
    if not dry_run:
        subprocess.run(command, cwd=ROOT, check=True)


def node_version(node: str) -> tuple[int, int, int]:
    completed = subprocess.run(
        [node, "--version"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", completed.stdout.strip())
    if not match:
        raise RuntimeError(f"Unable to read Node.js version: {completed.stdout.strip()}")
    return tuple(int(part) for part in match.groups())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create .venv, install the scientific and website dependencies, and run a local smoke test."
    )
    parser.add_argument("--dry-run", action="store_true", help="print the installation commands without running them")
    args = parser.parse_args()

    if sys.version_info < MINIMUM_PYTHON:
        print("ERROR: Python 3.12 or newer is required.", file=sys.stderr)
        return 2

    node = shutil.which("node")
    npm = shutil.which("npm.cmd" if os.name == "nt" else "npm")
    if not args.dry_run:
        if not node or not npm:
            print("ERROR: Node.js 20.9 or newer and npm are required.", file=sys.stderr)
            return 2
        if node_version(node) < (*MINIMUM_NODE, 0):
            print("ERROR: Node.js 20.9 or newer is required.", file=sys.stderr)
            return 2

    venv = ROOT / ".venv"
    venv_python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    run([sys.executable, "-m", "venv", str(venv)], dry_run=args.dry_run)
    run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], dry_run=args.dry_run)
    run([str(venv_python), "-m", "pip", "install", "--no-build-isolation", "-e", ".[dev]"], dry_run=args.dry_run)
    run([npm or "npm", "ci"], dry_run=args.dry_run)
    run([str(venv_python), "-m", "research_core.cli", "benchmark"], dry_run=args.dry_run)
    run([str(venv_python), "-m", "research_core.cli", "quiet", "--help"], dry_run=args.dry_run)

    if args.dry_run:
        print("Dry run complete; no files or environments were changed.")
    else:
        executable = venv / ("Scripts/research-core.exe" if os.name == "nt" else "bin/research-core")
        print("\nTheCubedz local research tools are installed.")
        print(f"Try: {executable} benchmark")
        print("This installation does not enroll a worker, open remote access, or upload data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
