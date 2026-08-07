from fractions import Fraction

from research_core.matrix import as_fraction_matrix, determinant, inverse, is_symmetric


def test_exact_minkowski_matrix_operations():
    matrix = as_fraction_matrix([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    assert is_symmetric(matrix)
    assert determinant(matrix) == Fraction(-1)
    assert inverse(matrix) == matrix


def test_fraction_preservation():
    matrix = as_fraction_matrix([[1, 2], [3, 4]])
    assert determinant(matrix) == Fraction(-2)
    assert inverse(matrix) == [[Fraction(-2), Fraction(1)], [Fraction(3, 2), Fraction(-1, 2)]]
