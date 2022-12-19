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

points = []
for x,y,z in map(eval, lines):
    g[x][y][z] = "#"

    points.append((x, y, z))


NEIGHBORS = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

s = 0
for x, plane in enumerate(g):
    for y, line in enumerate(plane):
        for z, char in enumerate(line):
            if char == " ":
                continue
                
            neighbor_count = 0
            for dx, dy, dz in NEIGHBORS:
                nx, ny, nz = x+dx, y+dy, z+dz
                if not grid.is_valid_grid_coord(g, nx, ny, nz):
                    continue

                neighbor_count += g[nx][ny][nz] != " "

            s += 6 - neighbor_count
            
print(s)
