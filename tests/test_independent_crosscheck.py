import json
from pathlib import Path

from independent.minkowski_crosscheck import _portable_text_digest, determinant, inverse, run_crosscheck


def test_separate_crosscheck_matches_all_comparable_reference_checks():
    result = run_crosscheck()
    assert result["comparison"] == "MATCH"
    assert len(result["observations"]["checks"]) == 11
    assert set(result["observations"]["checks"].values()) == {"PASS"}
    assert "schema.candidate.v1" not in result["observations"]["checks"]
    assert result["comparison_scope"]["excluded_reference_checks"] == ["schema.candidate.v1"]
    assert result["comparison_scope"]["schema_conformance_crosschecked"] is False
    assert result["discrepancies"] == []


def test_published_crosscheck_artifact_matches_the_runner():
    published = json.loads((Path(__file__).resolve().parents[1] / "artifacts" / "reproductions" / "CANDIDATE-000001.crosscheck.json").read_text(encoding="utf-8"))
    assert published == run_crosscheck()


def test_crosscheck_does_not_claim_external_reproduction():
    result = run_crosscheck()
    assert result["independence"]["separate_implementation"] is True
    assert result["independence"]["separate_environment"] is False
    assert result["independence"]["separate_contributor"] is False
    assert result["independence"]["counts_as_external_reproduction"] is False


def test_independent_module_does_not_import_research_core():
    source = (Path(__file__).resolve().parents[1] / "independent" / "minkowski_crosscheck.py").read_text(encoding="utf-8")
    assert "from research_core" not in source
    assert "import research_core" not in source


def test_leibniz_and_adjugate_math_handles_a_nontrivial_matrix():
    matrix = [[1, 2], [3, 5]]
    assert determinant(matrix) == -1
    assert inverse(matrix) == [[-5, 2], [3, -1]]


def test_input_digest_is_stable_across_checkout_line_endings(tmp_path):
    lf = tmp_path / "lf.json"
    crlf = tmp_path / "crlf.json"
    lf.write_bytes(b'{\n  "value": 1\n}\n')
    crlf.write_bytes(b'{\r\n  "value": 1\r\n}\r\n')
    assert _portable_text_digest(lf) == _portable_text_digest(crlf)
