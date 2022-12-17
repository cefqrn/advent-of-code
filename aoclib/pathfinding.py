from .infinity import Infinity, InfinityPositive
from .grid import is_valid_grid_coord

from collections import defaultdict, deque
from bisect import insort

from collections.abc import Iterable, Sequence
from typing import Callable, Optional, TypeVar, Union

T = TypeVar("T")
Number = Union[int, float]  # Union instead of | to support 3.9 (pypy)

Neighborhood = Iterable[tuple[int, int]]

SIDES:       Neighborhood = {(-1, 0), (1, 0), (0, -1), (0, 1)}
CORNERS:     Neighborhood = {(-1, -1), (-1, 1), (1, -1), (1, 1)}
MOORE:       Neighborhood = CORNERS | SIDES
VON_NEUMANN: Neighborhood = SIDES

def astar(
        grid: Sequence[Sequence[T]],
        start_point: tuple[int, int],
        end_point: tuple[int, int],
        neighborhood: Neighborhood,
        distance_function: Callable[[tuple[int, int], tuple[int, int]], Number],
        heuristic_function: Optional[Callable[[tuple[int, int]], Number]]=None,
        predicate: Optional[Callable[[T, T], bool]]=None
) -> dict[tuple[int, int], tuple[int, int]]:
    if heuristic_function is None:
        heuristic_function = lambda current_point: distance_function(current_point, end_point)
    
    if predicate is None:
        predicate = lambda *_: True

    neighborhood = tuple(neighborhood)

    f_scores: dict[tuple[int, int], Union[Number, Infinity]] = defaultdict(InfinityPositive)
    g_scores: dict[tuple[int, int], Union[Number, Infinity]] = defaultdict(InfinityPositive)

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
