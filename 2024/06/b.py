from itertools import cycle


def rotate_grid(grid):
    """rotate grid counter-clockwise"""
    return list(map("".join, zip(*grid)))[::-1]


def rotate_pos(w, h, x, y, n=1):
    """rotate position on grid counter-clockwise n times"""
    match n % 4:
        case 0: return x, y
        case 1: return y, (w-1) - x
        case 2: return (w-1) - x, (h-1) - y
        case 3: return (h-1) - y, x


def simulate(grids, w, h, x, y, track_visited):
    collisions_seen = set()
    positions_seen = set()
    for i, grid in cycle(enumerate(grids)):
        hit = grid[y].find("#", x+1)

        if track_visited:
            positions_seen.update(
                rotate_pos(w, h, nx, y, -i)  # coords relative to grids[0]
                for nx in range(x, h if hit == -1 else hit)
            )

        collision = i, hit, y
        if collision in collisions_seen:
            return positions_seen, True

        collisions_seen.add(collision)

        if hit == -1:
            break

        # move x to obstacle
        x = hit - 1

        # rotate ccw
        x, y = rotate_pos(w, h, x, y)
        w, h = h, w

    return positions_seen, False


with open(0) as f:
    lines = f.read().splitlines()

initial_pos = None
for y, row in enumerate(lines):
    for x, c in enumerate(row):
        if c == '^':
            initial_pos = x, y

assert initial_pos
w, h = len(lines[0]), len(lines)

grids = [lines := rotate_grid(lines) for _ in range(4)]

# initial cw rotation
ix, iy = initial_pos = rotate_pos(w, h, *initial_pos, -1)
grids = grids[-2:] + grids[:-2]  # already rotated ccw once so need to rotate cw twice
w, h = h, w

visited, _ = simulate(grids, w, h, ix, iy, track_visited=True)
print(len(visited))

p2 = 0
for x, y in visited - {initial_pos}:
    for i, g in enumerate(grids):
        rx, ry = rotate_pos(len(g[0]), len(g), x, y, i)
        g[ry] = g[ry][:rx] + "#" + g[ry][rx+1:]

    _, has_loop = simulate(grids, w, h, ix, iy, track_visited=False)
    p2 += has_loop

    for i, g in enumerate(grids):
        rx, ry = rotate_pos(len(g[0]), len(g), x, y, i)
        g[ry] = g[ry][:rx] + "X" + g[ry][rx+1:]

print(p2)
