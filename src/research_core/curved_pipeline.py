from __future__ import annotations

import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import sympy
from jsonschema import Draft202012Validator, FormatChecker

from .canonical import scientific_payload, sha256_hex
from .safe_symbolic import expressions_equal, matrices_equal, parse_symbolic, parse_symbolic_matrix
from .symbolic_tensor import compute_geometry, matrix_all_zero, nonzero_rank3, tensor_all_zero

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_NAME = "symbolic-curved-benchmark-validator"
VALIDATOR_VERSION = "0.1.0"
PROFILE = "benchmark.schwarzschild_exterior_v1"
PASSPORT_CONTRACT_SHA256 = "d8f983d51a22fbb9dd36912da31d5593843c4e9cdb5f45fdbeb6309e1df01e21"


def _check(check_id: str, category: str, passed: bool, summary: str, method: str, scope: str, observed: Any, expected: Any) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "category": category,
        "status": "PASS" if passed else "FAIL",
        "summary": summary,
        "method": method,
        "scope": scope,
        "observed": observed,
        "expected": expected,
    }


def _schema_errors(document: dict[str, Any], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.absolute_path))
    return [f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}" for error in errors]


def _source_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNAVAILABLE"


def _passport_contract(passport: dict[str, Any]) -> dict[str, Any]:
    return {
        key: passport.get(key)
        for key in (
            "schema_version", "passport_id", "passport_version", "benchmark_id", "candidate_id",
            "classification", "domain", "conventions", "expected_results", "preregistered_checks",
            "negative_cases", "unsupported_properties",
        )
    }


def _symbols() -> tuple[dict[str, sympy.Symbol], tuple[sympy.Symbol, ...]]:
    t = sympy.Symbol("t", real=True)
    r = sympy.Symbol("r", real=True, positive=True)
    theta = sympy.Symbol("theta", real=True)
    phi = sympy.Symbol("phi", real=True)
    mass = sympy.Symbol("M", real=True, positive=True)
    return {"t": t, "r": r, "theta": theta, "phi": phi, "M": mass}, (t, r, theta, phi)


def _parse_index(index: str, rank: int) -> tuple[int, ...]:
    parts = tuple(int(part) for part in index.split(","))
    if len(parts) != rank or any(part < 0 or part > 3 for part in parts):
        raise ValueError(f"invalid rank-{rank} tensor index: {index}")
    return parts


def _expr(value: sympy.Expr | None) -> str | None:
    return None if value is None else str(value)


def evaluate_curved(
    candidate: dict[str, Any],
    passport: dict[str, Any],
    *,
    reproducible: bool = False,
    source_commit: str | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    candidate_schema_errors = _schema_errors(candidate, ROOT / "src" / "core" / "candidate-v2.schema.json")
    passport_schema_errors = _schema_errors(passport, ROOT / "src" / "core" / "curved-benchmark-passport.schema.json")
    checks.append(_check(
        "schema.candidate.v2", "definition", not candidate_schema_errors,
        "Candidate matches the curved-benchmark schema." if not candidate_schema_errors else "Candidate violates the curved-benchmark schema.",
        "JSON Schema Draft 2020-12 validation", "Document structure and fixed Schwarzschild profile declarations.",
        candidate_schema_errors or "no schema violations", "no schema violations",
    ))
    checks.append(_check(
        "schema.passport.curved.v1", "definition", not passport_schema_errors,
        "Passport matches the curved-benchmark passport schema." if not passport_schema_errors else "Passport violates its schema.",
        "JSON Schema Draft 2020-12 validation", "Passport structure, identifiers, and expected-value fields.",
        passport_schema_errors or "no schema violations", "no schema violations",
    ))
    errors.extend(f"candidate schema: {error}" for error in candidate_schema_errors)
    errors.extend(f"passport schema: {error}" for error in passport_schema_errors)

    contract_digest = sha256_hex(_passport_contract(passport))
    passport_bound = (
        not passport_schema_errors
        and contract_digest == PASSPORT_CONTRACT_SHA256
        and passport.get("candidate_id") == candidate.get("candidate_id")
        and passport.get("passport_id") == "PASSPORT-000003"
        and passport.get("passport_version") == "1.0.0"
    )
    if not passport_bound:
        errors.append("passport does not match the preregistered PASSPORT-000003@1.0.0 scientific contract")

    symbols, coordinates = _symbols()
    expected = passport.get("expected_results", {})
    metric: sympy.Matrix | None = None
    expected_metric: sympy.Matrix | None = None
    expected_inverse: sympy.Matrix | None = None
    expected_ricci: sympy.Matrix | None = None
    expected_einstein: sympy.Matrix | None = None
    expected_determinant: sympy.Expr | None = None
    expected_scalar: sympy.Expr | None = None
    expected_kretschmann: sympy.Expr | None = None
    geometry = None
    try:
        metric = parse_symbolic_matrix(candidate.get("metric", {}).get("components", []), symbols)
        expected_metric = parse_symbolic_matrix(expected.get("metric", []), symbols)
        expected_inverse = parse_symbolic_matrix(expected.get("inverse_metric", []), symbols)
        expected_ricci = parse_symbolic_matrix(expected.get("ricci_tensor", []), symbols)
        expected_einstein = parse_symbolic_matrix(expected.get("einstein_tensor", []), symbols)
        expected_determinant = parse_symbolic(expected.get("metric_determinant"), symbols)
        expected_scalar = parse_symbolic(expected.get("ricci_scalar"), symbols)
        expected_kretschmann = parse_symbolic(expected.get("kretschmann_scalar"), symbols)
        geometry = compute_geometry(metric, coordinates)
    except (TypeError, ValueError, ZeroDivisionError, sympy.SympifyError) as exc:
        errors.append(f"symbolic benchmark calculation failed safely: {exc}")

    dimensions_ok = metric is not None and metric.shape == (4, 4)
    checks.append(_check(
        "metric.dimension", "mathematics", dimensions_ok,
        "Metric has one row and column per coordinate." if dimensions_ok else "Metric dimensions do not match four coordinates.",
        "Exact matrix shape comparison", "Four-dimensional Schwarzschild exterior profile only.",
        list(metric.shape) if metric is not None else None, [4, 4],
    ))
    symmetry_ok = dimensions_ok and metric == metric.T
    checks.append(_check(
        "metric.symmetry", "mathematics", bool(symmetry_ok),
        "Metric is symmetric." if symmetry_ok else "Metric is not established as symmetric.",
        "Exact symbolic component comparison", "Submitted metric matrix only.", bool(symmetry_ok), True,
    ))
    components_ok = passport_bound and metric is not None and expected_metric is not None and matrices_equal(metric, expected_metric)
    checks.append(_check(
        "metric.components", "benchmark", components_ok,
        "Every metric component matches the preregistered Schwarzschild exterior metric." if components_ok else "Metric components differ from the bound passport.",
        "Exact symbolic equality after simplification", "One preregistered Schwarzschild curvature-coordinate representation.",
        str(metric) if metric is not None else None, str(expected_metric) if expected_metric is not None else None,
    ))
    determinant_ok = passport_bound and geometry is not None and expected_determinant is not None and expressions_equal(geometry.determinant, expected_determinant)
    checks.append(_check(
        "metric.determinant", "mathematics", determinant_ok,
        "Metric determinant matches the passport." if determinant_ok else "Metric determinant differs or is unavailable.",
        "Symbolic determinant and exact simplification", "Declared exterior chart away from excluded coordinate sets.",
        _expr(geometry.determinant if geometry else None), _expr(expected_determinant),
    ))
    inverse_ok = passport_bound and geometry is not None and expected_inverse is not None and matrices_equal(geometry.inverse_metric, expected_inverse)
    checks.append(_check(
        "metric.inverse", "mathematics", inverse_ok,
        "Inverse metric matches the passport." if inverse_ok else "Inverse metric differs or is unavailable.",
        "Symbolic matrix inversion and exact component comparison", "Declared exterior chart only.",
        str(geometry.inverse_metric) if geometry else None, str(expected_inverse) if expected_inverse is not None else None,
    ))

    domain_ok = passport_bound and candidate.get("domain") == passport.get("domain")
    checks.append(_check(
        "domain.schwarzschild_exterior", "domain", domain_ok,
        "Mass, exterior-radius, angular, horizon, and singularity restrictions match the passport." if domain_ok else "Domain declarations differ from the bound exterior-domain contract.",
        "Exact structured declaration comparison", "M > 0, r > 2M, 0 < theta < pi; exterior patch only.",
        candidate.get("domain"), passport.get("domain"),
    ))
    position_ok = False
    if metric is not None:
        r, theta = symbols["r"], symbols["theta"]
        position_ok = (
            not expressions_equal(sympy.diff(metric[0, 0], r), sympy.Integer(0))
            and not expressions_equal(sympy.diff(metric[3, 3], theta), sympy.Integer(0))
        )
    checks.append(_check(
        "symbolic.position_dependence", "symbolic calculus", position_ok,
        "The metric has verified radial and angular position dependence." if position_ok else "Required position dependence was not established.",
        "Symbolic partial differentiation", "Checks representative derivatives; does not prove arbitrary symbolic support.",
        {"d_r_g_tt_nonzero": position_ok, "d_theta_g_phiphi_nonzero": position_ok}, True,
    ))

    gamma_ok = False
    gamma_observed: dict[str, str] = {}
    try:
        if geometry is not None:
            gamma_values = nonzero_rank3(geometry.christoffel)
            gamma_observed = {key: str(value) for key, value in gamma_values.items()}
            expected_gamma = expected.get("nonzero_christoffel", {})
            gamma_ok = passport_bound and set(gamma_values) == set(expected_gamma) and all(
                expressions_equal(gamma_values[key], parse_symbolic(value, symbols)) for key, value in expected_gamma.items()
            )
    except (TypeError, ValueError) as exc:
        errors.append(f"Christoffel comparison failed safely: {exc}")
    checks.append(_check(
        "connection.christoffel", "symbolic calculus", gamma_ok,
        "The complete nonzero Christoffel set matches the passport." if gamma_ok else "Christoffel symbols differ or are unavailable.",
        "Levi-Civita connection from symbolic first derivatives", "All nonzero components in the declared coordinate order.",
        gamma_observed, expected.get("nonzero_christoffel"),
    ))

    riemann_ok = False
    riemann_observed: dict[str, str] = {}
    try:
        if geometry is not None:
            expected_riemann = expected.get("representative_riemann", {})
            for key, value in expected_riemann.items():
                rho, sigma, mu, nu = _parse_index(key, 4)
                actual = geometry.riemann[rho][sigma][mu][nu]
                riemann_observed[key] = str(actual)
                if not expressions_equal(actual, parse_symbolic(value, symbols)):
                    break
            else:
                riemann_ok = passport_bound and bool(expected_riemann) and not tensor_all_zero(geometry.riemann)
    except (TypeError, ValueError) as exc:
        errors.append(f"Riemann comparison failed safely: {exc}")
    checks.append(_check(
        "curvature.riemann_nonzero", "symbolic calculus", riemann_ok,
        "Curvature is nonzero and every preregistered representative Riemann component matches." if riemann_ok else "The preregistered Riemann comparison failed.",
        "Declared Riemann convention from Christoffel derivatives and products", "Representative components plus a full-tensor nonzero test; not a published dump of all 256 components.",
        riemann_observed, expected.get("representative_riemann"),
    ))
    ricci_ok = passport_bound and geometry is not None and expected_ricci is not None and matrix_all_zero(geometry.ricci) and matrices_equal(geometry.ricci, expected_ricci)
    checks.append(_check(
        "curvature.ricci_zero", "symbolic calculus", ricci_ok,
        "Every Ricci-tensor component vanishes." if ricci_ok else "A Ricci-tensor component differs or is unavailable.",
        "Full contraction R^rho_{sigma rho nu}", "All 16 coordinate components.",
        str(geometry.ricci) if geometry else None, str(expected_ricci) if expected_ricci is not None else None,
    ))
    scalar_ok = passport_bound and geometry is not None and expected_scalar is not None and expressions_equal(geometry.ricci_scalar, expected_scalar)
    checks.append(_check(
        "curvature.ricci_scalar_zero", "symbolic calculus", scalar_ok,
        "Ricci scalar is zero." if scalar_ok else "Ricci scalar differs or is unavailable.",
        "Exact contraction g^mu_nu R_mu_nu", "Declared exterior domain.", _expr(geometry.ricci_scalar if geometry else None), _expr(expected_scalar),
    ))
    einstein_ok = passport_bound and geometry is not None and expected_einstein is not None and matrix_all_zero(geometry.einstein) and matrices_equal(geometry.einstein, expected_einstein)
    checks.append(_check(
        "curvature.einstein_zero", "symbolic calculus", einstein_ok,
        "Every Einstein-tensor component vanishes." if einstein_ok else "Einstein tensor differs or is unavailable.",
        "G_mu_nu = R_mu_nu - (1/2) g_mu_nu R", "All 16 coordinate components.",
        str(geometry.einstein) if geometry else None, str(expected_einstein) if expected_einstein is not None else None,
    ))
    kretschmann_ok = passport_bound and geometry is not None and expected_kretschmann is not None and expressions_equal(geometry.kretschmann, expected_kretschmann)
    checks.append(_check(
        "curvature.kretschmann", "symbolic calculus", kretschmann_ok,
        "Kretschmann scalar matches the established radial curvature invariant." if kretschmann_ok else "Kretschmann scalar differs or is unavailable.",
        "Exact contraction R_abcd R^abcd for the preregistered diagonal metric", "Schwarzschild exterior benchmark only.",
        _expr(geometry.kretschmann if geometry else None), _expr(expected_kretschmann),
    ))
    convention_ok = passport_bound and candidate.get("conventions") == {
        **passport.get("conventions", {}), "speed_of_light": 1, "gravitational_constant": 1
    }
    checks.append(_check(
        "conventions.tensor_signs", "conventions", convention_ok,
        "Signature, Riemann sign, Ricci contraction, units, and cosmological constant match the passport." if convention_ok else "Tensor conventions differ from the preregistered contract.",
        "Exact declaration comparison", "Convention-sensitive component signs are valid only under this contract.",
        candidate.get("conventions"), passport.get("conventions"),
    ))
    vacuum_ok = domain_ok and convention_ok and ricci_ok and scalar_ok and einstein_ok
    checks.append(_check(
        "physics.vacuum_exterior", "physical interpretation", vacuum_ok,
        "The chart satisfies the classical vacuum field equations for Lambda = 0." if vacuum_ok else "Vacuum exterior status is not established.",
        "Einstein equation implication from G_mu_nu = 0 and Lambda = 0", "Only the declared exterior chart; the central matter source is outside this domain.",
        "T_mu_nu = 0 in the declared exterior domain" if vacuum_ok else "not established", "T_mu_nu = 0 in the declared exterior domain",
    ))

    preregistered = passport.get("preregistered_checks", [])
    actual_ids = [check["check_id"] for check in checks]
    if actual_ids != preregistered:
        errors.append("implemented check order does not exactly match the preregistered check list")
        for check in checks:
            check["status"] = "FAIL"
    failed = [check for check in checks if check["status"] == "FAIL"]
    overall = "BENCHMARK_VERIFIED" if not failed and not errors else "VALIDATION_FAILED"
    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "result_id": "PENDING",
        "candidate": {
            "candidate_id": candidate.get("candidate_id"),
            "version": candidate.get("version"),
            "sha256": sha256_hex(candidate),
        },
        "validator": {
            "name": VALIDATOR_NAME,
            "version": VALIDATOR_VERSION,
            "profile": candidate.get("validation_profile"),
            "solver": f"SymPy {sympy.__version__}",
            "benchmark_passport": {
                "passport_id": passport.get("passport_id"),
                "passport_version": passport.get("passport_version"),
                "validation_contract_sha256": f"sha256:{contract_digest}",
                "bound": passport_bound,
            },
        },
        "checks": checks,
        "assessment": {
            "overall_status": overall,
            "mathematics_status": "PASSED_PREREGISTERED_CURVED_BENCHMARK_CHECKS" if overall == "BENCHMARK_VERIFIED" else "FAILED_ONE_OR_MORE_IMPLEMENTED_CHECKS",
            "physical_status": "CURVED_VACUUM_EXTERIOR_BENCHMARK_ONLY" if vacuum_ok else "NOT_ESTABLISHED",
            "transportation_status": "NOT_A_TRANSPORTATION_PROPOSAL",
            "statement": (
                "The established Schwarzschild exterior metric passed the bound symbolic benchmark under the declared domain and tensor conventions. "
                "This calibrates one curved known-answer case; it is not evidence for a novel geometry or transportation mechanism."
                if overall == "BENCHMARK_VERIFIED" else
                "One or more preregistered checks failed. No curved-spacetime, physical, or transportation conclusion is established."
            ),
        },
        "warnings": [
            "Schwarzschild curvature coordinates do not cover the horizon or interior; r = 2M is excluded from this chart.",
            "Coordinate components and signs are convention-sensitive; comparisons use only the declared Riemann and Ricci conventions.",
            "The primary calculation and separate solver comparison are project-internal checks, not independent scientific review.",
        ],
        "errors": errors,
        "limitations": list(passport.get("unsupported_properties", [])) + [
            "A passing known-answer benchmark validates bounded software behavior, not the Mars-distance thesis.",
            "No untrusted symbolic input should be evaluated outside the schema and restricted parser used by this profile.",
        ],
        "run": {
            "recorded_at": candidate.get("provenance", {}).get("created_at") if reproducible else datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "command": "research-core verify candidates/CANDIDATE-000003.json --passport benchmarks/BENCHMARK-000003.passport.json",
            "python": platform.python_version(),
            "source_commit": source_commit or _source_commit(),
        },
        "scientific_payload_digest": "PENDING",
    }
    digest = sha256_hex(scientific_payload(result))
    result["scientific_payload_digest"] = f"sha256:{digest}"
    result["result_id"] = f"RESULT-{candidate.get('candidate_id')}-{digest[:12].upper()}"
    return result


def load_and_evaluate_curved(path: Path, passport_path: Path, *, reproducible: bool = False) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = json.loads(path.read_text(encoding="utf-8"))
    passport = json.loads(passport_path.read_text(encoding="utf-8"))
    return candidate, evaluate_curved(candidate, passport, reproducible=reproducible)
