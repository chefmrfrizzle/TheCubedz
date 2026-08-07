from __future__ import annotations

from typing import Any


def beginner_report(candidate: dict[str, Any], result: dict[str, Any]) -> str:
    passed = sum(check["status"] == "PASS" for check in result["checks"])
    failed = sum(check["status"] == "FAIL" for check in result["checks"])
    limitations = "\n".join(f"- {item}" for item in result["limitations"])
    return f"""# {candidate['candidate_id']} — beginner report

## What did we test?

We tested the project's first baseline: ordinary flat spacetime, written as a four-by-four matrix. This candidate is the empty test track for the research system. It is not a shortcut to Mars.

## What happened?

- Implemented checks passed: **{passed}**
- Implemented checks failed: **{failed}**
- Recorded warnings: **{len(result['warnings'])}**
- Overall result: **{result['assessment']['overall_status']}**

{result['assessment']['statement']}

## Why begin here?

Before a search system examines unusual ideas, it must show that it can represent, hash, check, explain, and reproduce a simple known baseline without changing the result.

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
    return f"""# {candidate['candidate_id']} — technical report

## Candidate

- Title: **{candidate['title']}**
- Candidate version: `{candidate['version']}`
- Candidate SHA-256: `{result['candidate']['sha256']}`
- Validation profile: `{candidate['validation_profile']}`
- Validator: `{result['validator']['name']}@{result['validator']['version']}`
- Scientific payload: `{result['scientific_payload_digest']}`

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
