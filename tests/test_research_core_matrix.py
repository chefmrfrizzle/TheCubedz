from fractions import Fraction

from research_core.matrix import as_fraction_matrix, determinant, inverse, is_symmetric, multiply, pullback, transpose


def test_exact_minkowski_matrix_operations():
    matrix = as_fraction_matrix([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    assert is_symmetric(matrix)
    assert determinant(matrix) == Fraction(-1)
    assert inverse(matrix) == matrix


def test_fraction_preservation():
    matrix = as_fraction_matrix([[1, 2], [3, 4]])
    assert determinant(matrix) == Fraction(-2)
    assert inverse(matrix) == [[Fraction(-2), Fraction(1)], [Fraction(3, 2), Fraction(-1, 2)]]


def test_exact_linear_pullback_changes_components_without_changing_geometry():
    eta = as_fraction_matrix([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    jacobian = as_fraction_matrix([[2, 0, 0, 0], [0, 3, 0, 0], [0, 0, 4, 0], [0, 0, 0, 5]])
    expected = as_fraction_matrix([[-4, 0, 0, 0], [0, 9, 0, 0], [0, 0, 16, 0], [0, 0, 0, 25]])
    assert transpose(jacobian) == jacobian
    assert multiply(transpose(jacobian), eta)
    assert pullback(eta, jacobian) == expected
