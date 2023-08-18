from __future__ import annotations

from dataclasses import dataclass, replace, field
from collections import UserDict
from typing import NamedTuple
from heapq import heappush, heappop

from collections.abc import Iterable

class Position(NamedTuple):
    x: int
    y: int

important_data_position = None
@dataclass(slots=True, frozen=True)
class Node:
    position: Position
    size: int
    used: int
    important: int

    @property
    def available(self):
        return self.size - self.used
    
    @staticmethod
    def from_str(s: str) -> Node:
        filesystem, size, used, *_ = s.split()
        size = int(size[:-1])
        used = int(used[:-1])
        important = 0

        x, y = filesystem.rsplit("/", 1)[-1][5:].split("-")
        position = Position(int(x[1:]), int(y[1:]))
        if position == important_data_position:
            important = used

        return Node(
            position,
            size,
            used,
            important
        )

class NotEnoughSpaceError(Exception): ...

class NodeGrid(UserDict):
    def __init__(self, *args, important_position: Position=None, empty_spot: Position=None, **kwargs):
        self.goal_spot = important_position
        self.empty_spot = empty_spot
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_nodes(nodes: Iterable[Node]) -> NodeGrid:
        grid = NodeGrid()
        highest_x = 0
        empty_spot = None
        for node in nodes:
            grid[node.position] = node
            highest_x = max(highest_x, node.position.x)
            if not node.used:
                empty_spot = node.position

        if empty_spot is None:
            raise ValueError
        
        grid.empty_spot = empty_spot
        grid.goal_spot = goal_spot = Position(highest_x, 0)

        prev = grid[goal_spot]
        grid[goal_spot] = replace(prev, important=prev.used)

        return grid

    def available_neighbors_of(self, node: Node) -> list[Node]:
        neighbors = []
        x, y = node.position
        for dx, dy in (0, 1), (1, 0), (0, -1), (-1, 0):
            neighbor_position = x + dx, y + dy
            if (neighbor := self.data.get(neighbor_position, None)) is not None and neighbor.available >= node.used:
                neighbors.append(neighbor)
        
        return neighbors
                
    def moved(self, from_node: Node, to_node: Node) -> NodeGrid:
        new_data = self.data.copy()
        new_data[from_node.position] = replace(from_node, used=0, important=0)
        new_data[to_node.position] = replace(
            to_node,
            used=to_node.used + from_node.used,
            important=from_node.important
        )

        new_important_position = self.goal_spot
        if from_node.important:
            new_important_position = to_node.position

        return NodeGrid(new_data, important_position=new_important_position, empty_spot=from_node.position)

    def __hash__(self):
        return hash(tuple(sorted(self.data.items())))

@dataclass(order=True, slots=True)
class Possibility:
    expected_cost: int
    cost: int
    grid: NodeGrid = field(compare=False)

def h(grid: NodeGrid):
    ix, iy = grid.goal_spot
    ex, ey = grid.empty_spot
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

    if (dist := expected - cost) < closest:
        print("new closest:", dist, f"({grid.goal_spot}, {grid.empty_spot})", len(possibilities))
        closest = dist

    if grid.goal_spot == (0, 0):
        print(cost)
        break

    cost += 1
    for node in grid.values():
        for neighbor in grid.available_neighbors_of(node):
            new_grid = grid.moved(node, neighbor)

            if new_grid in seen and seen[new_grid] <= cost:
                continue
            seen[new_grid] = cost

            heappush(possibilities, Possibility(
                cost + h(new_grid),
                cost,
                new_grid
            ))
