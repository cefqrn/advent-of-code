from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from collections import deque, defaultdict
from bisect import insort

directions = [
    (-1, 0), # N
    (0, 1),  # E
    (1, 0),  # S
    (0, -1)  # W
]

height = len(lines)
width = len(lines[0])

possibilities = deque()
for direction in directions[1:3]:
    possibilities.append((0, (0, 0), direction, 10))

seen = defaultdict(lambda: float("inf"))
while possibilities:
    loss, (y, x), d, r = possibilities.popleft()

    if (y, x) == (height-1, width-1) and r <= 6:
        print(loss)
        break

    if r <= 6:
        di = directions.index(d)
        for nd in directions[(di+1) % 4], directions[di-1]:
            dy, dx = nd
            ny, nx = y+dy, x+dx

            if ny not in range(height) or nx not in range(width):
                continue

            nr = 9

            nloss = loss + int(lines[ny][nx])
            if seen[ny, nx, nd, nr] <= nloss:
                continue
            seen[ny, nx, nd, nr] = nloss

            insort(possibilities, (nloss, (ny, nx), nd, nr))

    if r > 0:
        dy, dx = d
        ny, nx = y+dy, x+dx

        if ny not in range(height) or nx not in range(width):
            continue

        nr = r-1
        nd = d

        nloss = loss + int(lines[ny][nx])
        if seen[ny, nx, nd, nr] <= nloss:
            continue
        seen[ny, nx, nd, nr] = nloss

        insort(possibilities, (nloss, (ny, nx), nd, nr))
