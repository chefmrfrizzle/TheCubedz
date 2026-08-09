from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .pipeline import load_and_evaluate
from .curved_pipeline import load_and_evaluate_curved
from .reporting import beginner_report, technical_report
from .control import SCHEMAS, load_and_validate_control
from .synthetic_benchmark import run_suite

ROOT = Path(__file__).resolve().parents[2]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="research-core", description="Run deliberately scoped, deterministic research validators.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify = subparsers.add_parser("verify", help="verify one candidate")
    verify.add_argument("candidate", type=Path)
    verify.add_argument("--write", action="store_true", help="write canonical result and reports")
    verify.add_argument("--reproducible", action="store_true", help="exclude wall-clock variability")
    verify.add_argument("--json", action="store_true", help="print the complete JSON result")
    verify.add_argument("--passport", type=Path, help="explicit benchmark passport used by a passport-bound profile")
    control = subparsers.add_parser("validate-control", help="validate one controlled-autonomy document")
    control.add_argument("kind", choices=sorted(SCHEMAS))
    control.add_argument("document", type=Path)
    benchmark = subparsers.add_parser("benchmark", help="run the frozen 100-case workflow benchmark")
    benchmark.add_argument("--write", action="store_true", help="write the canonical benchmark result")
    benchmark.add_argument("--json", action="store_true", help="print the complete benchmark result")
    return parser


def _write(candidate: dict, result: dict) -> None:
    result_path = ROOT / "artifacts" / "results" / f"{candidate['candidate_id']}.result.json"
    beginner_path = ROOT / "artifacts" / "reports" / f"{candidate['candidate_id']}.beginner.md"
    technical_path = ROOT / "artifacts" / "reports" / f"{candidate['candidate_id']}.technical.md"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    beginner_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    beginner_path.write_text(beginner_report(candidate, result), encoding="utf-8")
    technical_path.write_text(technical_report(candidate, result), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "validate-control":
        _, errors = load_and_validate_control(args.kind, args.document.resolve())
        if errors:
            for error in errors:
                print(f"FAIL: {error}")
            return 1
        print(f"PASS: {args.kind} document is valid and policy-conforming")
        return 0
    if args.command == "benchmark":
        result = run_suite()
        if args.write:
            output = ROOT / "artifacts" / "benchmarks" / "synthetic-suite-v1.result.json"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"suite: {result['suite_id']}@{result['suite_version']}")
            print(f"cases: {result['passed']} passed / {result['failed']} failed")
            print(f"outcomes: {json.dumps(result['outcomes'], sort_keys=True)}")
            print(f"digest: {result['result_digest']}")
        return 0 if result["failed"] == 0 else 1
    candidate_path = args.candidate.resolve()
    passport_path = args.passport.resolve() if args.passport else None
    candidate_document = json.loads(candidate_path.read_text(encoding="utf-8"))
    if candidate_document.get("schema_version") == "2.0.0":
        if passport_path is None:
            print("FAIL: curved benchmark profiles require an explicit --passport")
            return 1
        candidate, result = load_and_evaluate_curved(candidate_path, passport_path, reproducible=args.reproducible)
    else:
        candidate, result = load_and_evaluate(candidate_path, reproducible=args.reproducible, passport_path=passport_path)
    if args.write:
        _write(candidate, result)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"candidate: {candidate['candidate_id']}@{candidate['version']}")
        print(f"status: {result['assessment']['overall_status']}")
        print(f"checks: {sum(item['status'] == 'PASS' for item in result['checks'])} passed / {sum(item['status'] == 'FAIL' for item in result['checks'])} failed")
        print(f"digest: {result['scientific_payload_digest']}")
        print(f"transportation: {result['assessment']['transportation_status']}")
    return 0 if result["assessment"]["overall_status"] in {"BASELINE_VERIFIED", "BENCHMARK_VERIFIED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
