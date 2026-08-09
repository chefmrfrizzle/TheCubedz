import json
from copy import deepcopy
from pathlib import Path

from research_core.canonical import scientific_payload, sha256_hex
from research_core.curved_pipeline import evaluate_curved

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = json.loads((ROOT / "candidates" / "CANDIDATE-000003.json").read_text(encoding="utf-8"))
PASSPORT = json.loads((ROOT / "benchmarks" / "BENCHMARK-000003.passport.json").read_text(encoding="utf-8"))


def _statuses(result):
    return {check["check_id"]: check["status"] for check in result["checks"]}


def test_schwarzschild_exterior_has_seventeen_passing_checks():
    result = evaluate_curved(CANDIDATE, PASSPORT, reproducible=True, source_commit="TEST")
    assert result["assessment"]["overall_status"] == "BENCHMARK_VERIFIED"
    assert len(result["checks"]) == 17
    assert all(check["status"] == "PASS" for check in result["checks"])
    assert result["assessment"]["transportation_status"] == "NOT_A_TRANSPORTATION_PROPOSAL"
    assert result["validator"]["benchmark_passport"]["bound"] is True
    assert result["scientific_payload_digest"] == f"sha256:{sha256_hex(scientific_payload(result))}"


def test_curved_digest_excludes_runtime_metadata():
    first = evaluate_curved(CANDIDATE, PASSPORT, reproducible=True, source_commit="ONE")
    second = evaluate_curved(CANDIDATE, PASSPORT, reproducible=True, source_commit="TWO")
    assert first["scientific_payload_digest"] == second["scientific_payload_digest"]


def test_changed_metric_is_rejected():
    invalid = deepcopy(CANDIDATE)
    invalid["metric"]["components"][0][0] = "-(1 - 3*M/r)"
    result = evaluate_curved(invalid, PASSPORT, reproducible=True, source_commit="TEST")
    assert result["assessment"]["overall_status"] == "VALIDATION_FAILED"
    assert _statuses(result)["metric.components"] == "FAIL"


def test_domain_that_admits_horizon_is_rejected():
    invalid = deepcopy(CANDIDATE)
    invalid["domain"]["coordinate_ranges"]["r"] = "r >= 2*M"
    result = evaluate_curved(invalid, PASSPORT, reproducible=True, source_commit="TEST")
    assert _statuses(result)["schema.candidate.v2"] == "PASS"
    assert _statuses(result)["domain.schwarzschild_exterior"] == "FAIL"


def test_flipped_riemann_convention_is_rejected():
    invalid = deepcopy(CANDIDATE)
    invalid["conventions"]["riemann_tensor_definition"] = "opposite sign convention"
    result = evaluate_curved(invalid, PASSPORT, reproducible=True, source_commit="TEST")
    assert _statuses(result)["schema.candidate.v2"] == "FAIL"
    assert _statuses(result)["conventions.tensor_signs"] == "FAIL"


def test_modified_passport_cannot_redefine_the_bound_benchmark():
    invalid_passport = deepcopy(PASSPORT)
    invalid_passport["expected_results"]["kretschmann_scalar"] = 0
    result = evaluate_curved(CANDIDATE, invalid_passport, reproducible=True, source_commit="TEST")
    assert result["validator"]["benchmark_passport"]["bound"] is False
    assert result["assessment"]["overall_status"] == "VALIDATION_FAILED"
    assert _statuses(result)["curvature.kretschmann"] == "FAIL"
