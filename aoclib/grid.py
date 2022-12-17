from collections.abc import Sequence
from typing import Union


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
