from __future__ import annotations

from fractions import Fraction
from typing import Iterable

Matrix = list[list[Fraction]]


def as_fraction_matrix(values: Iterable[Iterable[int | float | Fraction]]) -> Matrix:
    return [[Fraction(value) for value in row] for row in values]


def is_square(matrix: Matrix) -> bool:
    return bool(matrix) and all(len(row) == len(matrix) for row in matrix)


def is_symmetric(matrix: Matrix) -> bool:
    return is_square(matrix) and all(matrix[i][j] == matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix)))


def determinant(matrix: Matrix) -> Fraction:
    if not is_square(matrix):
        raise ValueError("determinant requires a non-empty square matrix")
    size = len(matrix)
    work = [row[:] for row in matrix]
    sign = Fraction(1)
    product = Fraction(1)
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        product *= pivot_value
        for row in range(column + 1, size):
            factor = work[row][column] / pivot_value
            for item in range(column, size):
                work[row][item] -= factor * work[column][item]
    return sign * product


def inverse(matrix: Matrix) -> Matrix:
    if not is_square(matrix):
        raise ValueError("inverse requires a non-empty square matrix")
    size = len(matrix)
    work = [row[:] + [Fraction(int(i == j)) for j in range(size)] for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column] != 0), None)
        if pivot is None:
            raise ValueError("matrix is singular")
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
        pivot_value = work[column][column]
        work[column] = [value / pivot_value for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            factor = work[row][column]
            work[row] = [value - factor * pivot_value for value, pivot_value in zip(work[row], work[column], strict=True)]
    return [row[size:] for row in work]


def json_number(value: Fraction) -> int | float | str:
    if value.denominator == 1:
        return value.numerator
    return f"{value.numerator}/{value.denominator}"


def json_matrix(matrix: Matrix) -> list[list[int | float | str]]:
    return [[json_number(value) for value in row] for row in matrix]
