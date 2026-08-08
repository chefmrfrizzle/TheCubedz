from __future__ import annotations

import json
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _fraction(value: Any) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("booleans are not exact numeric components")
    return Fraction(value)


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
    candidate_path = ROOT / "candidates" / "CANDIDATE-000001.json"
    result_path = ROOT / "artifacts" / "results" / "CANDIDATE-000001.result.json"
    candidate_bytes = candidate_path.read_bytes()
    candidate = json.loads(candidate_bytes)
    reference = json.loads(result_path.read_text(encoding="utf-8"))
    components = candidate["metric"]["components"]
    matrix = [[_fraction(value) for value in row] for row in components]
    expected = [[Fraction(-1), Fraction(0), Fraction(0), Fraction(0)]] + [
        [Fraction(0 if row != column else 1) for column in range(4)] for row in range(1, 4)
    ]
    square = len(matrix) == 4 and all(len(row) == 4 for row in matrix)
    symmetric = square and all(matrix[i][j] == matrix[j][i] for i in range(4) for j in range(4))
    det = determinant(matrix) if square else None
    computed_inverse = inverse(matrix) if det else None
    exact_profile = matrix == expected
    signature = candidate["conventions"]["metric_signature"] == "-+++"
    cosmological_constant = candidate["conventions"]["cosmological_constant"] == 0
    constants = all(isinstance(value, (int, float)) and not isinstance(value, bool) for row in components for value in row)
    connection = exact_profile and constants
    curvature = connection
    vacuum = curvature and cosmological_constant
    independent = {
        "metric.dimension": square,
        "metric.symmetry": symmetric,
        "metric.determinant": det == -1,
        "metric.inverse": computed_inverse == expected,
        "minkowski.components": exact_profile,
        "minkowski.signature": signature,
        "minkowski.cosmological_constant": cosmological_constant,
        "minkowski.constant_components": constants,
        "minkowski.connection": connection,
        "minkowski.curvature": curvature,
        "minkowski.vacuum_source": vacuum,
    }
    reference_status = {item["check_id"]: item["status"] for item in reference["checks"]}
    excluded_reference_checks = sorted(set(reference_status) - set(independent))
    discrepancies = [
        check_id for check_id, passed in independent.items()
        if ("PASS" if passed else "FAIL") != reference_status.get(check_id)
    ]
    payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "reproduction_id": "REPRODUCTION-C000001-INDEPENDENT-PATH-001",
        "candidate_id": candidate["candidate_id"],
        "source_result_id": reference["result_id"],
        "source_scientific_payload_digest": reference["scientific_payload_digest"],
        "candidate_file_sha256": f"sha256:{sha256(candidate_bytes).hexdigest()}",
        "source_candidate_payload_sha256": f"sha256:{reference['candidate']['sha256']}",
        "implementation": {
            "name": "standard-library-leibniz-adjugate-crosscheck",
            "version": "1.1.0",
            "shared_research_core_code": False,
            "method": "Leibniz determinant and cofactor-adjugate inverse using fractions.Fraction",
        },
        "comparison_scope": {
            "reference_check_count": len(reference_status),
            "compared_check_count": len(independent),
            "compared_reference_checks": list(independent),
            "excluded_reference_checks": excluded_reference_checks,
            "schema_conformance_crosschecked": False,
            "exclusion_reason": "This standard-library arithmetic path does not implement JSON Schema Draft 2020-12; schema.candidate.v1 remains a primary-validator-only check.",
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
            "determinant": _plain(det) if det is not None else None,
            "inverse": _plain_matrix(computed_inverse) if computed_inverse else None,
            "checks": {check_id: "PASS" if passed else "FAIL" for check_id, passed in independent.items()},
        },
        "comparison": "MATCH" if not discrepancies and excluded_reference_checks == ["schema.candidate.v1"] else "MISMATCH",
        "discrepancies": discrepancies,
        "limitations": [
            "This is a separate implementation path created in the same repository and environment.",
            "It does not implement or claim an independent Draft 2020-12 schema validation.",
            "It is not an outside reproduction and does not increase the public independent-reproduction count.",
            "It checks only the exact submitted Minkowski Cartesian benchmark.",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    payload["record_digest"] = f"sha256:{sha256(canonical).hexdigest()}"
    return payload
