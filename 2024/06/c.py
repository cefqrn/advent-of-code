from itertools import cycle


def parse_grid(lines):
    return [
        int("".join(line).translate(str.maketrans(".^#", "001")), 2)
        for line in lines
    ]


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


def simulate(grids, w, h, x, y, track_visited=True):
    collisions_seen = set()
    positions_seen = set()
    for i, grid in cycle(enumerate(grids)):
        hit = w - (((1 << (w - x)) - 1) & grid[y]).bit_length()

        if track_visited:
            positions_seen.update(
                rotate_pos(w, h, nx, y, -i)  # coords relative to grids[0]
                for nx in range(x, hit)
            )

        collision = i, hit, y
        if collision in collisions_seen:
            return positions_seen, True

        collisions_seen.add(collision)

        if hit == w:
            break

        # move x to obstacle
        x = hit - 1

        # rotate ccw
        x, y = y, (w-1) - x
        w, h = h, w

    return positions_seen, False


with open(0) as f:
    lines = f.read().splitlines()

initial_pos = None
for y, row in enumerate(lines):
    for x, c in enumerate(row):
        if c == '^':
            initial_pos = x, y

w, h = len(row), len(lines)

assert initial_pos
w, h = len(lines[0]), len(lines)

grids = [parse_grid(lines := rotate_grid(lines)) for _ in range(4)]

# initial cw rotation
ix, iy = initial_pos = rotate_pos(w, h, *initial_pos, -1)
grids = grids[-2:] + grids[:-2]  # already rotated ccw once so need to rotate cw twice
w, h = h, w

visited, _ = simulate(grids, w, h, ix, iy, track_visited=True)
print(len(visited))

p2 = 0
for i, (x, y) in enumerate(visited - {initial_pos}):
    for i, g in enumerate(grids):
        rx, ry = rotate_pos([w, h][i % 2], [h, w][i % 2], x, y, i)
        g[ry] ^= 1 << (w + ~rx)

    _, has_loop = simulate(grids, w, h, ix, iy, False)

    for i, g in enumerate(grids):
        rx, ry = rotate_pos([w, h][i % 2], [h, w][i % 2], x, y, i)
        g[ry] ^= 1 << (w + ~rx)

    p2 += has_loop

print(p2)
