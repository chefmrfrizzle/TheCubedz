from __future__ import annotations

import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import __version__
from .canonical import scientific_payload, sha256_hex
from .matrix import as_fraction_matrix, determinant, inverse, is_square, is_symmetric, json_matrix
from .schema_validation import validate_candidate_schema

VALIDATOR_NAME = "deterministic-baseline-validator"
PROFILE = "benchmark.minkowski_cartesian_v1"
EXPECTED_MINKOWSKI = as_fraction_matrix([
    [-1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])


def _check(check_id: str, category: str, status: str, summary: str, method: str, scope: str, observed: Any, expected: Any) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "category": category,
        "status": status,
        "summary": summary,
        "method": method,
        "scope": scope,
        "observed": observed,
        "expected": expected,
    }


def _source_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNAVAILABLE"


def evaluate(candidate: dict[str, Any], *, reproducible: bool = False, source_commit: str | None = None) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    schema_errors = validate_candidate_schema(candidate)
    checks.append(_check(
        "schema.candidate.v1", "definition", "PASS" if not schema_errors else "FAIL",
        "Candidate matches the versioned candidate schema." if not schema_errors else "Candidate violates the versioned candidate schema.",
        "JSON Schema Draft 2020-12 validation", "Document shape, required fields, enums, patterns, and declared formats.",
        "no schema violations" if not schema_errors else schema_errors, "no schema violations",
    ))
    if schema_errors:
        errors.extend(schema_errors)

    matrix_values = candidate.get("metric", {}).get("components", [])
    try:
        matrix = as_fraction_matrix(matrix_values)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        matrix = []
        errors.append(f"metric components are not exact numeric values: {exc}")

    coordinate_count = len(candidate.get("coordinates", []))
    dimensions_ok = is_square(matrix) and len(matrix) == coordinate_count
    checks.append(_check(
        "metric.dimension", "mathematics", "PASS" if dimensions_ok else "FAIL",
        "Metric dimensions agree with the declared coordinate count." if dimensions_ok else "Metric dimensions do not agree with the coordinates.",
        "Exact matrix shape comparison", "Submitted component matrix only.",
        f"{len(matrix)} rows for {coordinate_count} coordinates", f"{coordinate_count} by {coordinate_count}",
    ))

    symmetry_ok = dimensions_ok and is_symmetric(matrix)
    checks.append(_check(
        "metric.symmetry", "mathematics", "PASS" if symmetry_ok else "FAIL",
        "Metric components are symmetric." if symmetry_ok else "Metric components are not symmetric.",
        "Exact component comparison g[i,j] = g[j,i]", "Submitted constant component matrix.", symmetry_ok, True,
    ))

    det = determinant(matrix) if dimensions_ok else None
    determinant_ok = det is not None and det != 0
    checks.append(_check(
        "metric.determinant", "mathematics", "PASS" if determinant_ok else "FAIL",
        "Metric is non-degenerate." if determinant_ok else "Metric is degenerate or unavailable.",
        "Exact fraction-preserving Gaussian elimination", "Submitted constant component matrix.",
        int(det) if det is not None and det.denominator == 1 else str(det), "non-zero",
    ))

    try:
        inverse_matrix = inverse(matrix) if dimensions_ok else None
    except ValueError:
        inverse_matrix = None
    inverse_ok = inverse_matrix is not None
    checks.append(_check(
        "metric.inverse", "mathematics", "PASS" if inverse_ok else "FAIL",
        "An exact inverse exists for the submitted matrix." if inverse_ok else "No exact inverse exists.",
        "Gauss-Jordan elimination using rational arithmetic", "Submitted constant component matrix.",
        json_matrix(inverse_matrix) if inverse_matrix else None, "an exact inverse matrix",
    ))

    profile_ok = candidate.get("validation_profile") == PROFILE
    components_ok = profile_ok and matrix == EXPECTED_MINKOWSKI
    checks.append(_check(
        "minkowski.components", "benchmark", "PASS" if components_ok else "FAIL",
        "Components match the declared Minkowski Cartesian baseline." if components_ok else "Components do not match the selected baseline profile.",
        "Exact matrix equality under the selected validation profile", "Minkowski benchmark profile only; no coordinate transformation is attempted.",
        json_matrix(matrix) if matrix else None, json_matrix(EXPECTED_MINKOWSKI),
    ))

    signature_ok = candidate.get("conventions", {}).get("metric_signature") == "-+++"
    checks.append(_check(
        "minkowski.signature", "benchmark", "PASS" if signature_ok else "FAIL",
        "Declared signature matches the baseline profile." if signature_ok else "Declared signature does not match the profile.",
        "Declared convention comparison", "Minkowski Cartesian benchmark profile only.",
        candidate.get("conventions", {}).get("metric_signature"), "-+++",
    ))

    lambda_ok = candidate.get("conventions", {}).get("cosmological_constant") == 0
    checks.append(_check(
        "minkowski.cosmological_constant", "benchmark", "PASS" if lambda_ok else "FAIL",
        "Cosmological constant is zero for this baseline." if lambda_ok else "Cosmological constant is not zero.",
        "Declared convention comparison", "Minkowski vacuum baseline profile only.",
        candidate.get("conventions", {}).get("cosmological_constant"), 0,
    ))

    constants_ok = bool(matrix) and all(value.denominator != 0 for row in matrix for value in row)
    checks.append(_check(
        "minkowski.constant_components", "analytic implication", "PASS" if constants_ok else "FAIL",
        "All submitted components are coordinate-independent constants." if constants_ok else "Components are not supported numeric constants.",
        "Schema-limited inspection of numeric component literals", "This profile accepts numeric constants only; symbolic expressions are not supported.", constants_ok, True,
    ))

    connection_ok = components_ok and constants_ok
    checks.append(_check(
        "minkowski.connection", "analytic implication", "PASS" if connection_ok else "FAIL",
        "Christoffel symbols vanish in the declared Cartesian inertial coordinates." if connection_ok else "The profile does not establish a vanishing connection.",
        "Analytic implication: derivatives of constant metric components are zero.", "Only the exact submitted Minkowski Cartesian profile.",
        "all Γ^ρ_{μν} = 0" if connection_ok else "not established", "all Γ^ρ_{μν} = 0",
    ))

    curvature_ok = connection_ok
    checks.append(_check(
        "minkowski.curvature", "analytic implication", "PASS" if curvature_ok else "FAIL",
        "Riemann, Ricci, scalar curvature, and Einstein tensors vanish for this profile." if curvature_ok else "Vanishing curvature is not established.",
        "Analytic implication from the vanishing connection and its derivatives.", "Only the exact submitted Minkowski Cartesian profile; not a general tensor engine.",
        {"riemann": "0", "ricci": "0", "ricci_scalar": 0, "einstein_tensor": "0"} if curvature_ok else "not established", "all zero",
    ))

    vacuum_ok = curvature_ok and lambda_ok
    checks.append(_check(
        "minkowski.vacuum_source", "physical interpretation", "PASS" if vacuum_ok else "FAIL",
        "The profile is consistent with a zero stress-energy tensor under Λ = 0." if vacuum_ok else "A zero vacuum source is not established.",
        "Einstein field equation implication for Gμν = 0 and Λ = 0.", "Classical general relativity under the declared conventions.",
        "Tμν = 0" if vacuum_ok else "not established", "Tμν = 0",
    ))

    failed = [item for item in checks if item["status"] == "FAIL"]
    overall_status = "BASELINE_VERIFIED" if not failed else "VALIDATION_FAILED"
    assessment = {
        "overall_status": overall_status,
        "mathematics_status": "PASSED_IMPLEMENTED_MINKOWSKI_BASELINE_CHECKS" if not failed else "FAILED_ONE_OR_MORE_IMPLEMENTED_CHECKS",
        "physical_status": "VACUUM_BASELINE_ONLY" if vacuum_ok else "NOT_ESTABLISHED",
        "transportation_status": "NOT_A_TRANSPORTATION_PROPOSAL",
        "statement": (
            "The exact submitted Minkowski Cartesian benchmark passed every implemented V0 check. "
            "This verifies the baseline pipeline, not a general relativity solver or transportation capability."
            if not failed else
            "The submitted candidate failed one or more implemented checks. No mathematical, physical, or transportation conclusion is established."
        ),
    }
    limitations = [
        "The implementation validates one exact constant-component Minkowski benchmark profile.",
        "It does not perform arbitrary coordinate transformations or symbolic tensor calculus.",
        "It does not solve Einstein's equations for general candidate metrics.",
        "It does not evaluate energy conditions, stability, causality, geodesics, or engineering realizability for exotic candidates.",
        "A passing result is a software/reproducibility milestone, not evidence for spacetime transportation.",
    ]
    warnings = [
        "The validator recognizes one exact benchmark representation; it does not prove equivalence under arbitrary coordinate transformations."
    ]
    candidate_hash = sha256_hex(candidate)
    recorded_at = candidate.get("provenance", {}).get("created_at") if reproducible else datetime.now(UTC).isoformat().replace("+00:00", "Z")
    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "result_id": "PENDING",
        "candidate": {"candidate_id": candidate.get("candidate_id"), "version": candidate.get("version"), "sha256": candidate_hash},
        "validator": {"name": VALIDATOR_NAME, "version": __version__, "profile": candidate.get("validation_profile")},
        "checks": checks,
        "assessment": assessment,
        "warnings": warnings,
        "errors": errors,
        "limitations": limitations,
        "run": {
            "recorded_at": recorded_at,
            "command": f"research-core verify candidates/{candidate.get('candidate_id')}.json",
            "python": platform.python_version(),
            "source_commit": source_commit or _source_commit(),
        },
        "scientific_payload_digest": "PENDING",
    }
    digest = sha256_hex(scientific_payload(result))
    result["scientific_payload_digest"] = f"sha256:{digest}"
    result["result_id"] = f"RESULT-{candidate.get('candidate_id')}-{digest[:12].upper()}"
    return result


def load_and_evaluate(path: Path, *, reproducible: bool = False) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = json.loads(path.read_text(encoding="utf-8"))
    return candidate, evaluate(candidate, reproducible=reproducible)
