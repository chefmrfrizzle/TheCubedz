from __future__ import annotations

from typing import Any


def beginner_report(candidate: dict[str, Any], result: dict[str, Any]) -> str:
    passed = sum(check["status"] == "PASS" for check in result["checks"])
    failed = sum(check["status"] == "FAIL" for check in result["checks"])
    limitations = "\n".join(f"- {item}" for item in result["limitations"])
    is_coordinate_benchmark = candidate["validation_profile"] == "benchmark.minkowski_linear_rescaled_v1"
    is_curved_benchmark = candidate["validation_profile"] == "benchmark.schwarzschild_exterior_v1"
    tested = (
        "We tested a known curved-spacetime answer: the empty region outside a spherical, non-rotating mass. "
        "The checker calculated how the metric changes from place to place, then checked the connection, curvature, vacuum equations, and a curvature fingerprint."
        if is_curved_benchmark else
        "We tested whether a differently numbered coordinate grid still describes the same ordinary flat spacetime. "
        "The checker used the declared conversion table to transform the original metric and compared every number exactly."
        if is_coordinate_benchmark else
        "We tested the project's first baseline: ordinary flat spacetime, written as a four-by-four matrix. "
        "This candidate is the empty test track for the research system. It is not a shortcut to Mars."
    )
    reason = (
        "Before testing an original spacetime idea, the software must correctly recognize a standard curved example with a known answer and clearly mark where its coordinate chart stops working."
        if is_curved_benchmark else
        "A trustworthy geometry checker must distinguish a real physical difference from a harmless change in coordinate labels or scales."
        if is_coordinate_benchmark else
        "Before a search system examines unusual ideas, it must show that it can represent, hash, check, explain, and reproduce a simple known baseline without changing the result."
    )
    return f"""# {candidate['candidate_id']} — beginner report

## What did we test?

{tested}

## What happened?

- Implemented checks passed: **{passed}**
- Implemented checks failed: **{failed}**
- Recorded warnings: **{len(result['warnings'])}**
- Overall result: **{result['assessment']['overall_status']}**

{result['assessment']['statement']}

## Why begin here?

{reason}

## What this does not prove

{limitations}

## Reproducibility fingerprint

`{result['scientific_payload_digest']}`

This fingerprint covers the candidate identity, validator identity, checks, assessment, warnings, errors, and limitations. Runtime metadata such as the clock time is not allowed to change that scientific payload.
"""


def technical_report(candidate: dict[str, Any], result: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{check['check_id']}` | {check['status']} | {check['summary']} | {check['method']} |"
        for check in result["checks"]
    )
    limitations = "\n".join(f"- {item}" for item in result["limitations"])
    warnings = "\n".join(f"- {item}" for item in result["warnings"]) or "- None"
    errors = "\n".join(f"- {item}" for item in result["errors"]) or "- None"
    passport = result["validator"].get("benchmark_passport")
    passport_lines = (
        f"- Benchmark passport: `{passport['passport_id']}@{passport['passport_version']}`\n"
        f"- Validation-contract digest: `{passport['validation_contract_sha256']}`"
        if passport else
        "- Benchmark passport: `not applicable to this profile`"
    )
    return f"""# {candidate['candidate_id']} — technical report

## Candidate

- Title: **{candidate['title']}**
- Candidate version: `{candidate['version']}`
- Candidate SHA-256: `{result['candidate']['sha256']}`
- Validation profile: `{candidate['validation_profile']}`
- Validator: `{result['validator']['name']}@{result['validator']['version']}`
- Scientific payload: `{result['scientific_payload_digest']}`
{passport_lines}

## Conventions

- Coordinates: `{', '.join(candidate['coordinates'])}`
- Signature: `{candidate['conventions']['metric_signature']}`
- Units: `{candidate['conventions']['units']}`
- Speed of light: `{candidate['conventions']['speed_of_light']}`
- Cosmological constant: `{candidate['conventions']['cosmological_constant']}`

## Implemented checks

| Check | Status | Result | Method |
|---|---|---|---|
{rows}

## Assessment

- Overall: `{result['assessment']['overall_status']}`
- Mathematics: `{result['assessment']['mathematics_status']}`
- Physical scope: `{result['assessment']['physical_status']}`
- Transportation scope: `{result['assessment']['transportation_status']}`

{result['assessment']['statement']}

## Warnings

{warnings}

## Errors

{errors}

## Limitations

{limitations}
"""
