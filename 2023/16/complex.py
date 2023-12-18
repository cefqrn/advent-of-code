from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

from itertools import starmap

# NESW
directions = [
    -1 + 0j,
     0 + 1j,
     1 + 0j,
     0 - 1j
]

lines = data.splitlines()

width = len(lines[0])
height = len(lines)

spots = {}
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        spots[y + x*1j] = c


def energized_count(position, direction):
    seen = set()
    possibilities = [(position, direction)]
    while possibilities:
        state = position, direction = possibilities.pop()

        try:
            spot = spots[position]
        except KeyError:
            continue

        if state in seen:
            continue
        seen.add(state)

        direction_index = directions.index(direction)
        if spot in "/\\":
            new_direction = direction * ((1 | -(direction_index & 1)) * " \\".find(spot) * 1j)
            new_position = position + new_direction

            possibilities.append((new_position, new_direction))

            continue

        if "|-".find(spot) ^ (direction_index & 1) > 0:
            for rotation in 1j, -1j:
                new_direction = direction * rotation
                new_position = position + new_direction

                possibilities.append((new_position, new_direction))

            continue

        new_direction = direction
        new_position = position + direction

        possibilities.append((new_position, new_direction))

    return len({position for position, _ in seen})


def starting_states(width, height):
    yield from ((y, 1j) for y in range(height))
    yield from ((y + (width-1) * 1j, -1j) for y in range(height))
    yield from ((x*1j, 1) for x in range(width))
    yield from (((height-1) + x*1j, -1) for x in range(width))


print(
    energized_count(0 + 0j, directions[1]),
    max(starmap(energized_count, starting_states(width, height)))
)
