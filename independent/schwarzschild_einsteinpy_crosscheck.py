from __future__ import annotations

import argparse
import ast
import hashlib
import json
import platform
import subprocess
from pathlib import Path
from typing import Any

import einsteinpy
import sympy
from einsteinpy.symbolic import (
    ChristoffelSymbols,
    EinsteinTensor,
    MetricTensor,
    RicciScalar,
    RicciTensor,
    RiemannCurvatureTensor,
)

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_PATH = ROOT / "candidates" / "CANDIDATE-000003.json"
PASSPORT_PATH = ROOT / "benchmarks" / "BENCHMARK-000003.passport.json"
OUTPUT_PATH = ROOT / "artifacts" / "reproductions" / "CANDIDATE-000003.einsteinpy-crosscheck.json"
PASSPORT_CONTRACT_SHA256 = "d8f983d51a22fbb9dd36912da31d5593843c4e9cdb5f45fdbeb6309e1df01e21"


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _source_commit() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def _passport_contract(passport: dict[str, Any]) -> dict[str, Any]:
    return {
        key: passport.get(key)
        for key in (
            "schema_version", "passport_id", "passport_version", "benchmark_id", "candidate_id",
            "classification", "domain", "conventions", "expected_results", "preregistered_checks",
            "negative_cases", "unsupported_properties",
        )
    }


def _parse(value: Any, symbols: dict[str, sympy.Symbol]) -> sympy.Expr:
    """Independent small expression reader; it does not import the primary parser."""
    if isinstance(value, bool):
        raise ValueError("boolean component")
    if isinstance(value, int):
        return sympy.Integer(value)
    if not isinstance(value, str) or len(value) > 160:
        raise ValueError("invalid symbolic component")
    tree = ast.parse(value, mode="eval")
    if sum(1 for _ in ast.walk(tree)) > 80:
        raise ValueError("expression too complex")

    def visit(node: ast.AST) -> sympy.Expr:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
            return sympy.Integer(node.value)
        if isinstance(node, ast.Name) and node.id in symbols:
            return symbols[node.id]
        if isinstance(node, ast.Name) and node.id == "pi":
            return sympy.pi
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            result = visit(node.operand)
            return result if isinstance(node.op, ast.UAdd) else -result
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if not right.is_Integer or abs(int(right)) > 12:
                raise ValueError("unsafe power")
            return left**right
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"sin", "cos"} and len(node.args) == 1 and not node.keywords:
            return {"sin": sympy.sin, "cos": sympy.cos}[node.func.id](visit(node.args[0]))
        raise ValueError(f"unsupported symbolic syntax: {type(node).__name__}")

    return sympy.cancel(visit(tree))


def _equal(left: sympy.Expr, right: sympy.Expr) -> bool:
    return sympy.simplify(sympy.trigsimp(left - right)) == 0


def _indices(value: str, rank: int) -> tuple[int, ...]:
    result = tuple(int(part) for part in value.split(","))
    if len(result) != rank or any(index < 0 or index > 3 for index in result):
        raise ValueError(f"invalid tensor index: {value}")
    return result


def run(*, source_commit: str | None = None) -> dict[str, Any]:
    candidate = json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))
    passport = json.loads(PASSPORT_PATH.read_text(encoding="utf-8"))
    expected = passport["expected_results"]
    t = sympy.Symbol("t", real=True)
    r = sympy.Symbol("r", real=True, positive=True)
    theta = sympy.Symbol("theta", real=True)
    phi = sympy.Symbol("phi", real=True)
    mass = sympy.Symbol("M", real=True, positive=True)
    symbols = {"t": t, "r": r, "theta": theta, "phi": phi, "M": mass}
    coordinates = (t, r, theta, phi)
    metric = sympy.Array([[_parse(value, symbols) for value in row] for row in candidate["metric"]["components"]])
    metric_tensor = MetricTensor(metric, coordinates)
    christoffel = ChristoffelSymbols.from_metric(metric_tensor).tensor()
    riemann_object = RiemannCurvatureTensor.from_metric(metric_tensor)
    riemann = riemann_object.tensor()
    ricci_object = RicciTensor.from_riemann(riemann_object)
    ricci = ricci_object.tensor()
    ricci_scalar = RicciScalar.from_riccitensor(ricci_object).expr
    einstein = EinsteinTensor.from_metric(metric_tensor).tensor()

    lower_riemann = riemann_object.change_config("llll").tensor()
    inverse = sympy.Matrix(metric.tolist()).inv()
    kretschmann = sympy.Integer(0)
    for alpha in range(4):
        for beta in range(4):
            for mu in range(4):
                for nu in range(4):
                    kretschmann += (
                        inverse[alpha, alpha] * inverse[beta, beta] * inverse[mu, mu] * inverse[nu, nu]
                        * lower_riemann[alpha, beta, mu, nu] ** 2
                    )
    kretschmann = sympy.factor(sympy.trigsimp(sympy.cancel(kretschmann)))

    contract_digest = _sha256(_passport_contract(passport))
    checks = {
        "passport_contract_bound": contract_digest == PASSPORT_CONTRACT_SHA256,
        "metric_exact": all(
            _equal(metric[i, j], _parse(expected["metric"][i][j], symbols)) for i in range(4) for j in range(4)
        ),
        "christoffel_complete": False,
        "riemann_representatives": all(
            _equal(riemann[_indices(index, 4)], _parse(value, symbols))
            for index, value in expected["representative_riemann"].items()
        ),
        "ricci_zero": all(_equal(ricci[i, j], sympy.Integer(0)) for i in range(4) for j in range(4)),
        "ricci_scalar_zero": _equal(ricci_scalar, sympy.Integer(0)),
        "einstein_zero": all(_equal(einstein[i, j], sympy.Integer(0)) for i in range(4) for j in range(4)),
        "kretschmann_exact": _equal(kretschmann, _parse(expected["kretschmann_scalar"], symbols)),
    }
    nonzero_gamma = {
        f"{rho},{mu},{nu}": christoffel[rho, mu, nu]
        for rho in range(4) for mu in range(4) for nu in range(4)
        if not _equal(christoffel[rho, mu, nu], sympy.Integer(0))
    }
    checks["christoffel_complete"] = set(nonzero_gamma) == set(expected["nonzero_christoffel"]) and all(
        _equal(nonzero_gamma[index], _parse(value, symbols))
        for index, value in expected["nonzero_christoffel"].items()
    )
    overall = "MATCH" if all(checks.values()) else "MISMATCH"
    record: dict[str, Any] = {
        "schema_version": "1.0.0",
        "record_id": "REPRODUCTION-CANDIDATE-000003-EINSTEINPY-INTERNAL",
        "classification": "INTERNAL_SEPARATE_SOLVER_COMPARISON",
        "independence": {
            "external_reproduction": False,
            "same_project_owner": True,
            "same_machine": True,
            "same_git_credentials": True,
            "separate_tensor_library": True,
            "statement": "This is a useful implementation comparison, not independent scientific evidence or outside peer review."
        },
        "conflict_of_interest": {
            "declared": True,
            "contributors": ["ChefMrFrizzle", "OpenAI Codex"],
            "details": "The repository owner requested the work and Codex implemented both repository paths in the same workspace."
        },
        "environment": {
            "operating_system": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "sympy": sympy.__version__,
            "einsteinpy": einsteinpy.__version__,
            "git_commit": source_commit or _source_commit(),
        },
        "commands": [
            "python independent/schwarzschild_einsteinpy_crosscheck.py",
            "python scripts/research.py verify candidates/CANDIDATE-000003.json --passport benchmarks/BENCHMARK-000003.passport.json --reproducible",
        ],
        "inputs": {
            "candidate": "candidates/CANDIDATE-000003.json",
            "candidate_sha256": f"sha256:{_sha256(candidate)}",
            "passport": "benchmarks/BENCHMARK-000003.passport.json",
            "passport_contract_sha256": f"sha256:{contract_digest}",
        },
        "solver": {
            "name": "EinsteinPy symbolic module",
            "version": einsteinpy.__version__,
            "calculation": "EinsteinPy constructs the connection and curvature tensors; an explicit full diagonal contraction computes the Kretschmann scalar.",
            "schema_conformance_crosschecked": False,
        },
        "comparison_scope": {
            "compared": list(checks),
            "excluded": ["JSON Schema conformance", "external reproducibility", "novel geometry", "geodesics", "engineering feasibility"],
        },
        "observations": {
            "checks": {name: "PASS" if passed else "FAIL" for name, passed in checks.items()},
            "kretschmann_scalar": str(kretschmann),
            "ricci_tensor": [[str(sympy.simplify(ricci[i, j])) for j in range(4)] for i in range(4)],
            "einstein_tensor": [[str(sympy.simplify(einstein[i, j])) for j in range(4)] for i in range(4)],
        },
        "overall_status": overall,
        "signature": {
            "status": "UNSIGNED_NO_KEY",
            "record_digest_is_not_a_signature": True,
            "required_for_signed_status": "An identified reproducer must sign the canonical record digest with a verifiable SSH, GPG, or Sigstore identity."
        },
        "record_digest": "PENDING",
    }
    record["record_digest"] = f"sha256:{_sha256({key: value for key, value in record.items() if key != 'record_digest'})}"
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description="Cross-check Candidate 000003 through EinsteinPy.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--source-commit")
    args = parser.parse_args()
    record = run(source_commit=args.source_commit)
    if args.write:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(record, indent=2, ensure_ascii=False))
    else:
        print(f"candidate: CANDIDATE-000003")
        print(f"solver: EinsteinPy {record['environment']['einsteinpy']}")
        print(f"status: {record['overall_status']}")
        print(f"checks: {sum(value == 'PASS' for value in record['observations']['checks'].values())} passed / {sum(value == 'FAIL' for value in record['observations']['checks'].values())} failed")
        print(f"digest: {record['record_digest']}")
        print("independence: INTERNAL_ONLY")
        print("signature: UNSIGNED_NO_KEY")
    return 0 if record["overall_status"] == "MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
