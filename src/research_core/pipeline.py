from __future__ import annotations

import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import __version__
from .canonical import scientific_payload, sha256_hex
from .matrix import as_fraction_matrix, determinant, inverse, is_square, is_symmetric, json_matrix, pullback
from .schema_validation import validate_benchmark_passport_schema, validate_candidate_schema

VALIDATOR_NAME = "deterministic-baseline-validator"
PROFILE = "benchmark.minkowski_cartesian_v1"
LINEAR_PROFILE = "benchmark.minkowski_linear_rescaled_v1"
ROOT = Path(__file__).resolve().parents[2]
LINEAR_PASSPORT_PATH = ROOT / "benchmarks" / "BENCHMARK-000002.passport.json"
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


def _load_linear_passport(path: Path = LINEAR_PASSPORT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _passport_validation_contract(passport: dict[str, Any]) -> dict[str, Any]:
    """Return only the stable fields that define the benchmark calculation."""
    return {
        "schema_version": passport.get("schema_version"),
        "passport_id": passport.get("passport_id"),
        "passport_version": passport.get("passport_version"),
        "benchmark_id": passport.get("benchmark_id"),
        "candidate_id": passport.get("candidate_id"),
        "classification": passport.get("classification"),
        "domain": passport.get("domain"),
        "source_model": passport.get("source_model"),
        "expected_results": passport.get("expected_results"),
        "preregistered_checks": passport.get("preregistered_checks"),
        "negative_cases": passport.get("negative_cases"),
        "unsupported_properties": passport.get("unsupported_properties"),
    }


def _replace_check(checks: list[dict[str, Any]], check_id: str, replacement: dict[str, Any]) -> None:
    index = next(index for index, check in enumerate(checks) if check["check_id"] == check_id)
    checks[index] = replacement


def _linear_coordinate_result(
    candidate: dict[str, Any],
    passport: dict[str, Any],
    matrix: list[list[Any]],
    checks: list[dict[str, Any]],
    errors: list[str],
    *,
    reproducible: bool,
    source_commit: str | None,
) -> dict[str, Any]:
    passport_errors = validate_benchmark_passport_schema(passport)
    if passport_errors:
        errors.extend(f"benchmark passport: {message}" for message in passport_errors)
    expected = passport.get("expected_results", {})
    try:
        expected_reference = as_fraction_matrix(expected.get("reference_metric", []))
        expected_jacobian = as_fraction_matrix(expected.get("jacobian", []))
        expected_metric = as_fraction_matrix(expected.get("submitted_metric", []))
        expected_inverse = as_fraction_matrix(expected.get("submitted_inverse", []))
        expected_determinant = determinant(expected_metric)
        expected_jacobian_determinant = determinant(expected_jacobian)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        expected_reference = []
        expected_jacobian = []
        expected_metric = []
        expected_inverse = []
        expected_determinant = None
        expected_jacobian_determinant = None
        errors.append(f"benchmark passport expected values are invalid: {exc}")
    passport_identity_ok = (
        not passport_errors
        and passport.get("candidate_id") == candidate.get("candidate_id")
        and passport.get("classification") == "ESTABLISHED_NON_NOVEL_GEOMETRY"
        and expected.get("tolerance") == "exact rational equality"
        and expected_reference == EXPECTED_MINKOWSKI
    )

    submitted_determinant = determinant(matrix) if is_square(matrix) else None
    exact_determinant_ok = (
        passport_identity_ok
        and expected_determinant is not None
        and expected.get("submitted_determinant") == int(expected_determinant)
        and submitted_determinant == expected_determinant
    )
    _replace_check(checks, "metric.determinant", _check(
        "metric.determinant", "mathematics", "PASS" if exact_determinant_ok else "FAIL",
        "Metric determinant exactly matches the benchmark passport." if exact_determinant_ok else "Metric determinant does not match the benchmark passport.",
        "Exact fraction-preserving Gaussian elimination and passport comparison", "Submitted metric and versioned benchmark passport only.",
        int(submitted_determinant) if submitted_determinant is not None and submitted_determinant.denominator == 1 else str(submitted_determinant),
        int(expected_determinant) if expected_determinant is not None and expected_determinant.denominator == 1 else str(expected_determinant),
    ))

    try:
        submitted_inverse = inverse(matrix) if is_square(matrix) else None
    except ValueError:
        submitted_inverse = None
    exact_inverse_ok = passport_identity_ok and submitted_inverse == expected_inverse
    _replace_check(checks, "metric.inverse", _check(
        "metric.inverse", "mathematics", "PASS" if exact_inverse_ok else "FAIL",
        "Metric inverse exactly matches the benchmark passport." if exact_inverse_ok else "Metric inverse does not match the benchmark passport.",
        "Exact Gauss-Jordan inversion and passport comparison", "Submitted metric and versioned benchmark passport only.",
        json_matrix(submitted_inverse) if submitted_inverse else None, json_matrix(expected_inverse) if expected_inverse else None,
    ))

    coordinate_map = candidate.get("parameters", {}).get("coordinate_map", {})
    from_coordinates = coordinate_map.get("from_coordinates", [])
    to_coordinates = coordinate_map.get("to_coordinates", [])
    coordinates_ok = (
        passport_identity_ok
        and from_coordinates == candidate.get("coordinates") == expected.get("from_coordinates") == passport.get("domain", {}).get("coordinates")
        and to_coordinates == expected.get("to_coordinates")
        and coordinate_map.get("relation") == expected.get("coordinate_relation")
        and len(from_coordinates) == len(matrix) == 4
    )
    checks.append(_check(
        "coordinate_map.coordinates", "coordinate equivalence", "PASS" if coordinates_ok else "FAIL",
        "Coordinate-map labels match both benchmark charts." if coordinates_ok else "Coordinate-map labels do not match the declared benchmark charts.",
        "Exact ordered coordinate-list comparison", "The approved four-dimensional linear-rescaling profile only.",
        {"from": from_coordinates, "to": to_coordinates, "relation": coordinate_map.get("relation")},
        {"from": expected.get("from_coordinates"), "to": expected.get("to_coordinates"), "relation": expected.get("coordinate_relation")},
    ))

    try:
        jacobian = as_fraction_matrix(coordinate_map.get("jacobian", []))
        jacobian_determinant = determinant(jacobian) if is_square(jacobian) and len(jacobian) == 4 else None
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        jacobian = []
        jacobian_determinant = None
        errors.append(f"coordinate-map Jacobian is not an exact square numeric matrix: {exc}")
    jacobian_ok = (
        passport_identity_ok
        and jacobian == expected_jacobian
        and jacobian_determinant is not None
        and jacobian_determinant == expected_jacobian_determinant
        and jacobian_determinant != 0
    )
    checks.append(_check(
        "coordinate_map.jacobian", "coordinate equivalence", "PASS" if jacobian_ok else "FAIL",
        "The complete Jacobian exactly matches the versioned benchmark passport and is invertible." if jacobian_ok else "The complete Jacobian differs from the benchmark passport, is singular, or is unavailable.",
        "Exact component and determinant comparison against the benchmark passport", "The one preregistered constant four-dimensional linear map only.",
        {"jacobian": json_matrix(jacobian) if jacobian else None, "determinant": int(jacobian_determinant) if jacobian_determinant is not None and jacobian_determinant.denominator == 1 else str(jacobian_determinant)},
        {"jacobian": json_matrix(expected_jacobian) if expected_jacobian else None, "determinant": int(expected_jacobian_determinant) if expected_jacobian_determinant is not None and expected_jacobian_determinant.denominator == 1 else str(expected_jacobian_determinant)},
    ))

    try:
        transformed = pullback(expected_reference, jacobian) if jacobian_ok else None
    except ValueError as exc:
        transformed = None
        errors.append(f"coordinate pullback could not be computed: {exc}")
    pullback_ok = coordinates_ok and matrix == expected_metric and transformed == expected_metric
    checks.append(_check(
        "coordinate_map.pullback", "coordinate equivalence", "PASS" if pullback_ok else "FAIL",
        "The submitted metric and exact pullback both match the benchmark passport." if pullback_ok else "The submitted metric or pullback differs from the benchmark passport.",
        "Exact matrix multiplication and component comparison against the benchmark passport", "One preregistered constant linear map to the canonical Minkowski chart; no arbitrary transformation search.",
        {"submitted": json_matrix(matrix) if matrix else None, "pullback": json_matrix(transformed) if transformed else None},
        {"submitted": json_matrix(expected_metric) if expected_metric else None, "pullback": json_matrix(expected_metric) if expected_metric else None},
    ))

    signature_ok = passport_identity_ok and candidate.get("conventions", {}).get("metric_signature") == expected.get("metric_signature")
    checks.append(_check(
        "minkowski.signature", "benchmark", "PASS" if signature_ok else "FAIL",
        "Declared signature matches the benchmark profile." if signature_ok else "Declared signature does not match the benchmark profile.",
        "Declared convention comparison", "Approved rescaled-coordinate Minkowski profile only.",
        candidate.get("conventions", {}).get("metric_signature"), expected.get("metric_signature"),
    ))

    lambda_ok = passport_identity_ok and candidate.get("conventions", {}).get("cosmological_constant") == passport.get("source_model", {}).get("cosmological_constant")
    checks.append(_check(
        "minkowski.cosmological_constant", "benchmark", "PASS" if lambda_ok else "FAIL",
        "Cosmological constant is zero for this benchmark." if lambda_ok else "Cosmological constant is not zero.",
        "Declared convention comparison", "Minkowski vacuum benchmark only.",
        candidate.get("conventions", {}).get("cosmological_constant"), passport.get("source_model", {}).get("cosmological_constant"),
    ))

    constants_ok = bool(matrix) and bool(jacobian)
    checks.append(_check(
        "minkowski.constant_components", "analytic implication", "PASS" if constants_ok else "FAIL",
        "Metric and Jacobian entries are supported exact constants." if constants_ok else "Metric or Jacobian entries are not supported exact constants.",
        "Schema-limited inspection of numeric literals", "Position-dependent components and symbolic expressions are unsupported.",
        constants_ok, True,
    ))

    connection_ok = pullback_ok and constants_ok and expected.get("connection") == "all zero"
    checks.append(_check(
        "minkowski.connection", "analytic implication", "PASS" if connection_ok else "FAIL",
        "Christoffel symbols vanish in the declared rescaled inertial coordinates." if connection_ok else "A vanishing connection is not established.",
        "Analytic implication from constant metric components", "Only the exact approved constant linear-rescaling profile.",
        "all connection coefficients = 0" if connection_ok else "not established", "all connection coefficients = 0",
    ))

    curvature_ok = connection_ok and expected.get("curvature") == "all zero"
    checks.append(_check(
        "minkowski.curvature", "analytic implication", "PASS" if curvature_ok else "FAIL",
        "Riemann, Ricci, scalar curvature, and Einstein tensors vanish for this profile." if curvature_ok else "Vanishing curvature is not established.",
        "Analytic implication from the vanishing connection and its derivatives", "Only the exact approved constant linear-rescaling profile; not a general tensor engine.",
        {"riemann": "0", "ricci": "0", "ricci_scalar": 0, "einstein_tensor": "0"} if curvature_ok else "not established", "all zero",
    ))

    vacuum_ok = (
        curvature_ok
        and lambda_ok
        and expected.get("stress_energy") == "all zero"
        and passport.get("source_model", {}).get("stress_energy") == "T_mu_nu = 0"
    )
    checks.append(_check(
        "minkowski.vacuum_source", "physical interpretation", "PASS" if vacuum_ok else "FAIL",
        "The profile is consistent with zero stress-energy under a zero cosmological constant." if vacuum_ok else "A zero vacuum source is not established.",
        "Einstein field equation implication for a vanishing Einstein tensor and cosmological constant", "Classical general relativity under the declared conventions.",
        "stress-energy tensor = 0" if vacuum_ok else "not established", "stress-energy tensor = 0",
    ))

    failed = [item for item in checks if item["status"] == "FAIL"]
    assessment = {
        "overall_status": "BENCHMARK_VERIFIED" if not failed else "VALIDATION_FAILED",
        "mathematics_status": "PASSED_IMPLEMENTED_LINEAR_COORDINATE_BENCHMARK_CHECKS" if not failed else "FAILED_ONE_OR_MORE_IMPLEMENTED_CHECKS",
        "physical_status": "VACUUM_BASELINE_ONLY" if vacuum_ok else "NOT_ESTABLISHED",
        "transportation_status": "NOT_A_TRANSPORTATION_PROPOSAL",
        "statement": (
            "The submitted rescaled-coordinate metric exactly matches the declared linear pullback of the canonical Minkowski metric. "
            "This verifies one bounded coordinate-equivalence capability, not a general coordinate solver or transportation capability."
            if not failed else
            "The submitted candidate failed one or more implemented checks. No mathematical, physical, or transportation conclusion is established."
        ),
    }
    limitations = [
        "The implementation validates one preregistered constant linear coordinate map, not arbitrary coordinate transformations.",
        "It does not support position-dependent metric components or symbolic tensor calculus.",
        "It does not solve Einstein's equations for general candidate metrics.",
        "It does not evaluate geodesics, travel time, energy conditions, stability, causality, traveler safety, or engineering realizability.",
        "A passing result shows the same established flat geometry in two representations; it is not a novel-physics result or transportation evidence.",
    ]
    warnings = [
        "Coordinate equivalence is established only for the exact declared constant linear map; nonlinear and inferred transformations remain unsupported."
    ]
    candidate_hash = sha256_hex(candidate)
    recorded_at = candidate.get("provenance", {}).get("created_at") if reproducible else datetime.now(UTC).isoformat().replace("+00:00", "Z")
    validation_contract_digest = f"sha256:{sha256_hex(_passport_validation_contract(passport))}"
    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "result_id": "PENDING",
        "candidate": {"candidate_id": candidate.get("candidate_id"), "version": candidate.get("version"), "sha256": candidate_hash},
        "validator": {
            "name": VALIDATOR_NAME,
            "version": __version__,
            "profile": candidate.get("validation_profile"),
            "benchmark_passport": {
                "passport_id": passport.get("passport_id"),
                "passport_version": passport.get("passport_version"),
                "validation_contract_sha256": validation_contract_digest,
            },
        },
        "checks": checks,
        "assessment": assessment,
        "warnings": warnings,
        "errors": errors,
        "limitations": limitations,
        "run": {
            "recorded_at": recorded_at,
            "command": f"research-core verify candidates/{candidate.get('candidate_id')}.json --passport benchmarks/BENCHMARK-000002.passport.json",
            "python": platform.python_version(),
            "source_commit": source_commit or _source_commit(),
            "benchmark_passport_path": "benchmarks/BENCHMARK-000002.passport.json",
        },
        "scientific_payload_digest": "PENDING",
    }
    digest = sha256_hex(scientific_payload(result))
    result["scientific_payload_digest"] = f"sha256:{digest}"
    result["result_id"] = f"RESULT-{candidate.get('candidate_id')}-{digest[:12].upper()}"
    return result


def evaluate(
    candidate: dict[str, Any],
    *,
    reproducible: bool = False,
    source_commit: str | None = None,
    benchmark_passport: dict[str, Any] | None = None,
) -> dict[str, Any]:
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

    if candidate.get("validation_profile") == LINEAR_PROFILE:
        passport = benchmark_passport if benchmark_passport is not None else _load_linear_passport()
        return _linear_coordinate_result(
            candidate, passport, matrix, checks, errors, reproducible=reproducible, source_commit=source_commit
        )

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


def load_and_evaluate(path: Path, *, reproducible: bool = False, passport_path: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = json.loads(path.read_text(encoding="utf-8"))
    passport = json.loads(passport_path.read_text(encoding="utf-8")) if passport_path is not None else None
    return candidate, evaluate(candidate, reproducible=reproducible, benchmark_passport=passport)
