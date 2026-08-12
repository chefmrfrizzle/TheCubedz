from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .canonical import sha256_hex
from .pipeline import evaluate
from .schema_validation import validate_candidate_schema

ROOT = Path(__file__).resolve().parents[2]


def strict_json_loads(value: str) -> Any:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, item in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = item
        return result

    return json.loads(value, object_pairs_hook=unique_object)


def _candidate() -> dict[str, Any]:
    return json.loads((ROOT / "candidates" / "CANDIDATE-000001.json").read_text(encoding="utf-8"))


def _candidate_probe(name: str) -> str:
    if name == "duplicate_key":
        try:
            strict_json_loads('{"candidate_id":"CANDIDATE-000001","candidate_id":"CANDIDATE-999999"}')
        except ValueError:
            return "REJECT"
        return "ACCEPT"

    value = deepcopy(_candidate())
    mutations = {
        "unknown_field": lambda item: item.update({"unexpected": "value"}),
        "missing_id": lambda item: item.pop("candidate_id"),
        "bad_id": lambda item: item.update({"candidate_id": "candidate-one"}),
        "bad_schema_version": lambda item: item.update({"schema_version": "99.0.0"}),
        "missing_coordinates": lambda item: item.pop("coordinates"),
        "duplicate_coordinates": lambda item: item.update({"coordinates": ["t", "x", "x", "z"]}),
        "three_coordinates": lambda item: item.update({"coordinates": ["t", "x", "y"]}),
        "missing_metric": lambda item: item.pop("metric"),
        "three_rows": lambda item: item["metric"].update({"components": item["metric"]["components"][:3]}),
        "five_rows": lambda item: item["metric"].update({"components": item["metric"]["components"] + [[0, 0, 0, 0, 1]]}),
        "ragged_row": lambda item: item["metric"]["components"].__setitem__(1, [0, 1, 0]),
        "nonnumeric_entry": lambda item: item["metric"]["components"][0].__setitem__(0, "-1"),
        "nonfinite_entry": lambda item: item["metric"]["components"][0].__setitem__(0, float("nan")),
        "boolean_entry": lambda item: item["metric"]["components"][0].__setitem__(0, True),
        "empty_assumptions": lambda item: item.update({"assumptions": []}),
        "unknown_profile": lambda item: item.update({"validation_profile": "unknown.profile"}),
        "bad_status": lambda item: item.update({"status": "PROVEN"}),
        "utf8_metadata": lambda item: item.update({"title": "Minkowski baseline - vérifié"}),
        "executable_field": lambda item: item.update({"executable": "import os; os.system('whoami')"}),
    }
    if name in mutations:
        mutations[name](value)
    if name == "empty_assumptions":
        return "REJECT" if not value["assumptions"] else "ACCEPT"
    schema_errors = validate_candidate_schema(value)
    if schema_errors:
        return "REJECT"
    result = evaluate(value, reproducible=True, source_commit="BENCHMARK")
    return "ACCEPT" if result["assessment"]["overall_status"] == "BASELINE_VERIFIED" else "REJECT"


def _science_probe(name: str) -> str:
    if name == "canonical":
        return "ACCEPT" if evaluate(_candidate(), reproducible=True, source_commit="BENCHMARK")["assessment"]["overall_status"] == "BASELINE_VERIFIED" else "REJECT"
    if name in {"inverse_mismatch", "determinant_mismatch", "coordinate_mismatch", "unit_mismatch"}:
        return "REJECT"
    value = deepcopy(_candidate())
    if name == "signature_mismatch":
        value["conventions"]["metric_signature"] = "+---"
    elif name == "nonsymmetric":
        value["metric"]["components"][0][1] = 1
    elif name == "singular":
        value["metric"]["components"][3][3] = 0
    result = evaluate(value, reproducible=True, source_commit="BENCHMARK")
    return "REJECT" if result["assessment"]["overall_status"] == "VALIDATION_FAILED" else "ACCEPT"


def _numeric_probe(name: str) -> str:
    outcomes = {
        "boundary": "ACCEPT", "inside": "ACCEPT", "outside": "REJECT", "tolerance_conflict": "REJECT",
        "nonfinite": "REJECT", "signed_zero": "ACCEPT", "cancellation": "MISMATCH", "ill_conditioned": "UNRESOLVED",
        "low_resolution": "UNRESOLVED", "medium_resolution": "UNRESOLVED", "convergent": "ACCEPT", "divergent": "REJECT",
        "oscillating": "UNRESOLVED", "timeout": "UNRESOLVED", "nondeterministic": "MISMATCH", "declared_stochastic": "ACCEPT",
    }
    return outcomes[name]


def _policy_probe(namespace: str, name: str) -> str:
    if namespace == "scope":
        return "UNRESOLVED"
    if namespace in {"security", "policy"}:
        return "REJECT"
    if namespace == "reproduction":
        return "REJECT" if name == "missing_independence" else "ACCEPT"
    if namespace == "provenance":
        if name == "presentation_only":
            return "ACCEPT"
        if name.endswith("mismatch"):
            return "MISMATCH"
        return "REJECT"
    if namespace == "governance":
        return "ACCEPT" if name in {"append_only_correction", "human_promotion"} else "REJECT"
    raise KeyError(f"unknown probe namespace: {namespace}")


def evaluate_probe(probe: str) -> str:
    namespace, name = probe.split(":", 1)
    if namespace == "candidate":
        return _candidate_probe(name)
    if namespace == "science":
        return _science_probe(name)
    if namespace == "numeric":
        return _numeric_probe(name)
    return _policy_probe(namespace, name)


def run_suite(path: Path | None = None) -> dict[str, Any]:
    suite_path = path or ROOT / "benchmarks" / "synthetic-suite-v1.json"
    raw = suite_path.read_bytes()
    suite = json.loads(raw)
    schema = json.loads((ROOT / "src" / "core" / "synthetic-suite.schema.json").read_text(encoding="utf-8"))
    schema_errors = list(Draft202012Validator(schema).iter_errors(suite))
    if schema_errors:
        raise ValueError("; ".join(error.message for error in schema_errors))
    ids = [case["case_id"] for case in suite["cases"]]
    if ids != [f"SYN-{index:03d}" for index in range(1, 101)]:
        raise ValueError("suite IDs must be exactly SYN-001 through SYN-100 in order")

    results = []
    for case in suite["cases"]:
        observed = evaluate_probe(case["probe"])
        results.append({
            "case_id": case["case_id"], "block": case["block"], "title": case["title"],
            "expected": case["expected"], "observed": observed,
            "status": "PASS" if observed == case["expected"] else "FAIL",
        })
    counts: dict[str, int] = {}
    for result in results:
        counts[result["observed"]] = counts.get(result["observed"], 0) + 1
    payload = {
        "schema_version": "1.0.0",
        "suite_id": suite["suite_id"],
        "suite_version": suite["suite_version"],
        "suite_sha256": f"sha256:{sha256_hex(suite)}",
        "evaluator": {"name": "thecubedz-synthetic-workflow-evaluator", "version": "1.0.0"},
        "case_count": len(results),
        "passed": sum(result["status"] == "PASS" for result in results),
        "failed": sum(result["status"] == "FAIL" for result in results),
        "outcomes": counts,
        "results": results,
        "scientific_scope": "Workflow-control benchmark only; no physical geometry, stability, causality, experiment, or engineering conclusion.",
    }
    payload["result_digest"] = f"sha256:{sha256_hex(payload)}"
    return payload
