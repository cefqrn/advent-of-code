from collections.abc import Iterable, Sequence

VON_NEUMANN_NEIGHBORHOOD = (-1, 0), (1, 0), (0, -1), (0, 1)
DIAGONAL_NEIGHBORHOOD = (-1, -1), (-1, 1), (1, -1), (1, 1)

MOORE_NEIGHBORHOOD = VON_NEUMANN_NEIGHBORHOOD + DIAGONAL_NEIGHBORHOOD


def neighbor_indices(grid: Sequence[Sequence], x: int, y: int, neighborhood: Iterable[tuple[int, int]]=MOORE_NEIGHBORHOOD) -> list[tuple[int, int]]:
    return [
        (ny, nx)
        for dy, dx in neighborhood
        if  (ny:=y+dy) in range(len(grid))
        and (nx:=x+dx) in range(len(grid[0]))
    ]


def neighbors[T](grid: Sequence[Sequence[T]], x: int, y: int, neighborhood: Iterable[tuple[int, int]]=MOORE_NEIGHBORHOOD) -> list[T]:
    return [
        grid[ny][nx]
        for ny, nx in neighbor_indices(grid, x, y, neighborhood)
    ]
