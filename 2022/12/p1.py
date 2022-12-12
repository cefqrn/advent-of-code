import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *
from collections import deque
from bisect import insort

highest = 0
highest_pos = (0,0)
start_pos = (0, 0)
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == 'S':
            start_pos = i, j
            lines[i] = lines[i][:j] + chr(ord('a') - 1) + lines[i][j+1:]
        if c == 'E':
            highest_pos = i, j
            lines[i] = lines[i][:j] + chr(ord('z') + 1) + lines[i][j+1:]


NEIGHBORS = ((0, 1), (0, -1), (1, 0), (-1, 0))

def manhattan(x, y):
    return abs(x - highest_pos[0]) + abs(y - highest_pos[0])

possible = deque([(*start_pos, 0)])
visited = {start_pos}

from collections import defaultdict
fscores = defaultdict(lambda: 999999999999)
gscores = defaultdict(lambda: 999999999999)

fscores[start_pos] = 0
gscores[start_pos] = manhattan(0, 0)

camefrom = {}

s = 0
while possible:
    x, y, s = possible.popleft()
    c = x, y
    if c == highest_pos:
        break

    for dx, dy in NEIGHBORS:
        n = nx, ny = x+dx, y+dy

        if not is_valid_grid_coord(lines, nx, ny):
            continue

        if ord(lines[nx][ny]) > ord(lines[x][y]) + 1:
            continue

        v = ord(lines[nx][ny])

        g = gscores[c] + 1
        if g < gscores[n]:
            camefrom[n] = c
            gscores[n] = g
            fscores[n] = g + manhattan(*n)
            if n not in possible:
                insort(possible, (nx, ny, s+1), key=lambda x: fscores[x])
else:
    print('could not find')

print(s)
