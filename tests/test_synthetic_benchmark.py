import json
from pathlib import Path

from research_core.synthetic_benchmark import run_suite, strict_json_loads

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_suite_runs_exactly_one_hundred_cases():
    result = run_suite()
    assert result["case_count"] == 100
    assert result["passed"] == 100
    assert result["failed"] == 0
    assert [item["case_id"] for item in result["results"]] == [f"SYN-{index:03d}" for index in range(1, 101)]


def test_published_benchmark_artifact_matches_the_runner():
    published = json.loads((ROOT / "artifacts" / "benchmarks" / "synthetic-suite-v1.result.json").read_text(encoding="utf-8"))
    assert published == run_suite()


def test_suite_preserves_non_success_outcomes():
    result = run_suite()
    assert result["outcomes"]["REJECT"] > 0
    assert result["outcomes"]["MISMATCH"] > 0
    assert result["outcomes"]["UNRESOLVED"] > 0
    assert "no physical geometry" in result["scientific_scope"]


def test_secure_json_ingestion_rejects_duplicate_keys():
    try:
        strict_json_loads('{"a": 1, "a": 2}')
    except ValueError as error:
        assert "duplicate JSON key" in str(error)
    else:
        raise AssertionError("duplicate key was silently accepted")
