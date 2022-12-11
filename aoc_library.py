from math import sin, cos, radians
from re import findall

from typing import Optional, Sequence


def get_input() -> str:
    return input_string


def get_chunks(chunk_count: int, s: Optional[str]=None) -> list[tuple[str, ...]]:
    if s is None:
        s = input_string

    return list(zip(*chunk_count*[iter(get_lines(s))]))


def get_blocks(s: Optional[str]=None) -> list[str]:
    if s is None:
        s = input_string

    return s.split('\n\n')


def get_lines(s: Optional[str]=None) -> list[str]:
    if s is None:
        s = input_string

    return s.splitlines()


def get_lines_nonempty(s: Optional[str]=None) -> list[str]:
    if s is None:
        s = input_string

    return list(filter(None, get_lines(s)))


def get_ints(s: Optional[str]=None) -> list[int]:
    if s is None:
        s = input_string

    return list(map(int, findall(r"[+-]?\d+", s)))


def get_floats(s: Optional[str]=None) -> list[float]:
    if s is None:
        s = input_string

    return list(map(float, findall(r"[+-]?\d*\.?\d+", s)))


def get_lists(s: Optional[str]=None) -> list[list]:
    if s is None:
        s = input_string

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


def print_grid(grid: Sequence[str | Sequence[str]]) -> None:
    print('\n'.join(map(' '.join, grid)))


def is_valid_grid_coord(grid: Sequence[Sequence], *coords: int) -> bool:
    line = grid
    for coord in coords:
        if not (0 <= coord < len(line)):
            return False

        line = line[0]
    
    return True


if __name__ != "__main__":
    from inspect import stack as _stack
    from pathlib import Path

    # directory of the file that imported this module
    _directory = Path(_stack()[6].filename).parent

    try:
        with open(_directory / "input") as f:
            input_string = f.read().rstrip('\n')
    except FileNotFoundError:
        print("Could not open input.")
        input_string = ""

    blocks = get_blocks(input_string)
    lines = get_lines(input_string)
    lines_transposed = transpose(lines)
    lines_nonempty = get_lines_nonempty(input_string)

    lists = get_lists(input_string)

    ints = get_ints(input_string)
    floats = get_floats(input_string)
