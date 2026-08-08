import json
from pathlib import Path

from research_core.canonical import scientific_payload, sha256_hex
from research_core.pipeline import evaluate

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = json.loads((ROOT / "candidates" / "CANDIDATE-000001.json").read_text())
COORDINATE_CANDIDATE = json.loads((ROOT / "candidates" / "CANDIDATE-000002.json").read_text())


def test_baseline_has_twelve_passing_checks():
    result = evaluate(CANDIDATE, reproducible=True, source_commit="TEST")
    assert result["assessment"]["overall_status"] == "BASELINE_VERIFIED"
    assert len(result["checks"]) == 12
    assert all(check["status"] == "PASS" for check in result["checks"])
    assert result["assessment"]["transportation_status"] == "NOT_A_TRANSPORTATION_PROPOSAL"


def test_scientific_digest_is_deterministic_and_excludes_runtime():
    first = evaluate(CANDIDATE, reproducible=True, source_commit="ONE")
    second = evaluate(CANDIDATE, reproducible=True, source_commit="TWO")
    assert first["scientific_payload_digest"] == second["scientific_payload_digest"]
    assert first["scientific_payload_digest"] == f"sha256:{sha256_hex(scientific_payload(first))}"


def test_invalid_matrix_fails():
    invalid = json.loads(json.dumps(CANDIDATE))
    invalid["metric"]["components"][0][1] = 2
    result = evaluate(invalid, reproducible=True, source_commit="TEST")
    assert result["assessment"]["overall_status"] == "VALIDATION_FAILED"
    assert any(check["check_id"] == "metric.symmetry" and check["status"] == "FAIL" for check in result["checks"])


def test_rescaled_coordinate_benchmark_has_fourteen_passing_checks():
    result = evaluate(COORDINATE_CANDIDATE, reproducible=True, source_commit="TEST")
    assert result["assessment"]["overall_status"] == "BENCHMARK_VERIFIED"
    assert len(result["checks"]) == 14
    assert all(check["status"] == "PASS" for check in result["checks"])
    assert next(check for check in result["checks"] if check["check_id"] == "metric.determinant")["observed"] == -14400
    assert next(check for check in result["checks"] if check["check_id"] == "coordinate_map.jacobian")["observed"] == 120
    assert result["assessment"]["transportation_status"] == "NOT_A_TRANSPORTATION_PROPOSAL"


def test_rescaled_coordinate_benchmark_digest_is_deterministic():
    first = evaluate(COORDINATE_CANDIDATE, reproducible=True, source_commit="ONE")
    second = evaluate(COORDINATE_CANDIDATE, reproducible=True, source_commit="TWO")
    assert first["scientific_payload_digest"] == second["scientific_payload_digest"]


def test_rescaled_coordinate_benchmark_rejects_wrong_pullback():
    invalid = json.loads(json.dumps(COORDINATE_CANDIDATE))
    invalid["metric"]["components"][3][3] = 24
    result = evaluate(invalid, reproducible=True, source_commit="TEST")
    assert result["assessment"]["overall_status"] == "VALIDATION_FAILED"
    assert next(check for check in result["checks"] if check["check_id"] == "coordinate_map.pullback")["status"] == "FAIL"


def test_rescaled_coordinate_benchmark_rejects_singular_jacobian():
    invalid = json.loads(json.dumps(COORDINATE_CANDIDATE))
    invalid["parameters"]["coordinate_map"]["jacobian"][3][3] = 0
    result = evaluate(invalid, reproducible=True, source_commit="TEST")
    assert next(check for check in result["checks"] if check["check_id"] == "coordinate_map.jacobian")["status"] == "FAIL"
    assert next(check for check in result["checks"] if check["check_id"] == "coordinate_map.pullback")["status"] == "FAIL"


def test_rescaled_coordinate_benchmark_rejects_convention_and_coordinate_mismatches():
    invalid = json.loads(json.dumps(COORDINATE_CANDIDATE))
    invalid["parameters"]["coordinate_map"]["from_coordinates"][0] = "wrong"
    invalid["conventions"]["metric_signature"] = "+---"
    invalid["conventions"]["cosmological_constant"] = 1
    result = evaluate(invalid, reproducible=True, source_commit="TEST")
    statuses = {check["check_id"]: check["status"] for check in result["checks"]}
    assert statuses["coordinate_map.coordinates"] == "FAIL"
    assert statuses["minkowski.signature"] == "FAIL"
    assert statuses["minkowski.cosmological_constant"] == "FAIL"
