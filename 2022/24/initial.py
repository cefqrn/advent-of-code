import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *

from aoclib.point import Point

from collections import defaultdict, deque

UP     = Point( 0, -1)
DOWN   = Point( 0,  1)
LEFT   = Point(-1,  0)
RIGHT  = Point( 1,  0)
WAIT   = Point( 0,  0)

directions = {
    "^": UP,
    "v": DOWN,
    "<": LEFT,
    ">": RIGHT,
    " ": WAIT
}

minx = 1
miny = 1
maxx = len(lines[0]) - 2
maxy = len(lines) - 2

START = Point(1, 0)
EXIT = Point(maxx, maxy+1)


def next_room(room):
    new_room = defaultdict(list)
    for coord, element in room.items():
        for blizzard in element:
            if blizzard in "<>":
                new_coord = Point((coord.x - 1 + directions[blizzard].x) % maxx + 1, coord.y)
                new_room[new_coord].append(blizzard)
            elif blizzard in "v^":
                new_coord = Point(coord.x, (coord.y - 1 + directions[blizzard].y) % maxy + 1)
                new_room[new_coord].append(blizzard)
            elif blizzard == "#":
                new_room[coord].append(blizzard)  # wall

    return new_room


g = [defaultdict(list)]
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c in "<>v^#":
            g[0][Point(x, y)].append(c)

possibilities = deque([(Point(1, 0), 0)])
tried = {possibilities[0]}

while possibilities:
    position, time = possibilities.popleft()

    if position == EXIT:
        initial_end = time
        break

    for diff in directions.values():
        new_position, new_time = new_state = position + diff, time + 1

        if new_state in tried:
            continue

        tried.add(new_state)

        if new_time >= len(g):
            g.append(next_room(g[time]))

        if g[new_time][new_position]:
            continue

        if new_position.y < 0:
            continue

        possibilities.append(new_state)

possibilities = deque([(EXIT, initial_end)])
tried = {possibilities[0]}

while possibilities:
    position, time = possibilities.popleft()

    if position == START:
        back_to_start = time
        break

    for diff in directions.values():
        new_position, new_time = new_state = position + diff, time + 1

        if new_state in tried:
            continue

        tried.add(new_state)

        if new_time >= len(g):
            g.append(next_room(g[time]))

        if g[new_time][new_position]:
            continue

        if new_position.y < 0:
            continue

        possibilities.append(new_state)

possibilities = deque([(START, back_to_start)])
tried = {possibilities[0]}

while possibilities:
    position, time = possibilities.popleft()

    if position == EXIT:
        print(time)
        break

    for diff in directions.values():
        new_position, new_time = new_state = position + diff, time + 1

        if new_state in tried:
            continue

        tried.add(new_state)

        if new_time >= len(g):
            g.append(next_room(g[time]))

        if g[new_time][new_position]:
            continue

        if new_position.y < 0:
            continue

        possibilities.append(new_state)