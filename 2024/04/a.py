from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

p1 = p2 = 0

from itertools import product
directions = list(filter(any, ((dx, dy) for dx, dy in product((1, 0, -1), repeat=2))))

from operator import add
def find(s, pos, direction):
    if not s:
        return 1

    x, y = pos
    if x < 0 or y < 0:
        return 0

    try:
        if s[0] != lines[y][x]:
            return 0
    except IndexError:
        return 0

    return find(s[1:], list(map(add, pos, direction)), direction)

for y, line in enumerate(lines):
    for x, _ in enumerate(line):
        pos = x, y
        for direction in directions:
            p1 += find("XMAS", pos, direction)

def transposed(it):
    return list(zip(*it))

def rotated_cw(it, n=1):
    for _ in range(n % 4):
        it = list(map(list, map(reversed, zip(*it))))

    return it

for _ in range(4):
    for y, line in enumerate(lines):
        for x, _ in enumerate(line):
            pos = x, y

            p2 += find("MAS", pos, (1, 1)) and find("MAS", (x + 2, y), (-1, 1))

    lines = rotated_cw(lines)

print(p1)
print(p2)
