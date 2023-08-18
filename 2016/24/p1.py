from __future__ import annotations

from collections import defaultdict
from itertools import permutations, combinations, pairwise, chain, tee
from typing import NamedTuple
from heapq import heappush, heappop

class Position(NamedTuple):
    x: int
    y: int

    @property
    def neighbors(self) -> list[Position]:
        return [
            Position(self.x+dx, self.y+dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))
        ]

    def distance_to(self, other: Position) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

def h(position: Position, target: Position) -> int:
    return position.distance_to(target)

with open(0) as f:
    lines = f.read().split()
data = "".join(lines)
w = len(lines[0])

def position_to_index(position: Position) -> int:
    return position.y * w + position.x

def index_to_position(index: int) -> Position:
    y, x = divmod(index, w)
    return Position(x, y)

def shortest_distance(maze: str, initial: Position, target: Position):
    possibilities = [(
        0, 0, initial
    )]

    seen = {initial: 0}
    while possibilities:
        _, cost, position = heappop(possibilities)
        if position == target:
            return cost
        
        cost += 1
        for neighbor in position.neighbors:
            if maze[position_to_index(neighbor)] == '#':
                continue
            if (prev_cost := seen.get(neighbor)) is not None and prev_cost <= cost:
                continue
            seen[neighbor] = cost
            heappush(possibilities, (
                cost + h(neighbor, target),
                cost,
                neighbor
            ))

waypoints = set(filter(str.isdigit, data))

distances = defaultdict(dict)
for a, b in combinations(waypoints, r=2):
    a_position = index_to_position(data.index(a))
    b_position = index_to_position(data.index(b))

    distance = shortest_distance(data, a_position, b_position)
    distances[a][b] = distance
    distances[b][a] = distance

def get_total_distance_a(order) -> int:
    return sum(distances[a][b] for a, b in pairwise(chain('0', order)))

def get_total_distance_b(order) -> int:
    return sum(distances[a][b] for a, b in pairwise(chain('0', order, '0')))

non_zero_waypoints = tuple(filter(int, waypoints))
perm_a, perm_b = tee(permutations(non_zero_waypoints))

print(min(map(get_total_distance_a, perm_a)), min(map(get_total_distance_b, perm_b)))
