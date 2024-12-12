from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

grid = {}
ipos = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        grid[x, y] = c
        if c == '':
            ipos = x, y

w, h = len(line), len(lines)

directions = (-1, 0), (0, 1), (1, 0), (0, -1)

def in_bounds(x, y):
    return 0 <= x < w and 0 <= y < h

def get_inside(ix, iy):
    inside = set()
    seen = set()

    c = grid[ix, iy]

    left = [(ix, iy)]
    while left:
        pos = x, y = left.pop()
        inside.add(pos)
        for dx, dy in directions:
            npos = nx, ny = x+dx, y+dy

            if npos in seen: continue
            seen.add(npos)

            if not in_bounds(nx, ny):
                continue

            if grid[nx, ny] != c:
                continue

            left.append(npos)

    return inside


observed = set()

p1 = p2 = 0

from itertools import product
for pos in product(range(w), range(h)):
    if pos in observed:
        continue

    x, y = pos
    inside = get_inside(x, y)

    sides_seen = set()

    perimeter = 0
    sides = 0
    for x, y in sorted(inside):
        for direction in directions:
            dx, dy = direction
            npos = nx, ny = x+dx, y+dy

            if npos in inside:
                continue

            perimeter += 1

            ldx, ldy = directions[(directions.index(direction) - 1) % 4]
            rdx, rdy = directions[(directions.index(direction) + 1) % 4]

            wall = (npos, direction)
            sides_seen.add(wall)

            left_wall = ((nx+ldx, ny+ldy), direction)
            right_wall = ((nx+rdx, ny+rdy), direction)

            sides += left_wall not in sides_seen and right_wall not in sides_seen

    p1 += len(inside) * perimeter
    p2 += len(inside) * sides

    observed.update(inside)

print(p1)
print(p2)
