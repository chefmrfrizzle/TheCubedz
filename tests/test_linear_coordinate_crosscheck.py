import json
from pathlib import Path

from independent.linear_coordinate_crosscheck import _portable_text_digest, evaluate_checks, run_crosscheck

ROOT = Path(__file__).resolve().parents[1]


def test_linear_coordinate_crosscheck_matches_all_reference_checks():
    result = run_crosscheck()
    assert result["comparison"] == "MATCH"
    assert len(result["observations"]["checks"]) == 13
    assert set(result["observations"]["checks"].values()) == {"PASS"}
    assert "schema.candidate.v1" not in result["observations"]["checks"]
    assert result["comparison_scope"]["excluded_reference_checks"] == ["schema.candidate.v1"]
    assert result["comparison_scope"]["schema_conformance_crosschecked"] is False
    assert result["observations"]["metric_determinant"] == -14400
    assert result["observations"]["jacobian_determinant"] == 120
    assert result["discrepancies"] == []


def test_published_linear_coordinate_crosscheck_matches_runner():
    published = json.loads((ROOT / "artifacts" / "reproductions" / "CANDIDATE-000002.crosscheck.json").read_text(encoding="utf-8"))
    assert published == run_crosscheck()


def test_linear_coordinate_crosscheck_is_not_external_reproduction():
    result = run_crosscheck()
    assert result["independence"]["separate_implementation"] is True
    assert result["independence"]["separate_environment"] is False
    assert result["independence"]["separate_contributor"] is False
    assert result["independence"]["counts_as_external_reproduction"] is False


def test_linear_coordinate_crosscheck_does_not_import_research_core():
    source = (ROOT / "independent" / "linear_coordinate_crosscheck.py").read_text(encoding="utf-8")
    assert "from research_core" not in source
    assert "import research_core" not in source
    assert '"schema.candidate.v1": required.issubset(candidate)' not in source


def test_linear_coordinate_crosscheck_rejects_reviewer_jacobian_counterexample():
    candidate = json.loads((ROOT / "candidates" / "CANDIDATE-000002.json").read_text(encoding="utf-8"))
    passport = json.loads((ROOT / "benchmarks" / "BENCHMARK-000002.passport.json").read_text(encoding="utf-8"))
    candidate["parameters"]["coordinate_map"]["jacobian"] = [
        [4.25, 5.625, 0, 0],
        [3.75, 6.375, 0, 0],
        [0, 0, 4, 0],
        [0, 0, 0, 5],
    ]
    checks = evaluate_checks(candidate, passport)["checks"]
    assert checks["coordinate_map.jacobian"] is False


def test_coordinate_input_digest_is_stable_across_checkout_line_endings(tmp_path):
    lf = tmp_path / "lf.json"
    crlf = tmp_path / "crlf.json"
    lf.write_bytes(b'{\n  "value": 1\n}\n')
    crlf.write_bytes(b'{\r\n  "value": 1\r\n}\r\n')
    assert _portable_text_digest(lf) == _portable_text_digest(crlf)
