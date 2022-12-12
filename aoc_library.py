from __future__ import annotations

from collections import defaultdict, deque
from functools import total_ordering, wraps
from bisect import insort
from math import sin, cos, radians
from re import findall

from collections.abc import Iterable, Callable, Sequence
from typing import Any, Literal, Optional, TypeVar

T = TypeVar("T")


Neighborhood = Iterable[tuple[int, int]]

SIDES:       Neighborhood = {(-1, 0), (1, 0), (0, -1), (0, 1)}
CORNERS:     Neighborhood = {(-1, -1), (-1, 1), (1, -1), (1, 1)}
MOORE:       Neighborhood = CORNERS | SIDES
VON_NEUMANN: Neighborhood = SIDES


# consider turning this into a singleton
@total_ordering
class Infinity:
    """
    class of objects that are greater/smaller than everything except other Infinity objects
    used in defaultdicts that default to infinity
    """
    def __init__(self, is_negative: bool=False) -> None:
        self.is_negative = is_negative

    def __add__(self, other: Any) -> Infinity:
        if isinstance(other, Infinity) and self.is_negative ^ other.is_negative:
            raise ValueError("Can't add Infinity to Infinity of opposing sign.")

        return Infinity(self.is_negative)
    
    def __sub__(self, other: Any) -> Infinity:
        if isinstance(other, Infinity) and self.is_negative == other.is_negative:
            raise ValueError("Can't subtract Infinity from Infinity of same sign.")
        
        return Infinity(self.is_negative)

    def __mul__(self, other: Any) -> Infinity:
        try:
            return Infinity(self.is_negative ^ (other < 0))
        except TypeError:
            return Infinity(self.is_negative)

    def __truediv__(self, other: Any) -> Infinity:
        if isinstance(other, Infinity):
            raise ValueError("Can't divide Infinity by Infinity.")
        
        try:
            return Infinity(self.is_negative ^ (other < 0))
        except TypeError:
            return Infinity(self.is_negative)

    def __rtruediv__(self, _: Any) -> Literal[0]:
        # Infinity / Infinity is handled in __truediv__
        return 0

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__

    def __neg__(self) -> Infinity:
        return Infinity(not self.is_negative)

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Infinity):
            return other.is_negative > self.is_negative

        return not self.is_negative
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Infinity) and self.is_negative == other.is_negative

    def __repr__(self) -> str:
        return '-inf' if self.is_negative else 'inf'
    
    __str__ = __repr__


class InfinityPositive(Infinity):
    def __init__(self):
        super().__init__(False)


class InfinityNegative(Infinity):
    def __init__(self):
        super().__init__(True)


def uses_input(f: Callable[[str], T]) -> Callable[[Optional[str]], T]:
    @wraps(f)
    def inner(s: Optional[str]=None) -> T:
        if s is None:
            s = input_string

        return f(s)

    return inner


def get_chunks(s: Optional[str], chunk_count: int) -> list[tuple[str, ...]]:
    if s is None:
        s = input_string

    return list(zip(*chunk_count*[iter(get_lines(s))]))


@uses_input
def get_blocks(s: str) -> list[str]:
    return s.split('\n\n')


@uses_input
def get_lines(s: str) -> list[str]:
    return s.splitlines()


@uses_input
def get_lines_nonempty(s: str) -> list[str]:
    return list(filter(None, get_lines(s)))


@uses_input
def get_ints(s: str) -> list[int]:
    return list(map(int, findall(r"[+-]?\d+", s)))


@uses_input
def get_floats(s: str) -> list[float]:
    return list(map(float, findall(r"[+-]?\d*\.?\d+", s)))


@uses_input
def get_lists(s: str) -> list[list]:
    return list(map(str.split, get_lines_nonempty(s)))


def transpose(l: Sequence[Sequence]) -> list[Sequence]:
    if not l:
        return list(l)

    if isinstance(l[0], str):
        return list(map(''.join, zip(*l)))
    
    return list(map(list, zip(*l)))


def rotate_2d(x: int | float, y: int | float, angleDegrees: int | float) -> tuple[int | float, int | float]:
    angleDegrees %= 360
    match angleDegrees:
        case 0:
            return  x,  y
        case 90:
            return -y,  x
        case 180:
            return -x, -y
        case 270:
            return  y, -x
        case _:
            angleRadians = radians(angleDegrees)
            return x*cos(angleRadians) - y*sin(angleRadians), x*sin(angleRadians) + y*cos(angleRadians)


def manhattan(a: Sequence[int | float], b: Sequence[int | float]) -> int | float:
    return sum(abs(ac - bc) for ac, bc in zip(a, b, strict=True))  # type: ignore


def astar(
        grid: Sequence[Sequence[T]],
        start_point: tuple[int, int],
        end_point: tuple[int, int],
        neighborhood: Neighborhood,
        distance_function: Callable[[tuple[int, int], tuple[int, int]], int | float],
        heuristic_function: Optional[Callable[[tuple[int, int]], int | float]]=None,
        predicate: Optional[Callable[[T, T], bool]]=None
) -> dict[tuple[int, int], tuple[int, int]]:
    if heuristic_function is None:
        heuristic_function = lambda current_point: distance_function(current_point, end_point)
    
    if predicate is None:
        predicate = lambda *_: True

    neighborhood = tuple(neighborhood)

    f_scores: dict[tuple[int, int], int | float | Infinity] = defaultdict(InfinityPositive)
    g_scores: dict[tuple[int, int], int | float | Infinity] = defaultdict(InfinityPositive)

    came_from: dict[tuple[int, int], tuple[int, int]] = {}

    f_scores[start_point] = 0
    g_scores[start_point] = distance_function(start_point, end_point)

    possible = deque([start_point])
    while possible:
        c = x, y = possible.popleft()

        if c == end_point:
            return came_from

        for dx, dy in neighborhood:
            n = nx, ny = x+dx, y+dy

            if not is_valid_grid_coord(grid, *n):
                continue

            if not predicate(grid[x][y], grid[nx][ny]):
                continue
            
            new_g = g_scores[c] + distance_function(c, n)
            if new_g < g_scores[n]:
                came_from[n] = c
                g_scores[n] = new_g
                f_scores[n] = new_g + heuristic_function(n)
                if n not in possible:
                    insort(possible, n, key=lambda x: f_scores[x])
    
    return came_from


def reconstruct_path(came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int]):
    total_path = deque([current])
    while came_from.get(current):
        current = came_from[current]
        total_path.appendleft(current)

    return total_path


def print_grid(grid: Sequence[str | Sequence[str]]) -> None:
    print('\n'.join(map(' '.join, grid)))


def is_valid_grid_coord(grid: Sequence[Sequence], *coords: int) -> bool:
    axis = grid
    for coord in coords:
        if not (0 <= coord < len(axis)):
            return False

        axis = axis[0]
    
    return True


if __name__ != "__main__":
    from inspect import stack as _stack
    from pathlib import Path as _Path

    # directory of the file that imported this module
    _directory = _Path(_stack()[6].filename).parent

    try:
        with open(_directory / "input") as f:
            input_string = f.read().rstrip('\n')
    except FileNotFoundError:
        print("Could not open input.")
        input_string = ""

    INFINITY          = InfinityPositive()
    INFINITY_NEGATIVE = InfinityNegative()

    blocks           = get_blocks(input_string)
    lines            = get_lines(input_string)
    lines_transposed = transpose(lines)
    lines_nonempty   = get_lines_nonempty(input_string)

    lists = get_lists(input_string)

    ints   = get_ints(input_string)
    floats = get_floats(input_string)
