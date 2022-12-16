from dataclasses import dataclass
from time import perf_counter
from re import findall

st = perf_counter()


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    
    def __repr__(self):
        return f"({self.x}, {self.y})"


squares = []
with open(0) as f:
    for i, line in enumerate(f.readlines()):
        x, y, bx, by = map(int, findall(r"[-+]?\d+", line))
        dist = abs(x-bx) + abs(y-by)

        diamond = [
            Point(x, y+dist),
            Point(x+dist, y),
            Point(x, y-dist),
            Point(x-dist, y)
        ]

        squares.append(diamond)

for s in squares:
    print(f"polygon({s})")

# shove it into desmos and find the empty point
