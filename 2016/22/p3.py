from __future__ import annotations

from dataclasses import dataclass, replace, field
from collections import UserDict
from typing import NamedTuple, ClassVar
from heapq import heappush, heappop

from collections.abc import Iterable

class Position(NamedTuple):
    x: int
    y: int

@dataclass(slots=True, frozen=True)
class Node:
    position: Position
    important: bool
    empty: bool
    unmovable: ClassVar[list[Position]]
    
    @classmethod
    def from_str(cls, s: str) -> Node:
        filesystem, _, used, *_ = s.split()
        used = int(used[:-1])

        x, y = filesystem.rsplit("/", 1)[-1][5:].split("-")
        position = Position(int(x[1:]), int(y[1:]))
        if used > 300:
            cls.unmovable.append()

        return Node(
            Position(int(x[1:]), int(y[1:])),
            unmovable=used > 300,
            important=False,
            empty=not used
        )

class NodeGrid(UserDict):
    def __init__(self, *args, important_position: Position=None, empty_position: Position=None, **kwargs):
        self.goal_position = important_position
        self.empty_position = empty_position
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_nodes(nodes: Iterable[Node]) -> NodeGrid:
        grid = NodeGrid()
        goal_position = Position(0, 0)
        empty_position = None
        for node in nodes:
            grid[node.position] = node
            if node.position.y == 0:
                goal_position = max(goal_position, node.position)

            if node.empty:
                empty_position = node.position

        if empty_position is None:
            raise ValueError
        
        grid.empty_position = empty_position
        grid.goal_position = goal_position

        grid[goal_position] = replace(grid[goal_position], important=True)

        return grid

    def neighbors_of(self, node: Node) -> list[Node]:
        x, y = node.position

        return [
            neighbor
            for neighbor_position in ((x, y+1), (x+1, y), (x, y-1), (x-1, y))
            if (neighbor := self.get(neighbor_position)) is not None
            and not neighbor.unmovable
        ]
                
    def moved(self, from_node: Node, to_node: Node) -> NodeGrid:
        new_grid = self.copy()
        new_grid[from_node.position] = replace(from_node, empty=True, important=False)
        new_grid[to_node.position] = replace(to_node, empty=False, important=from_node.important)

        new_grid.empty_position = from_node.position
        if from_node.important:
            new_grid.goal_position = to_node.position

        return new_grid

    def __hash__(self):
        return hash(tuple(sorted(self.data.items())))

@dataclass(order=True, slots=True)
class Possibility:
    expected_cost: int
    cost: int
    grid: NodeGrid = field(compare=False)

def h(grid: NodeGrid):
    ix, iy = grid.goal_position
    ex, ey = grid.empty_position
    return (ix + iy) + max(abs(ex - ix), abs(ey - iy))

with open(0) as f:
    data = f.readlines()[2:]

grid = NodeGrid.from_nodes(map(Node.from_str, data))
possibilities = [Possibility(
    0 + h(grid),
    0,
    grid
)]
seen = {0: grid}
closest = 9999
while possibilities:
    possibility = heappop(possibilities)
    expected, cost, grid = possibility.expected_cost, possibility.cost, possibility.grid

    if (dist := expected - cost) < closest or grid.empty_position.y < 21:
        print("new closest:", dist, f"({grid.goal_position}, {grid.empty_position})", len(possibilities))
        closest = dist

    if grid.goal_position == (0, 0):
        print(cost)
        break

    cost += 1
    empty_node = grid[grid.empty_position]
    for neighbor in grid.neighbors_of(empty_node):
        new_grid = grid.moved(neighbor, empty_node)

        if new_grid in seen and seen[new_grid] < cost:
            continue
        seen[new_grid] = cost

        heappush(possibilities, Possibility(
            cost + h(new_grid),
            cost,
            new_grid
        ))
