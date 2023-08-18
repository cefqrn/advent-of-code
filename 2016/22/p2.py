from typing import NamedTuple

class Position(NamedTuple):
    x: int
    y: int

class Node(NamedTuple):
    position: Position
    available: int
    size: int
    used: int

    def from_str(s: str):
        filesystem, size, used, available, _ = s.split()
        x, y = filesystem.rsplit("/", 1)[-1][5:].split("-")

        return Node(
            Position(int(x[1:]), int(y[1:])),
            int(size[:-1]),
            int(used[:-1]),
            int(available[:-1])
        )
    
with open(0) as f:
    nodes = tuple(map(Node.from_str, f.readlines()[2:]))

from itertools import combinations

p1 = 0
for a, b in combinations(nodes, r=2):
    p1 += a.used and a.used <= b.available
    p1 += b.used and b.used <= a.available

print(p1)