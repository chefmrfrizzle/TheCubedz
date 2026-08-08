from __future__ import annotations

import json
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _matrix(values: list[list[Any]]) -> list[list[Fraction]]:
    return [[Fraction(value) for value in row] for row in values]


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


def run_crosscheck() -> dict[str, Any]:
    candidate_path = ROOT / "candidates" / "CANDIDATE-000002.json"
    result_path = ROOT / "artifacts" / "results" / "CANDIDATE-000002.result.json"
    candidate_bytes = candidate_path.read_bytes()
    candidate = json.loads(candidate_bytes)
    reference = json.loads(result_path.read_text(encoding="utf-8"))

    matrix = _matrix(candidate["metric"]["components"])
    coordinate_map = candidate["parameters"]["coordinate_map"]
    jacobian = _matrix(coordinate_map["jacobian"])
    eta = _matrix([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    pulled_back = multiply(multiply(transpose(jacobian), eta), jacobian)
    matrix_det = determinant(matrix)
    jacobian_det = determinant(jacobian)
    computed_inverse = inverse(matrix)
    square = len(matrix) == 4 and all(len(row) == 4 for row in matrix)
    symmetric = square and all(matrix[i][j] == matrix[j][i] for i in range(4) for j in range(4))
    coordinates_ok = coordinate_map["from_coordinates"] == candidate["coordinates"] and coordinate_map["to_coordinates"] == ["t", "x", "y", "z"]
    exact_pullback = pulled_back == matrix
    signature = candidate["conventions"]["metric_signature"] == "-+++"
    cosmological_constant = candidate["conventions"]["cosmological_constant"] == 0
    constants = all(isinstance(value, (int, float)) and not isinstance(value, bool) for row in candidate["metric"]["components"] + coordinate_map["jacobian"] for value in row)
    connection = exact_pullback and constants
    curvature = connection
    vacuum = curvature and cosmological_constant
    required = {
        "schema_version", "candidate_id", "version", "title", "status", "intended_use",
        "validation_profile", "coordinates", "coordinate_system", "conventions", "metric",
        "parameters", "assumptions", "claims", "falsification", "references", "provenance",
    }
    independent = {
        "schema.candidate.v1": required.issubset(candidate),
        "metric.dimension": square,
        "metric.symmetry": symmetric,
        "metric.determinant": matrix_det == -14400,
        "metric.inverse": computed_inverse == _matrix([[Fraction(-1, 4), 0, 0, 0], [0, Fraction(1, 9), 0, 0], [0, 0, Fraction(1, 16), 0], [0, 0, 0, Fraction(1, 25)]]),
        "coordinate_map.coordinates": coordinates_ok,
        "coordinate_map.jacobian": jacobian_det == 120,
        "coordinate_map.pullback": exact_pullback,
        "minkowski.signature": signature,
        "minkowski.cosmological_constant": cosmological_constant,
        "minkowski.constant_components": constants,
        "minkowski.connection": connection,
        "minkowski.curvature": curvature,
        "minkowski.vacuum_source": vacuum,
    }
    reference_status = {item["check_id"]: item["status"] for item in reference["checks"]}
    discrepancies = [
        check_id for check_id, passed in independent.items()
        if ("PASS" if passed else "FAIL") != reference_status.get(check_id)
    ]
    payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "reproduction_id": "REPRODUCTION-C000002-INDEPENDENT-PATH-001",
        "candidate_id": candidate["candidate_id"],
        "source_result_id": reference["result_id"],
        "source_scientific_payload_digest": reference["scientific_payload_digest"],
        "candidate_file_sha256": f"sha256:{sha256(candidate_bytes).hexdigest()}",
        "source_candidate_payload_sha256": f"sha256:{reference['candidate']['sha256']}",
        "implementation": {
            "name": "standard-library-leibniz-coordinate-pullback-crosscheck",
            "version": "1.0.0",
            "shared_research_core_code": False,
            "method": "Independent Leibniz determinant, cofactor inverse, transpose, and matrix multiplication using fractions.Fraction",
        },
        "independence": {
            "separate_environment": False,
            "separate_implementation": True,
            "separate_solver": False,
            "separate_contributor": False,
            "level": "R2_IMPLEMENTATION_PATH_ONLY",
            "counts_as_external_reproduction": False,
        },
        "observations": {
            "metric_determinant": _plain(matrix_det),
            "metric_inverse": _plain_matrix(computed_inverse),
            "jacobian_determinant": _plain(jacobian_det),
            "pullback": _plain_matrix(pulled_back),
            "checks": {check_id: "PASS" if passed else "FAIL" for check_id, passed in independent.items()},
        },
        "comparison": "MATCH" if not discrepancies else "MISMATCH",
        "discrepancies": discrepancies,
        "limitations": [
            "This is a separate implementation path created in the same repository and environment.",
            "It is not an outside reproduction and does not increase the public independent-reproduction count.",
            "It checks only one exact constant linear coordinate map for an established flat-spacetime benchmark.",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    payload["record_digest"] = f"sha256:{sha256(canonical).hexdigest()}"
    return payload
