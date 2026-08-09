from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

import sympy
from sympy import Matrix, Rational

ROOT = Path(__file__).resolve().parents[1]


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _file_digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _record_digest(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _git(root: Path, *args: str) -> str:
    process = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)
    return process.stdout.strip()


def _sympy_matrix(values: list[list[Any]]) -> Matrix:
    def exact(value: Any) -> Any:
        if isinstance(value, bool):
            raise TypeError("boolean matrix components are not numeric evidence")
        if isinstance(value, str) and "/" in value:
            numerator, denominator = value.split("/", 1)
            return Rational(int(numerator), int(denominator))
        return sympy.Integer(value)

    return Matrix([[exact(value) for value in row] for row in values])


def _plain(value: Any) -> int | str:
    simplified = sympy.cancel(value)
    return int(simplified) if simplified.is_Integer else str(simplified)


def _plain_matrix(matrix: Matrix) -> list[list[int | str]]:
    return [[_plain(matrix[row, column]) for column in range(matrix.cols)] for row in range(matrix.rows)]


def evaluate_baseline(root: Path = ROOT) -> dict[str, Any]:
    candidate_path = root / "candidates" / "CANDIDATE-000001.json"
    result_path = root / "artifacts" / "results" / "CANDIDATE-000001.result.json"
    candidate = _json(candidate_path)
    result = _json(result_path)
    metric = _sympy_matrix(candidate["metric"]["components"])
    expected = sympy.diag(-1, 1, 1, 1)
    inverse = metric.inv()
    checks = {
        "metric.dimension": metric.shape == (4, 4),
        "metric.symmetry": metric == metric.T,
        "metric.determinant": metric.det() == -1,
        "metric.inverse": inverse == expected,
        "minkowski.components": metric == expected,
        "minkowski.signature": candidate["conventions"]["metric_signature"] == "-+++",
        "minkowski.cosmological_constant": candidate["conventions"]["cosmological_constant"] == 0,
        "minkowski.constant_components": not any(component.free_symbols for component in metric),
    }
    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_file_sha256": _file_digest(candidate_path),
        "published_scientific_payload_digest": result["scientific_payload_digest"],
        "checks": {check_id: "PASS" if passed else "FAIL" for check_id, passed in checks.items()},
        "observations": {"determinant": _plain(metric.det()), "inverse": _plain_matrix(inverse)},
    }


def evaluate_coordinate(root: Path = ROOT) -> dict[str, Any]:
    candidate_path = root / "candidates" / "CANDIDATE-000002.json"
    result_path = root / "artifacts" / "results" / "CANDIDATE-000002.result.json"
    passport_path = root / "benchmarks" / "BENCHMARK-000002.passport.json"
    candidate = _json(candidate_path)
    result = _json(result_path)
    passport = _json(passport_path)
    expected = passport["expected_results"]
    metric = _sympy_matrix(candidate["metric"]["components"])
    jacobian = _sympy_matrix(candidate["parameters"]["coordinate_map"]["jacobian"])
    reference_metric = _sympy_matrix(expected["reference_metric"])
    expected_metric = _sympy_matrix(expected["submitted_metric"])
    expected_inverse = _sympy_matrix(expected["submitted_inverse"])
    pullback = sympy.simplify(jacobian.T * reference_metric * jacobian)
    checks = {
        "metric.dimension": metric.shape == (4, 4),
        "metric.symmetry": metric == metric.T,
        "metric.determinant": metric.det() == expected["submitted_determinant"],
        "metric.inverse": metric.inv() == expected_inverse,
        "coordinate_map.coordinates": candidate["parameters"]["coordinate_map"]["from_coordinates"] == expected["from_coordinates"] and candidate["parameters"]["coordinate_map"]["to_coordinates"] == expected["to_coordinates"],
        "coordinate_map.jacobian": jacobian == _sympy_matrix(expected["jacobian"]) and jacobian.det() != 0,
        "coordinate_map.pullback": metric == expected_metric and pullback == expected_metric,
    }
    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_file_sha256": _file_digest(candidate_path),
        "passport_file_sha256": _file_digest(passport_path),
        "published_scientific_payload_digest": result["scientific_payload_digest"],
        "checks": {check_id: "PASS" if passed else "FAIL" for check_id, passed in checks.items()},
        "observations": {
            "determinant": _plain(metric.det()),
            "inverse": _plain_matrix(metric.inv()),
            "jacobian_determinant": _plain(jacobian.det()),
            "pullback": _plain_matrix(pullback),
        },
    }


def run(root: Path = ROOT) -> dict[str, Any]:
    baseline = evaluate_baseline(root)
    coordinate = evaluate_coordinate(root)
    all_checks = [*baseline["checks"].values(), *coordinate["checks"].values()]
    payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "reproduction_id": "REPRODUCTION-INTERNAL-CLEAN-CLONE-000001",
        "classification": "INTERNAL_CLEAN_CLONE_SEPARATE_LIBRARY_REPRODUCTION",
        "repository": {
            "url": _git(root, "remote", "get-url", "origin"),
            "commit": _git(root, "rev-parse", "HEAD"),
            "working_tree_clean": _git(root, "status", "--porcelain") == "",
        },
        "environment": {
            "operating_system": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "sympy_version": sympy.__version__,
        },
        "commands": [
            "python scripts/research.py verify candidates/CANDIDATE-000001.json --reproducible",
            "python scripts/research.py verify candidates/CANDIDATE-000002.json --passport benchmarks/BENCHMARK-000002.passport.json --reproducible",
            "python independent/sympy_clean_clone_reproduction.py --json",
        ],
        "implementation": {
            "name": "sympy-clean-clone-matrix-reproduction",
            "library": "SymPy",
            "library_version": sympy.__version__,
            "imports_research_core": False,
            "method": "SymPy Matrix determinant, inverse, transpose, and multiplication directly from raw JSON inputs.",
        },
        "candidates": [baseline, coordinate],
        "comparison": "MATCH" if all(status == "PASS" for status in all_checks) else "MISMATCH",
        "conflict_of_interest": {
            "disclosed": True,
            "operator": "ChefMrFrizzle with Codex",
            "overlaps": [
                "project owner and repository author",
                "same Codex collaborator used for implementation",
                "same physical machine and GitHub credentials",
                "same repository history, despite a clean remote clone",
            ],
        },
        "independence": {
            "clean_remote_clone": True,
            "separate_library": True,
            "separate_implementation": True,
            "separate_machine": False,
            "separate_contributor": False,
            "counts_as_external_reproduction": False,
            "level": "R2_INTERNAL_CLEAN_CLONE_SEPARATE_LIBRARY",
        },
        "signature": {
            "status": "UNSIGNED_NO_KEY",
            "content_digest_is_not_a_signature": True,
            "reason": "No Git signing key, GPG secret key, or SSH-agent signing identity was configured in the reproduction environment.",
        },
        "limitations": [
            "This run is regression and portability evidence, not an outside scientific reproduction.",
            "SymPy is a separate library path, but the same project owner, Codex collaborator, machine, repository history, and credentials were involved.",
            "JSON Schema conformance is not independently reimplemented by this path.",
            "A named outside contributor and verifiable signature remain required for external reproduction credit.",
        ],
    }
    payload["record_digest"] = _record_digest(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Recompute both flat-spacetime candidates with SymPy from a clean clone.")
    parser.add_argument("--json", action="store_true", help="print the complete reproduction record")
    args = parser.parse_args()
    result = run()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"reproduction: {result['reproduction_id']}")
        print(f"comparison: {result['comparison']}")
        print(f"commit: {result['repository']['commit']}")
        print(f"python: {result['environment']['python_version']}")
        print(f"sympy: {result['environment']['sympy_version']}")
        print(f"external reproduction: {result['independence']['counts_as_external_reproduction']}")
        print(f"signature: {result['signature']['status']}")
        print(f"digest: {result['record_digest']}")
    return 0 if result["comparison"] == "MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
