from collections import deque
from itertools import islice, cycle


def rotate_grid(grid):
    """rotate grid clockwise"""
    return list(map("".join, zip(*reversed(grid))))


def rotate_pos(w, h, x, y, n=1):
    """rotate position on grid clockwise n times"""
    match n % 4:
        case 0: return x, y
        case 1: return (h-1) - y, x
        case 2: return (w-1) - x, (h-1) - y
        case 3: return y, (w-1) - x


def iterate(f, it):
    yield it
    while True:
        yield (it := f(it))


def simulate(grids, initial_pos, track_visited=True):
    grids = grids.copy()

    w, h = len(grids[0][0]), len(grids[0])

    # initial cw rotation
    x, y = rotate_pos(w, h, *initial_pos)
    grids.rotate(-1)
    w, h = h, w

    ends_seen = set()
    positions_seen = set()
    for i in cycle([-1, 0, 1, 2]):
        hit = grids[0][y].find("#", x+1)

        if track_visited:
            positions_seen.update(
                rotate_pos(w, h, nx, y, i)
                for nx in range(x, h if hit == -1 else hit)
            )

        end = (i, x, y)
        if end in ends_seen:
            return positions_seen, True

        ends_seen.add(end)

        if hit == -1:
            break

        # move x to obstacle
        x = hit - 1

        # rotate ccw
        x, y = rotate_pos(w, h, x, y, -1)
        grids.rotate()
        w, h = h, w

    return positions_seen, False


with open(0) as f:
    grid = f.read().splitlines()

initial_pos = None
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == '^':
            initial_pos = x, y

assert initial_pos

grids = deque(islice(iterate(rotate_grid, grid), 4))

visited, _ = simulate(grids, initial_pos)
print(len(visited))

p2 = 0
for i, (x, y) in enumerate(visited - {initial_pos}):
    for i, g in enumerate(grids):
        rx, ry = rotate_pos(len(g[0]), len(g), x, y, i)
        g[ry] = g[ry][:rx] + "#" + g[ry][rx+1:]

    _, has_loop = simulate(grids, initial_pos, False)

    for i, g in enumerate(grids):
        rx, ry = rotate_pos(len(g[0]), len(g), x, y, i)
        g[ry] = g[ry][:rx] + "." + g[ry][rx+1:]

    p2 += has_loop

print(p2)
