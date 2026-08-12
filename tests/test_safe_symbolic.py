import pytest
import sympy

from research_core.safe_symbolic import UnsafeSymbolicExpression, parse_symbolic


SYMBOLS = {"r": sympy.Symbol("r", positive=True), "M": sympy.Symbol("M", positive=True)}


@pytest.mark.parametrize(
    "value",
    [
        "__import__('os').system('whoami')",
        "r.__class__",
        "open('secret')",
        "1.5",
        "r**1000",
        True,
    ],
)
def test_restricted_symbolic_parser_rejects_unsafe_or_out_of_profile_input(value):
    with pytest.raises(UnsafeSymbolicExpression):
        parse_symbolic(value, SYMBOLS)


def test_restricted_symbolic_parser_accepts_benchmark_grammar():
    expression = parse_symbolic("48*M**2/r**6", SYMBOLS)
    assert sympy.simplify(expression - 48 * SYMBOLS["M"] ** 2 / SYMBOLS["r"] ** 6) == 0
