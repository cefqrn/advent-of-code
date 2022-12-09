import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

hx=hy=tx=ty=0

visited: set[tuple[int, int]] = set([(0, 0),])
for line in lines:
    match line.split():
        # only worked by coincidence
        # the head moves one spot at a time
        case ["L", n]:
            hx -= int(n)

        case ["R", n]:
            hx += int(n)

        case ["U", n]:
            hy -= int(n)

        case ["D", n]:
            hy += int(n)

    while (abs(hd := hx - tx) > 1) or (abs(hy - ty) > 1):
        vd = hy - ty
        if hd and vd:
            tx += hd // abs(hd)
            ty += vd // abs(vd)
            visited.add((tx, ty))
            continue

        if hd:
            tx += hd // abs(hd)
            visited.add((tx, ty))
            continue

        if vd:
            ty += vd // abs(vd)
            visited.add((tx, ty))

print(len(visited))
