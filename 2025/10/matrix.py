from __future__ import annotations

from collections import UserList
from itertools import batched, repeat, product
from operator import add, mul, sub

from collections.abc import Sized as Sized, Iterable
from numbers import Rational
from typing import overload, Optional


def solve_augmented_matrix(A: Matrix, B: Matrix) -> Matrix:
    return *map(Matrix, zip(*(
        (row[:A.w], row[A.w:])
        for row in Matrix(map(add, A.rows, B.rows)).rref.rows
    ))),


class Matrix(UserList):
    @overload
    def __init__(self, h: int, w: int, data: Optional[Iterable]): ...

    @overload
    def __init__(self, data: Iterable[Iterable]): ...

    def __init__(self, a, b=None, c=None):
        if isinstance(a, Iterable):
            super().__init__()

            iter_a = iter(a)
            self.data.extend(next(iter_a))
            w = len(self.data)

            h = 1
            for h, row in enumerate(iter_a, h+1):
                self.data.extend(row)

            self.w = w
            self.h = h
        elif isinstance(a, int) and isinstance(b, int) and (isinstance(c, Iterable) or c is None):
            self.h = a
            self.w = b

            super().__init__(repeat(0, a*b) if c is None else c)
        else:
            raise ValueError

    @classmethod
    def identity(cls, n: int):
        matrix = Matrix(n, n)
        for i in range(n):
            matrix[i, i] = 1

        return matrix

    @property
    def rows(self):
        return tuple(batched(self.data, self.w))

    @property
    def transposed(self):
        return Matrix(list(zip(*self.rows)))

    @property
    def columns(self):
        return self.transposed.rows

    @property
    def rref(self):
        rows = list(map(list, self.rows))

        pivot_index = 0
        pivot_row_index = 0
        while pivot_row_index < self.h and pivot_index < (self.w-1):
            for new_pivot_row_index, pivot_row in enumerate(
                rows[pivot_row_index:],
                pivot_row_index
            ):
                if pivot := pivot_row[pivot_index]:
                    break
            else:
                pivot_index += 1
                continue

            if new_pivot_row_index != pivot_row_index:
                rows[pivot_row_index], rows[new_pivot_row_index] = pivot_row, rows[pivot_row_index]

            for row_index, row in enumerate(rows):
                if row_index == pivot_row_index:
                    continue

                multiplier = row[pivot_index] / pivot
                row[:] = (
                    row_value - multiplier * pivot_row_value
                    for row_value, pivot_row_value in zip(row, pivot_row)
                )

            pivot_row[:] = map(lambda x: x/pivot, pivot_row)

            pivot_row_index += 1
            pivot_index += 1

        return Matrix(rows)

    @property
    def is_identity(self):
        return self == Matrix.identity(self.w)

    @property
    def is_in_rref(self):
        return self == self.rref

    @property
    def inverse(self):
        if self.h != self.w:
            raise ValueError("can't invert non square matrix")

        a, b = solve_augmented_matrix(self, self.identity(self.w))
        if not a.is_identity:
            raise ValueError("matrix isn't invertible")

        return b

    @property
    def det(self):
        if self.h != self.w:
            raise ValueError("can't compute determinant for non square matrix")

        if self.h == 1:
            return self.data[0]

        def det(rows):
            if len(rows) == 2:
                return rows[0][0]*rows[1][1] - rows[0][1]*rows[1][0]

            multipliers, *bottom_rows = rows
            return sum(
                multiplier * det([
                    r[:i] + r[i+1:]
                    for r in bottom_rows
                ]) * (-1)**i
                for i, multiplier in enumerate(multipliers)
            )

        return det(self.rows)

    def reshaped(self, h: int, w: int) -> Matrix:
        return Matrix(h, w, self.data)

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.rows[i]
        elif isinstance(i, tuple):
            y, x = i
            return self.data[y*self.w + x]

        raise TypeError

    def __setitem__(self, i, v):
        y, x = i
        self.data[y*self.w + x] = v

    def __eq__(self, other: Matrix):
        return self.h == other.h and self.w == other.w and self.data == other.data

    def __add__(self, other: Matrix):
        return Matrix(self.h, self.w, map(add, self.data, other.data))

    def __sub__(self, other: Matrix):
        return Matrix(self.h, self.w, map(sub, self.data, other.data))

    def __mul__(self, other: Rational):
        return Matrix(self.h, self.w, (x*other for x in self.data))

    __rmul__ = __mul__

    def __truediv__(self, other: Rational):
        return Matrix(self.h, self.w, (x/other for x in self.data))

    def __matmul__(self, other: Matrix):
        if self.w != other.h:
            raise ValueError(f"Matrices arent compatible ({self.h}x{self.w} and {other.h}x{other.w})")
        return Matrix(self.h, other.w, (
            sum(map(mul, row, column))
            for row, column in product(self.rows, other.transposed.rows)
        ))

    def __str__(self):
        max_width = max(map(len, map(str, self.data)))
        rows = [" ".join(str(x).rjust(max_width) for x in row) for row in self.rows]

        if self.h == 1:
            return "[ " + rows[0] + " ]"

        return "\n".join((
              "⎡ " + rows[0]  + " ⎤",
            *("⎢ " + row      + " ⎥" for row in rows[1:-1]),
              "⎣ " + rows[-1] + " ⎦"
        ))
