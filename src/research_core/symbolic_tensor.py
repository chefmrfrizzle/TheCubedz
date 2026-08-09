from __future__ import annotations

from dataclasses import dataclass

import sympy

from .safe_symbolic import expressions_equal


@dataclass(frozen=True)
class SymbolicGeometry:
    coordinates: tuple[sympy.Symbol, ...]
    metric: sympy.Matrix
    inverse_metric: sympy.Matrix
    determinant: sympy.Expr
    christoffel: tuple
    riemann: tuple
    ricci: sympy.Matrix
    ricci_scalar: sympy.Expr
    einstein: sympy.Matrix
    kretschmann: sympy.Expr


def _simplify(value: sympy.Expr) -> sympy.Expr:
    return sympy.factor(sympy.trigsimp(sympy.cancel(value)))


def compute_geometry(metric: sympy.Matrix, coordinates: tuple[sympy.Symbol, ...]) -> SymbolicGeometry:
    size = len(coordinates)
    if metric.shape != (size, size):
        raise ValueError("metric dimensions must match the coordinates")
    inverse = metric.inv().applyfunc(_simplify)
    determinant = _simplify(metric.det())
    christoffel = tuple(
        tuple(
            tuple(
                _simplify(sum(
                    inverse[rho, sigma] * (
                        sympy.diff(metric[sigma, nu], coordinates[mu])
                        + sympy.diff(metric[sigma, mu], coordinates[nu])
                        - sympy.diff(metric[mu, nu], coordinates[sigma])
                    )
                    for sigma in range(size)
                ) / 2)
                for nu in range(size)
            )
            for mu in range(size)
        )
        for rho in range(size)
    )
    riemann = tuple(
        tuple(
            tuple(
                tuple(
                    _simplify(
                        sympy.diff(christoffel[rho][nu][sigma], coordinates[mu])
                        - sympy.diff(christoffel[rho][mu][sigma], coordinates[nu])
                        + sum(
                            christoffel[rho][mu][lam] * christoffel[lam][nu][sigma]
                            - christoffel[rho][nu][lam] * christoffel[lam][mu][sigma]
                            for lam in range(size)
                        )
                    )
                    for nu in range(size)
                )
                for mu in range(size)
            )
            for sigma in range(size)
        )
        for rho in range(size)
    )
    ricci = sympy.Matrix(size, size, lambda sigma, nu: _simplify(sum(riemann[rho][sigma][rho][nu] for rho in range(size))))
    ricci_scalar = _simplify(sum(inverse[sigma, nu] * ricci[sigma, nu] for sigma in range(size) for nu in range(size)))
    einstein = sympy.Matrix(size, size, lambda mu, nu: _simplify(ricci[mu, nu] - metric[mu, nu] * ricci_scalar / 2))
    kretschmann = sympy.Integer(0)
    for alpha in range(size):
        for beta in range(size):
            for mu in range(size):
                for nu in range(size):
                    lowered = _simplify(sum(metric[alpha, rho] * riemann[rho][beta][mu][nu] for rho in range(size)))
                    raised_weight = inverse[alpha, alpha] * inverse[beta, beta] * inverse[mu, mu] * inverse[nu, nu]
                    kretschmann += _simplify(raised_weight * lowered**2)
    return SymbolicGeometry(
        coordinates=coordinates,
        metric=metric,
        inverse_metric=inverse,
        determinant=determinant,
        christoffel=christoffel,
        riemann=riemann,
        ricci=ricci,
        ricci_scalar=ricci_scalar,
        einstein=einstein,
        kretschmann=_simplify(kretschmann),
    )


def tensor_all_zero(tensor: tuple) -> bool:
    def values(value):
        if isinstance(value, tuple):
            for item in value:
                yield from values(item)
        else:
            yield value

    return all(expressions_equal(item, sympy.Integer(0)) for item in values(tensor))


def matrix_all_zero(matrix: sympy.Matrix) -> bool:
    return all(expressions_equal(matrix[i, j], sympy.Integer(0)) for i in range(matrix.rows) for j in range(matrix.cols))


def nonzero_rank3(tensor: tuple) -> dict[str, sympy.Expr]:
    output: dict[str, sympy.Expr] = {}
    for i in range(len(tensor)):
        for j in range(len(tensor[i])):
            for k in range(len(tensor[i][j])):
                if not expressions_equal(tensor[i][j][k], sympy.Integer(0)):
                    output[f"{i},{j},{k}"] = tensor[i][j][k]
    return output
