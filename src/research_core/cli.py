from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .pipeline import load_and_evaluate
from .curved_pipeline import load_and_evaluate_curved
from .reporting import beginner_report, technical_report
from .control import SCHEMAS, load_and_validate_control
from .quiet_compute import (
    allocate_replications,
    build_isolated_execution_plan,
    compare_measurements,
    evaluate_consensus,
    load_json,
    score_evidence_reputation,
    seal_measurement,
    seal_passport,
    seal_reproduction,
    seal_submission,
    validate_measurement,
    validate_passport,
    validate_reproduction,
    validate_submission,
    verify_and_claim_job_envelope,
    verify_job_envelope,
)
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
    quiet = subparsers.add_parser("quiet", help="run local-only Quiet Compute evidence tools")
    quiet_subparsers = quiet.add_subparsers(dest="quiet_command", required=True)

    for name, help_text in (
        ("seal-measurement", "seal a local measurement draft with its canonical digest"),
        ("seal-passport", "seal a comparison passport draft with its canonical digest"),
        ("seal-submission", "seal a deliberate submission draft with its canonical digest"),
        ("seal-reproduction", "seal a reproduction result draft with its canonical digest"),
    ):
        command = quiet_subparsers.add_parser(name, help=help_text)
        command.add_argument("document", type=Path)
        command.add_argument("--output", type=Path, required=True)

    for name, help_text in (
        ("validate-measurement", "validate one sealed local measurement"),
        ("validate-passport", "validate one sealed comparison passport"),
        ("validate-submission", "validate one deliberate submission bundle"),
    ):
        command = quiet_subparsers.add_parser(name, help=help_text)
        command.add_argument("document", type=Path)
        command.add_argument("--json", action="store_true")

    compare = quiet_subparsers.add_parser("compare", help="compare an intervention with its frozen baseline")
    compare.add_argument("baseline", type=Path)
    compare.add_argument("intervention", type=Path)
    compare.add_argument("passport", type=Path)
    compare.add_argument("--output", type=Path)

    job = quiet_subparsers.add_parser("validate-job", help="verify a signed declarative job and worker eligibility")
    job.add_argument("envelope", type=Path)
    job.add_argument("trust_store", type=Path)
    job.add_argument("worker", type=Path)
    job.add_argument("--now", help="UTC timestamp used for reproducible verification")
    job.add_argument("--output", type=Path)

    plan = quiet_subparsers.add_parser("plan-job", help="verify a signed job and emit a non-executing isolation plan")
    plan.add_argument("envelope", type=Path)
    plan.add_argument("trust_store", type=Path)
    plan.add_argument("worker", type=Path)
    plan.add_argument("--now", help="UTC timestamp used for reproducible verification")
    plan.add_argument("--replay-ledger", type=Path, required=True, help="directory used for atomic nonce claims")
    plan.add_argument("--output", type=Path)

    allocation = quiet_subparsers.add_parser("allocate", help="assign one signed job across independent eligible workers")
    allocation.add_argument("envelope", type=Path)
    allocation.add_argument("trust_store", type=Path)
    allocation.add_argument("workers", type=Path, help="JSON array or object with a workers array")
    allocation.add_argument("passport", type=Path)
    allocation.add_argument("--now", help="UTC timestamp used for reproducible verification")
    allocation.add_argument("--output", type=Path)

    consensus = quiet_subparsers.add_parser("consensus", help="evaluate independent results against every declared tolerance")
    consensus.add_argument("results", type=Path, help="JSON array or object with a results array of signed envelopes")
    consensus.add_argument("workers", type=Path, help="JSON array or object with a workers array")
    consensus.add_argument("passport", type=Path)
    consensus.add_argument("--output", type=Path)

    reputation = quiet_subparsers.add_parser("reputation", help="score verified evidence-quality events")
    reputation.add_argument("events", type=Path, help="JSON array or object with an events array")
    reputation.add_argument("--output", type=Path)
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


def _write_json(path: Path | None, document: dict) -> None:
    body = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    if path is None:
        print(body, end="")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def _collection(path: Path, key: str) -> list[dict]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, dict):
        value = value.get(key)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"{path}: expected a JSON array or an object with a {key} array")
    return value


def _quiet(args: argparse.Namespace) -> int:
    from datetime import datetime

    sealers = {
        "seal-measurement": (seal_measurement, validate_measurement),
        "seal-passport": (seal_passport, validate_passport),
        "seal-submission": (seal_submission, validate_submission),
        "seal-reproduction": (seal_reproduction, validate_reproduction),
    }
    if args.quiet_command in sealers:
        sealer, validator = sealers[args.quiet_command]
        sealed = sealer(load_json(args.document.resolve()))
        errors = validator(sealed)
        if errors:
            for error in errors:
                print(f"FAIL: {error}")
            return 1
        _write_json(args.output.resolve(), sealed)
        print(f"PASS: sealed document written to {args.output.resolve()}")
        return 0

    validators = {
        "validate-measurement": validate_measurement,
        "validate-passport": validate_passport,
        "validate-submission": validate_submission,
    }
    if args.quiet_command in validators:
        document = load_json(args.document.resolve())
        errors = validators[args.quiet_command](document)
        if args.json:
            _write_json(None, {"status": "PASS" if not errors else "FAIL", "errors": errors})
        elif errors:
            for error in errors:
                print(f"FAIL: {error}")
        else:
            print(f"PASS: {args.quiet_command.removeprefix('validate-')} is valid and locally sealed")
        return 0 if not errors else 1

    if args.quiet_command == "compare":
        result = compare_measurements(load_json(args.baseline.resolve()), load_json(args.intervention.resolve()), load_json(args.passport.resolve()))
        _write_json(args.output.resolve() if args.output else None, result)
        return 0 if result["overall_status"] == "PASS" else 1

    if args.quiet_command in {"validate-job", "plan-job"}:
        envelope = load_json(args.envelope.resolve())
        trust_store = load_json(args.trust_store.resolve())
        worker = load_json(args.worker.resolve())
        now = datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else None
        decision = verify_job_envelope(envelope, trust_store, worker, now=now)
        if args.quiet_command == "plan-job":
            decision = verify_and_claim_job_envelope(envelope, trust_store, worker, args.replay_ledger.resolve(), now=now)
        output = decision
        if args.quiet_command == "plan-job" and decision["status"] == "ACCEPT":
            output = {"admission": decision, "plan": build_isolated_execution_plan(envelope["manifest"], worker)}
        _write_json(args.output.resolve() if args.output else None, output)
        return 0 if decision["status"] == "ACCEPT" else 1

    if args.quiet_command == "allocate":
        passport = load_json(args.passport.resolve())
        errors = validate_passport(passport)
        if errors:
            raise ValueError("invalid comparison passport: " + "; ".join(errors))
        now = datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else None
        output = allocate_replications(
            load_json(args.envelope.resolve()),
            load_json(args.trust_store.resolve()),
            _collection(args.workers.resolve(), "workers"),
            passport["replication"],
            now=now,
        )
        _write_json(args.output.resolve() if args.output else None, output)
        return 0 if output["status"] == "ALLOCATED" else 1

    if args.quiet_command == "consensus":
        output = evaluate_consensus(_collection(args.results.resolve(), "results"), _collection(args.workers.resolve(), "workers"), load_json(args.passport.resolve()))
        _write_json(args.output.resolve() if args.output else None, output)
        return 0 if output["status"] == "CONSENSUS" else 1

    if args.quiet_command == "reputation":
        output = score_evidence_reputation(_collection(args.events.resolve(), "events"))
        _write_json(args.output.resolve() if args.output else None, output)
        return 0
    raise ValueError(f"unknown Quiet Compute command: {args.quiet_command}")


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "quiet":
        try:
            return _quiet(args)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(f"FAIL: {error}")
            return 1
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
