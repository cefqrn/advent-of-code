import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib import *

g = []
for i in range(30):
    x = []
    g.append(x)
    for j in range(30):
        y = []
        x.append(y)
        for z in range(30):
            y.append(" ")

for x,y,z in map(eval, lines):
    g[x+1][y+1][z+1] = "#"

f = set()

NEIGHBORS = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

first = []
s = 0
remaining = [(0, 0, 0)]
visited = set()
while remaining:
    x, y, z = remaining.pop()

    for dx, dy, dz in NEIGHBORS:
        nx, ny, nz = x+dx, y+dy, z+dz
        if not grid.is_valid_grid_coord(g, nx, ny, nz):
            continue

        if g[nx][ny][nz] == " ":
            if (nx, ny, nz) in visited:
                continue
            
            visited.add((nx, ny, nz))
            remaining.append((nx, ny, nz))
        else:
            s += 1
            
print(s)
