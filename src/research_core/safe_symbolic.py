from __future__ import annotations

import ast
from typing import Any

import sympy

MAX_EXPRESSION_LENGTH = 160
MAX_AST_NODES = 80


class UnsafeSymbolicExpression(ValueError):
    pass


def parse_symbolic(value: Any, symbols: dict[str, sympy.Symbol]) -> sympy.Expr:
    """Parse a deliberately tiny arithmetic grammar without eval or sympify."""
    if isinstance(value, bool):
        raise UnsafeSymbolicExpression("booleans are not symbolic numeric values")
    if isinstance(value, int):
        return sympy.Integer(value)
    if not isinstance(value, str) or not value or len(value) > MAX_EXPRESSION_LENGTH:
        raise UnsafeSymbolicExpression("symbolic components must be short non-empty strings or integers")
    try:
        tree = ast.parse(value, mode="eval")
    except SyntaxError as exc:
        raise UnsafeSymbolicExpression(f"invalid symbolic syntax: {exc.msg}") from exc
    if sum(1 for _ in ast.walk(tree)) > MAX_AST_NODES:
        raise UnsafeSymbolicExpression("symbolic expression is too complex")

    functions = {"sin": sympy.sin, "cos": sympy.cos}

    def convert(node: ast.AST) -> sympy.Expr:
        if isinstance(node, ast.Expression):
            return convert(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
            return sympy.Integer(node.value)
        if isinstance(node, ast.Name):
            if node.id in symbols:
                return symbols[node.id]
            if node.id == "pi":
                return sympy.pi
            raise UnsafeSymbolicExpression(f"unknown symbol: {node.id}")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = convert(node.operand)
            return operand if isinstance(node.op, ast.UAdd) else -operand
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
            left, right = convert(node.left), convert(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if not right.is_Integer or abs(int(right)) > 12:
                raise UnsafeSymbolicExpression("powers must be small integer constants")
            return left**right
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in functions and len(node.args) == 1 and not node.keywords:
            return functions[node.func.id](convert(node.args[0]))
        raise UnsafeSymbolicExpression(f"unsupported symbolic syntax: {type(node).__name__}")

    return sympy.cancel(convert(tree))


def parse_symbolic_matrix(values: list[list[Any]], symbols: dict[str, sympy.Symbol]) -> sympy.Matrix:
    if not isinstance(values, list) or not values or any(not isinstance(row, list) for row in values):
        raise UnsafeSymbolicExpression("metric must be a non-empty matrix")
    return sympy.Matrix([[parse_symbolic(value, symbols) for value in row] for row in values])


def expressions_equal(left: sympy.Expr, right: sympy.Expr) -> bool:
    return sympy.simplify(sympy.trigsimp(left - right)) == 0


def matrices_equal(left: sympy.Matrix, right: sympy.Matrix) -> bool:
    return left.shape == right.shape and all(expressions_equal(left[i, j], right[i, j]) for i in range(left.rows) for j in range(left.cols))
