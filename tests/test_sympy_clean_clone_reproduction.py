from pathlib import Path

from independent.sympy_clean_clone_reproduction import run

ROOT = Path(__file__).resolve().parents[1]


def test_sympy_reproduction_matches_both_candidates():
    result = run()
    assert result["comparison"] == "MATCH"
    assert len(result["candidates"]) == 2
    assert all(status == "PASS" for candidate in result["candidates"] for status in candidate["checks"].values())
    assert result["candidates"][0]["published_scientific_payload_digest"].startswith("sha256:")
    assert result["candidates"][1]["observations"]["jacobian_determinant"] == 120


def test_sympy_reproduction_discloses_conflicts_and_is_not_external_or_signed():
    result = run()
    assert result["conflict_of_interest"]["disclosed"] is True
    assert result["independence"]["clean_remote_clone"] is True
    assert result["independence"]["separate_library"] is True
    assert result["independence"]["separate_contributor"] is False
    assert result["independence"]["counts_as_external_reproduction"] is False
    assert result["signature"]["status"] == "UNSIGNED_NO_KEY"


def test_sympy_reproduction_does_not_import_project_science_code():
    source = (ROOT / "independent" / "sympy_clean_clone_reproduction.py").read_text(encoding="utf-8")
    assert "from research_core" not in source
    assert "import research_core" not in source
