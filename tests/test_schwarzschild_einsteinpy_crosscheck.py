from independent.schwarzschild_einsteinpy_crosscheck import run


def test_einsteinpy_crosscheck_matches_with_separate_solver():
    result = run(source_commit="TEST")
    assert result["overall_status"] == "MATCH"
    assert all(status == "PASS" for status in result["observations"]["checks"].values())
    assert result["independence"]["separate_tensor_library"] is True
    assert result["solver"]["name"] == "EinsteinPy symbolic module"


def test_einsteinpy_crosscheck_discloses_conflict_and_signature_boundary():
    result = run(source_commit="TEST")
    assert result["independence"]["external_reproduction"] is False
    assert result["conflict_of_interest"]["declared"] is True
    assert result["signature"]["status"] == "UNSIGNED_NO_KEY"
    assert result["signature"]["record_digest_is_not_a_signature"] is True
