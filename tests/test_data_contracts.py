import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "src" / "core"


def load(path: Path):
    return json.loads(path.read_text())


def test_knowledge_graph_schema_and_references():
    graph = load(ROOT / "data" / "knowledge-graph.json")
    schema = load(CORE / "knowledge-graph.schema.json")
    node_schema = load(CORE / "knowledge-node.schema.json")
    schema["properties"]["nodes"]["items"] = node_schema
    errors = list(Draft202012Validator(schema).iter_errors(graph))
    assert not errors, [error.message for error in errors]
    ids = {node["id"] for node in graph["nodes"]}
    assert len(ids) == len(graph["nodes"])
    assert all(edge["source"] in ids and edge["target"] in ids for edge in graph["edges"])
    assert next(node for node in graph["nodes"] if node["id"] == "REVIEW-000002")["status"] == "APPROVED"


def test_event_ledger_is_valid_and_monotonic():
    schema = load(CORE / "event.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    events = [json.loads(line) for line in (ROOT / "data" / "ledger" / "events.jsonl").read_text().splitlines() if line.strip()]
    assert events
    assert [event["event_id"] for event in events] == sorted(event["event_id"] for event in events)
    for event in events:
        assert not list(validator.iter_errors(event))


def test_agent_permissions_are_explicit():
    agents = load(ROOT / "data" / "agents.json")["agents"]
    assert agents
    assert len({agent["id"] for agent in agents}) == len(agents)
    assert all(agent["may"] and agent["may_not"] for agent in agents)
    assert all("promote a scientific claim" in agent["may_not"] for agent in agents if agent["id"] == "AGENT-ORCHESTRATOR")


def test_roadmap_gates_novel_research():
    phases = load(ROOT / "data" / "roadmap.json")["phases"]
    assert phases[-1]["title"] == "Novel research"
    assert phases[-1]["status"] == "GATED"


def test_second_benchmark_passport_is_valid_and_matches_preregistered_result():
    passport = load(ROOT / "benchmarks" / "BENCHMARK-000002.passport.json")
    schema = load(CORE / "benchmark-passport.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    assert not list(validator.iter_errors(passport))
    result = load(ROOT / "artifacts" / "results" / "CANDIDATE-000002.result.json")
    assert passport["passport_version"] == "1.0.1"
    # The passport stays byte-identical to the approved source commit. Post-run
    # approval is recorded separately so provenance is not rewritten in place.
    assert passport["scientific_review"] == "CHANGES_REQUIRED"
    assert passport["review_history"][-1]["response_status"] == "ADDRESSED_AWAITING_REREVIEW"
    assert passport["candidate_id"] == result["candidate"]["candidate_id"]
    assert passport["preregistered_checks"] == [check["check_id"] for check in result["checks"]]
    assert passport["expected_results"]["tolerance"] == "exact rational equality"


def test_coordinate_benchmark_implementation_rereview_is_approved_and_bounded():
    review = load(ROOT / "artifacts" / "reviews" / "REVIEW-000002.json")
    schema = load(CORE / "review-record.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    assert not list(validator.iter_errors(review))
    assert review["outcome"] == "APPROVED"
    assert review["subject"]["passport_version"] == "1.0.1"
    assert review["subject"]["head_commit"] == "4b2e24d445f9cacd08cd85cc1a35350951a1553f"
    assert len(review["verified_items"]) == 7
    assert review["remaining_objections"] == []
    assert all((ROOT / evidence_path).is_file() for item in review["verified_items"] for evidence_path in item["evidence_paths"])
    assert review["boundaries"] == {
        "external_scientific_reproduction": False,
        "novel_physics_claim": False,
        "transportation_claim": False,
    }
