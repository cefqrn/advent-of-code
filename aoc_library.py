from math import sin, cos, radians
from re import findall

from typing import Optional


def get_input() -> str:
    return input_string


def get_chunks(chunk_count: int, s: Optional[str]=None) -> list[tuple[str]]:
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

    return s.split('\n')


def get_nonempty_lines(s: Optional[str]=None) -> list[str]:
    if s is None:
        s = input_string

    return list(filter(None, s.split('\n')))


def get_ints(s: Optional[str]=None) -> list[int]:
    if s is None:
        s = input_string

    return list(map(int, findall(r"(?<!\d)\d+(?!\d)", s)))


def get_floats(s: Optional[str]=None) -> list[float]:
    if s is None:
        s = input_string

    return list(map(float, findall(r"(?<![\d\.])[\d\.]+(?![\d\.])", s)))


def get_lists(s: Optional[str]=None) -> list[list]:
    if s is None:
        s = input_string

    return list(map(str.split, get_nonempty_lines()))


def rotate_2d(x: int | float, y: int | float, angleDegrees: int | float):
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


if __name__ != "__main__":
    from contextlib import suppress
    from inspect import stack
    from pathlib import Path

    # directory of the file that imported this module
    _directory = Path(stack()[6].filename).parent

    try:
        with open(_directory / "input") as f:
            input_string = f.read()
    except FileNotFoundError:
        print("Could not open input.")
        input_string = ""

    blocks = get_blocks(input_string)
    lines = get_lines(input_string)
    nonempty_lines = get_nonempty_lines(input_string)

    lists = get_lists(input_string)

    with suppress(ValueError):
        ints = get_ints(input_string)

    with suppress(ValueError):
        floats = get_floats(input_string)
