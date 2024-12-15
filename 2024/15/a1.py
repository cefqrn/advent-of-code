from itertools import groupby, product
from pathlib import Path

p1 = p2 = 0

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.splitlines()
sections = [
    list(section)
    for has_content, section in groupby(lines, bool)
    if has_content
]

a, b = sections

b = "".join(b)
# print(b)


grid = {}
ipos = None
for y, line in enumerate(a):
    for x, c in enumerate(line):
        grid[x, y] = c
        if c == '@':
            ipos = x, y
            grid[x, y] = '.'

w, h = len(line), len(a)

# print(w, h)

x, y = ipos

def parse(instruction):
    match instruction:
        case "^":
            return 0, -1
        case ">":
            return 1, 0
        case "v":
            return 0, 1
        case "<":
            return -1, 0

def push(instruction, ipos) -> bool:
    x, y = ipos
    dx, dy = parse(instruction)

    npos = x+dx, y+dy
    if grid[npos] == "#":
        return False

    if grid[npos] == "O":
        if push(instruction, npos):
            grid[npos] = "O"
        else:
            return False

    grid[npos] = "O"
    return True


def attempt(instruction, ipos):
    x, y = ipos
    dx, dy = parse(instruction)

    npos = x+dx, y+dy

    if npos not in grid or grid[npos] == '#':
        return ipos

    if grid[npos] == 'O':
        if push(instruction, npos):
            grid[npos] = "."
        else:
            return ipos

    return npos

def gps(x, y):
    return (y) * 100 + (x)

def print_grid(pos):
    for y in range(h):
        l = ""
        for x in range(w):
            if (x, y) == pos:
                c = "@"
            else:
                c = grid[x, y]
            l += " " +c

        print(l)

for i, instruction in enumerate(b):
    x, y = attempt(instruction, (x, y))
    # print()
    # print(i, instruction)
    # print_grid((x, y))

    # if i > 20:
        # input()
        # break


for y in range(h):
    for x in range(w):
        if grid[x, y] == "O":
            p1 += gps(x, y)

print(p1)
# print(p2)
