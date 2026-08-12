import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
PROGRAM = json.loads((ROOT / "data/quiet-compute-program.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / "src/core/quiet-compute-program.schema.json").read_text(encoding="utf-8"))


def errors_for(value):
    validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
    return list(validator.iter_errors(value))


def test_quiet_compute_program_matches_its_draft_contract():
    assert errors_for(PROGRAM) == []
    assert PROGRAM["campaign_line"] == "Data centers are too freaking loud."
    assert PROGRAM["response_line"] == "Let's make them quiet."
    assert PROGRAM["authority"] == "DRAFT_NOT_PREREGISTERED"
    assert PROGRAM["status"] == "VALIDATION_CORE_IMPLEMENTED"
    assert PROGRAM["current_evidence"]["verified_quieter_systems"] == 0
    assert PROGRAM["current_evidence"]["verified_superconductors"] == 0
    assert PROGRAM["security"]["worker_status"] == "ADMISSION_AND_PLANNING_IMPLEMENTED_EXECUTION_DISABLED"
    assert PROGRAM["implementation"]["signed_result_verification"] == "IMPLEMENTED"
    assert PROGRAM["implementation"]["public_job_execution"] == "DISABLED"


def test_quiet_compute_program_rejects_an_enabled_public_worker():
    changed = copy.deepcopy(PROGRAM)
    changed["current_evidence"]["public_volunteer_worker_enabled"] = True
    changed["security"]["public_code_execution"] = "ENABLED"
    assert errors_for(changed)


def test_quiet_compute_program_rejects_unknown_claim_fields():
    changed = copy.deepcopy(PROGRAM)
    changed["claimed_solution"] = "SUPERCONDUCTOR"
    assert errors_for(changed)
