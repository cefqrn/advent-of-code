from dataclasses import dataclass, field
from typing import NamedTuple
from heapq import heappush, heappop

class Position(NamedTuple):
    x: int
    y: int

    @property
    def neighbors(self):
        return [
            Position(self.x+dx, self.y+dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0))
        ]

def h(empty_position: Position, goal_position: Position):
    ex, ey = empty_position
    ix, iy = goal_position

    dx, dy = abs(ex - ix), abs(ey - iy)
    eh = 1 if max(dx, dy) < 2 else dx + dy

    return ix + iy + eh
    
@dataclass(order=True, slots=True)
class Possibility:
    expected_cost: int
    cost: int                = field(compare=False)
    empty_position: Position = field(compare=False)
    goal_position: Position  = field(compare=False)

with open(0) as f:
    data = f.readlines()[2:]

nodes: set[Position] = set()
empty = None
goal = None
for node in data:
    filesystem, _, used, *_ = node.split()

    used = int(used[:-1])
    if used > 300:
        continue

    position = _, y =  Position(*(int(x[1:]) for x in filesystem.rsplit("/", 1)[-1][5:].split("-")))
    if used == 0:
        empty = position

    if y == 0 and (goal is None or goal < position):
        goal = position

    nodes.add(position)

assert empty is not None
assert goal is not None

target = Position(0, 0)
possibilities = [Possibility(
    h(empty, goal),
    0,
    empty,
    goal
)]
seen = {(empty, goal): 0}

best = 999
attempts = 0
while possibilities:
    possibility = heappop(possibilities)
    attempts += 1
    cost = possibility.cost
    empty = possibility.empty_position
    goal = possibility.goal_position

    if h(empty, goal) < best:
        print("new best:", h(empty, goal), f"({empty}, {goal})")
        best = h(empty, goal)

    if goal == target:
        print(len(nodes) - 1, cost, attempts)
        break

    cost += 1
    for neighbor in empty.neighbors:
        if neighbor not in nodes:
            continue

        new_empty = neighbor
        new_goal = goal
        if neighbor == goal:
            new_goal = empty

        if (previous_cost := seen.get((new_empty, new_goal))) is not None and previous_cost <= cost:
            continue
        seen[(new_empty, new_goal)] = cost

        heappush(possibilities, Possibility(
            cost + h(neighbor, new_goal),
            cost,
            neighbor,
            new_goal
        ))
