from .infinity import Infinity, INFINITY, INFINITY_NEGATIVE

from itertools import chain

from collections.abc import Sequence
from typing import Union, TypeVar, Any

T = TypeVar("T", int, float)

__all__ = [
    "transpose", "print_grid", "is_valid_grid_coord", "get_bounds"
]


# TODO: move some of these into a class

def transpose(l: Sequence[Sequence]) -> list[Sequence]:
    if not l:
        return list(l)

    if isinstance(l[0], str):
        return list(map(''.join, zip(*l)))
    
    return list(map(list, zip(*l)))


def print_grid(grid: Sequence[Union[str, Sequence[str]]]) -> None:
    print('\n'.join(map(' '.join, grid)))


def is_valid_grid_coord(grid: Sequence[Sequence], *coords: int) -> bool:
    axis = grid
    for coord in coords:
        if not (0 <= coord < len(axis)):
            return False

        axis = axis[0]
    
    return True


def get_bounds(grid: Union[dict[Sequence[T], Any], set[Sequence[T]]]) -> tuple[tuple[T, T], ...]:
    if isinstance(grid, dict):
        p = next(iter(grid.keys()))
    else:
        grid.add(p:=grid.pop())
    dimension_count = len(p)

    mins:  list[T | Infinity] = [INFINITY] * dimension_count
    maxes: list[T | Infinity] = [INFINITY_NEGATIVE] * dimension_count
    for p in grid:
        for i, c in enumerate(p):
            if c < mins[i]:
                mins[i] = c
            if c > maxes[i]:
                maxes[i] = c

    if any(isinstance(x, Infinity) for x in chain(mins, maxes)):
        raise ValueError

    return tuple(zip(mins, maxes))
