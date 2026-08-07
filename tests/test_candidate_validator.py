from scripts.validate_candidate import validate


def baseline():
    return {
        "candidate_id": "CANDIDATE-000001",
        "version": "0.1.0",
        "title": "baseline",
        "status": "DRAFT",
        "coordinates": ["t", "x"],
        "metric": {"components": [[-1, 0], [0, 1]]},
        "parameters": {},
        "assumptions": [],
        "references": [],
        "provenance": {"created_by": "test", "created_at": "2026-08-07T00:00:00Z"},
    }


def test_baseline_is_structurally_valid():
    assert validate(baseline()) == []


def test_non_symmetric_metric_is_rejected():
    item = baseline()
    item["metric"]["components"] = [[-1, 2], [0, 1]]
    assert "metric is not symmetric" in validate(item)[0]
