from __future__ import annotations

import json
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _portable_text_digest(path: Path) -> str:
    normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return f"sha256:{sha256(normalized.encode('utf-8')).hexdigest()}"


def _fraction(value: Any) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("booleans are not exact numeric components")
    return Fraction(value)


def _matrix(values: list[list[Any]]) -> list[list[Fraction]]:
    return [[_fraction(value) for value in row] for row in values]


def _permutation_sign(values: tuple[int, ...]) -> int:
    inversions = sum(values[i] > values[j] for i in range(len(values)) for j in range(i + 1, len(values)))
    return -1 if inversions % 2 else 1


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    if not size or any(len(row) != size for row in matrix):
        raise ValueError("determinant requires a non-empty square matrix")
    total = Fraction(0)
    for ordering in permutations(range(size)):
        product = Fraction(_permutation_sign(ordering))
        for row, column in enumerate(ordering):
            product *= matrix[row][column]
        total += product
    return total


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(column) for column in zip(*matrix, strict=True)]


def multiply(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    columns = transpose(right)
    return [[sum((a * b for a, b in zip(row, column, strict=True)), Fraction(0)) for column in columns] for row in left]


def _minor(matrix: list[list[Fraction]], row: int, column: int) -> list[list[Fraction]]:
    return [[value for j, value in enumerate(values) if j != column] for i, values in enumerate(matrix) if i != row]


def inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    det = determinant(matrix)
    if det == 0:
        raise ValueError("singular matrix")
    size = len(matrix)
    cofactors = [[Fraction((-1) ** (i + j)) * determinant(_minor(matrix, i, j)) for j in range(size)] for i in range(size)]
    return [[cofactors[j][i] / det for j in range(size)] for i in range(size)]


def _plain(value: Fraction) -> int | str:
    return value.numerator if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _plain_matrix(matrix: list[list[Fraction]]) -> list[list[int | str]]:
    return [[_plain(value) for value in row] for row in matrix]


def _validation_contract(passport: dict[str, Any]) -> dict[str, Any]:
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


def _digest(value: Any) -> str:
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return f"sha256:{sha256(canonical).hexdigest()}"


def evaluate_checks(candidate: dict[str, Any], passport: dict[str, Any]) -> dict[str, Any]:
    matrix = _matrix(candidate["metric"]["components"])
    coordinate_map = candidate["parameters"]["coordinate_map"]
    jacobian = _matrix(coordinate_map["jacobian"])
    expected = passport["expected_results"]
    expected_reference = _matrix(expected["reference_metric"])
    expected_jacobian = _matrix(expected["jacobian"])
    expected_metric = _matrix(expected["submitted_metric"])
    expected_inverse = _matrix(expected["submitted_inverse"])
    pulled_back = multiply(multiply(transpose(jacobian), expected_reference), jacobian)
    matrix_det = determinant(matrix)
    jacobian_det = determinant(jacobian)
    expected_jacobian_det = determinant(expected_jacobian)
    computed_inverse = inverse(matrix)
    square = len(matrix) == 4 and all(len(row) == 4 for row in matrix)
    symmetric = square and all(matrix[i][j] == matrix[j][i] for i in range(4) for j in range(4))
    coordinates_ok = (
        coordinate_map["from_coordinates"] == candidate["coordinates"] == expected["from_coordinates"] == passport["domain"]["coordinates"]
        and coordinate_map["to_coordinates"] == expected["to_coordinates"]
        and coordinate_map["relation"] == expected["coordinate_relation"]
    )
    exact_jacobian = jacobian == expected_jacobian and jacobian_det == expected_jacobian_det != 0
    exact_pullback = matrix == expected_metric and pulled_back == expected_metric
    signature = candidate["conventions"]["metric_signature"] == expected["metric_signature"]
    cosmological_constant = candidate["conventions"]["cosmological_constant"] == passport["source_model"]["cosmological_constant"]
    constants = all(
        isinstance(value, (int, float)) and not isinstance(value, bool)
        for row in candidate["metric"]["components"] + coordinate_map["jacobian"]
        for value in row
    )
    connection = exact_pullback and exact_jacobian and constants and expected["connection"] == "all zero"
    curvature = connection and expected["curvature"] == "all zero"
    vacuum = (
        curvature
        and cosmological_constant
        and expected["stress_energy"] == "all zero"
        and passport["source_model"]["stress_energy"] == "T_mu_nu = 0"
    )
    checks = {
        "metric.dimension": square,
        "metric.symmetry": symmetric,
        "metric.determinant": matrix_det == Fraction(expected["submitted_determinant"]),
        "metric.inverse": computed_inverse == expected_inverse,
        "coordinate_map.coordinates": coordinates_ok,
        "coordinate_map.jacobian": exact_jacobian,
        "coordinate_map.pullback": exact_pullback,
        "minkowski.signature": signature,
        "minkowski.cosmological_constant": cosmological_constant,
        "minkowski.constant_components": constants,
        "minkowski.connection": connection,
        "minkowski.curvature": curvature,
        "minkowski.vacuum_source": vacuum,
    }
    return {
        "checks": checks,
        "metric_determinant": _plain(matrix_det),
        "metric_inverse": _plain_matrix(computed_inverse),
        "jacobian": _plain_matrix(jacobian),
        "jacobian_determinant": _plain(jacobian_det),
        "pullback": _plain_matrix(pulled_back),
        "validation_contract_sha256": _digest(_validation_contract(passport)),
    }


def run_crosscheck() -> dict[str, Any]:
    candidate_path = ROOT / "candidates" / "CANDIDATE-000002.json"
    result_path = ROOT / "artifacts" / "results" / "CANDIDATE-000002.result.json"
    passport_path = ROOT / "benchmarks" / "BENCHMARK-000002.passport.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    passport = json.loads(passport_path.read_text(encoding="utf-8"))
    reference = json.loads(result_path.read_text(encoding="utf-8"))
    evaluation = evaluate_checks(candidate, passport)
    independent = evaluation["checks"]
    reference_status = {item["check_id"]: item["status"] for item in reference["checks"]}
    excluded_reference_checks = sorted(set(reference_status) - set(independent))
    discrepancies = [
        check_id for check_id, passed in independent.items()
        if ("PASS" if passed else "FAIL") != reference_status.get(check_id)
    ]
    reference_binding = reference.get("validator", {}).get("benchmark_passport", {})
    expected_binding = {
        "passport_id": passport["passport_id"],
        "passport_version": passport["passport_version"],
        "validation_contract_sha256": evaluation["validation_contract_sha256"],
    }
    if reference_binding != expected_binding:
        discrepancies.append("validator.benchmark_passport")
    payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "reproduction_id": "REPRODUCTION-C000002-INDEPENDENT-PATH-001",
        "candidate_id": candidate["candidate_id"],
        "source_result_id": reference["result_id"],
        "source_scientific_payload_digest": reference["scientific_payload_digest"],
        "candidate_file_sha256": _portable_text_digest(candidate_path),
        "source_candidate_payload_sha256": f"sha256:{reference['candidate']['sha256']}",
        "passport_file_sha256": _portable_text_digest(passport_path),
        "validation_contract_sha256": evaluation["validation_contract_sha256"],
        "implementation": {
            "name": "standard-library-leibniz-coordinate-pullback-crosscheck",
            "version": "1.2.0",
            "shared_research_core_code": False,
            "method": "Independent Leibniz determinant, cofactor inverse, transpose, exact passport comparison, and matrix multiplication using fractions.Fraction; input file hashes normalize UTF-8 line endings to LF",
        },
        "independence": {
            "separate_environment": False,
            "separate_implementation": True,
            "separate_solver": False,
            "separate_contributor": False,
            "level": "R2_IMPLEMENTATION_PATH_ONLY",
            "counts_as_external_reproduction": False,
        },
        "comparison_scope": {
            "reference_check_count": len(reference_status),
            "compared_check_count": len(independent),
            "compared_reference_checks": list(independent),
            "excluded_reference_checks": excluded_reference_checks,
            "schema_conformance_crosschecked": False,
            "exclusion_reason": "This standard-library arithmetic path does not implement JSON Schema Draft 2020-12; schema.candidate.v1 remains a primary-validator-only check.",
        },
        "observations": {
            "metric_determinant": evaluation["metric_determinant"],
            "metric_inverse": evaluation["metric_inverse"],
            "jacobian": evaluation["jacobian"],
            "jacobian_determinant": evaluation["jacobian_determinant"],
            "pullback": evaluation["pullback"],
            "checks": {check_id: "PASS" if passed else "FAIL" for check_id, passed in independent.items()},
        },
        "comparison": "MATCH" if not discrepancies and excluded_reference_checks == ["schema.candidate.v1"] else "MISMATCH",
        "discrepancies": discrepancies,
        "limitations": [
            "This is a separate arithmetic implementation path created in the same repository and environment.",
            "It does not implement or claim an independent Draft 2020-12 schema validation.",
            "It is not an outside reproduction and does not increase the public independent-reproduction count.",
            "It checks only the preregistered constant linear coordinate map for an established flat-spacetime benchmark.",
        ],
    }
    payload["record_digest"] = _digest(payload)
    return payload
