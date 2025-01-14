from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

p1 = p2 = 0

directions = (0, -1), (1, 0), (0, 1), (-1, 0),

from collections import defaultdict

spots = defaultdict(lambda: '.')

initial_pos = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "^":
            c = '.'
            initial_pos = x, y

        spots[x, y] = c


spots_seen = set()
def can_place(obs_x, obs_y):
    global spots_seen
    if spots[obs_x, obs_y] == '#':
        return 0

    pos = initial_pos
    spots[obs_x, obs_y] = "#"

    seen = set()
    spots_seen = set()
    current_direction = (0, -1)
    while (pos, current_direction) not in seen:
        seen.add((pos, current_direction))
        spots_seen.add(pos)

        x, y = pos
        dx, dy = current_direction

        nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or nx >= len(lines[0]) or ny >= len(lines):
            break

        while spots[nx, ny] == '#':
            dx, dy = current_direction = directions[(directions.index(current_direction) + 1) % 4]
            nx, ny = x + dx, y + dy

        pos = nx, ny
    else:
        spots[obs_x, obs_y] = "."
        return 1

    spots[obs_x, obs_y] = "."
    return 0

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        p2 += can_place(x, y)

can_place(99999999, 999999999)
print(len(spots_seen))
print(p2)
