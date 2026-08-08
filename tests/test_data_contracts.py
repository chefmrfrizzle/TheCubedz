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
    assert passport["scientific_review"] == "CHANGES_REQUIRED"
    assert passport["review_history"][-1]["response_status"] == "ADDRESSED_AWAITING_REREVIEW"
    assert passport["candidate_id"] == result["candidate"]["candidate_id"]
    assert passport["preregistered_checks"] == [check["check_id"] for check in result["checks"]]
    assert passport["expected_results"]["tolerance"] == "exact rational equality"
