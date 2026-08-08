from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from independent.linear_coordinate_crosscheck import run_crosscheck


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the separate standard-library linear-coordinate cross-check.")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_crosscheck()
    if args.write:
        output = ROOT / "artifacts" / "reproductions" / "CANDIDATE-000002.crosscheck.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"comparison: {result['comparison']}")
        print(f"checks: {len(result['observations']['checks'])}")
        print(f"independence: {result['independence']['level']}")
        print(f"external reproduction: {result['independence']['counts_as_external_reproduction']}")
        print(f"digest: {result['record_digest']}")
    return 0 if result["comparison"] == "MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
