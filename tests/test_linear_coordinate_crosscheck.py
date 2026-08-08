import json
from pathlib import Path

from independent.linear_coordinate_crosscheck import run_crosscheck

ROOT = Path(__file__).resolve().parents[1]


def test_linear_coordinate_crosscheck_matches_all_reference_checks():
    result = run_crosscheck()
    assert result["comparison"] == "MATCH"
    assert len(result["observations"]["checks"]) == 14
    assert set(result["observations"]["checks"].values()) == {"PASS"}
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
