import json
from pathlib import Path

from research_core.canonical import scientific_payload, sha256_hex
from research_core.pipeline import evaluate

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = json.loads((ROOT / "candidates" / "CANDIDATE-000001.json").read_text())


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
