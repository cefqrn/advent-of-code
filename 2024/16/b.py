with open(0) as f:
    lines = f.readlines()

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

directions = (0, -1), (1, 0), (0, 1), (-1, 0)

def allowed(direction):
    i = directions.index(direction)
    return directions[i-1], directions[i-3]

def inverse(direction):
    return directions[directions.index(direction)-2]

from collections import defaultdict
from heapq import heappush, heappop

RIGHT = (1, 0)

remaining = [(0, ipos, RIGHT, {ipos})]

from math import inf

seen = defaultdict(lambda: inf)
istate = ipos, RIGHT
seen[istate] = 0


best = None

in_best = set()

while remaining:
    score, pos, direction, history = heappop(remaining)
    x, y = pos

    if best is not None and score > best:
        continue

    if pos == epos:
        best = score
        in_best.update(history)
        print(len(remaining))
        continue

    dx, dy = direction

    npos = nx, ny = x+dx, y+dy
    if grid.get(npos) != '#':
        state = npos, direction
        nscore = score + 1

        if seen[state] >= nscore:
            seen[state] = nscore
            heappush(remaining, (nscore, npos, direction, history | {npos}))

    nscore = score + 1000
    for ndirection in allowed(direction):
        state = pos, ndirection
        if seen[pos, inverse(ndirection)] != inf:
            continue

        if grid.get((pos[0] + ndirection[0], pos[1] + ndirection[1])) != '.':
            continue

        if seen[state] >= nscore:
            heappush(remaining, (nscore, pos, ndirection, history))

print(best)
print(len(in_best))
