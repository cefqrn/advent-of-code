from itertools import groupby, product
from pathlib import Path

p1 = p2 = 0

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.splitlines()
sections = [
    list(section)
    for has_content, section in groupby(lines, bool)
    if has_content
]

grid = {}
ipos = None
epos = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        grid[x, y] = c
        if c == 'S':
            ipos = x, y
        if c == 'E':
            epos = x, y

w, h = len(line), len(lines)


directions = (0, -1), (1, 0), (0, 1), (-1, 0)

def allowed(direction):
    i = directions.index(direction)

    return directions[i-1], directions[(i+1) % len(directions)]

def inverse(direction):
    return directions[directions.index(direction)-2]

from bisect import insort
from collections import deque, defaultdict

RIGHT = (1, 0)

remaining = deque([(0, ipos, RIGHT, {ipos})])

from math import inf

seen = defaultdict(lambda: inf)
istate = ipos, RIGHT
seen[istate] = 0


best = None

in_best = set()

while remaining:
    score, pos, direction, history = remaining.popleft()
    x, y = pos

    if best is not None:
        if score > best:
            continue

    if pos == epos:
        best = score
        in_best.update(history)
        continue

    dx, dy = direction

    npos = nx, ny = x+dx, y+dy
    if grid.get(npos) != '#':
        state = npos, direction
        nscore = score + 1

        if seen[state] >= nscore:
            seen[state] = nscore
            insort(remaining, (nscore, npos, direction, history | {npos}))

    nscore = score + 1000
    for ndirection in allowed(direction):
        state = pos, ndirection
        if seen[pos, inverse(ndirection)] != inf:
            continue

        if grid.get((pos[0] + ndirection[0], pos[1] + ndirection[1])) != '.':
            continue

        if seen[state] >= nscore:
            insort(remaining, (nscore, pos, ndirection, history))

print(best)
print(len(in_best))
