from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "src/core/research-program.schema.json").read_text(encoding="utf-8"))
PROGRAM = json.loads((ROOT / "data/research-program.json").read_text(encoding="utf-8"))


def errors(document):
    validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
    return sorted(validator.iter_errors(document), key=lambda error: list(error.absolute_path))


def test_research_program_matches_schema_and_preserves_current_counts():
    assert errors(PROGRAM) == []
    assert PROGRAM["current_evidence"] == {
        "known_answer_examples": 3,
        "implemented_checks": 43,
        "workflow_cases": 100,
        "novel_transportation_candidates": 0,
        "traveler_safety_evaluations": 0,
        "outside_reproductions": 0,
    }


def test_research_program_cannot_claim_a_solution_or_verified_traveler_safety():
    inflated = deepcopy(PROGRAM)
    inflated["current_evidence"]["novel_transportation_candidates"] = 1
    assert errors(inflated)

    inflated = deepcopy(PROGRAM)
    inflated["traveler_constraint"]["requirement"] = "VERIFIED"
    assert errors(inflated)


def test_research_program_keeps_agents_and_public_inputs_noncanonical():
    assert PROGRAM["security"] == {
        "public_input_mode": "REPOSITORY_REVIEW_ONLY",
        "public_code_execution": "DISABLED",
        "canonical_promotion": "NAMED_HUMAN_ONLY",
        "agent_authority": "PROPOSE_ONLY",
    }
    assert all(task["canonical_effect"] == "NONE_WITHOUT_HUMAN_REVIEW" for task in PROGRAM["contribution_tasks"])


def test_only_the_established_benchmark_gates_are_currently_passing():
    passed = [gate for gate in PROGRAM["success_gates"] if gate["status"] == "PASS"]
    assert [gate["id"] for gate in passed] == ["GATE-01", "GATE-02"]
    assert all(gate["evidence"] == [] for gate in PROGRAM["success_gates"] if gate["status"] != "PASS")
