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
        if c == "O":
            grid[2*x, y] = "["
            grid[2*x+1, y] = "]"
        elif c == '@':
            ipos = 2*x, y
            grid[2*x, y] = "."
            grid[2*x+1, y] = "."
        else:
            grid[2*x, y] = c
            grid[2*x+1, y] = c


w, h = len(line)*2, len(a)

# print(w, h)

x, y = ipos

def left(instruction):
    match instruction:
        case "^":
            return -1, 0
        case "v":
            return 1, 0

    raise ValueError

def right(instruction):
    match instruction:
        case "^":
            return 1, 0
        case "v":
            return -1, 0

    raise ValueError

def invert(instruction):
    match instruction:
        case "^":
            return 0, 1
        case ">":
            return -1, 0
        case "v":
            return 0, -1
        case "<":
            return 1, 0

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

def attempt(instruction, ipos):
    x, y = ipos
    dx, dy = parse(instruction)

    npos = x+dx, y+dy

    if npos not in grid or grid[npos] == '#':
        return []

    if grid[npos] in '[]':
        if instruction in "<>":
            if a := attempt(instruction, npos):
                return a + [(npos, ipos)]
            else:
                return []

        if grid[npos] == "[" and instruction == "^" or grid[npos] == "]" and instruction == "v":
            dx1, dy1 = right(instruction)
        else:
            dx1, dy1 = left(instruction)

        npos2 = x+dx+dx1, y+dy+dy1

        a = attempt(instruction, npos)
        b = attempt(instruction, npos2)
        if a and b:
            return a + b + [(npos, ipos), (npos2, ipos)]
        else:
            return []

    return [(npos, ipos)]

def print_grid(pos):
    for y in range(h):
        l = ""
        for x in range(w):
            if (x, y) == pos:
                c = "@"
            else:
                c = grid[x, y]
            l += c

        print(l)

from collections import defaultdict


def move(moves):
    curr = grid.copy()
    pushed = defaultdict(int)
    for newpos, prevpos in moves:
        # x, y = newpos
        # dx, dy = invert(instruction)
        # prevpos = x+dx, y+dy

        pushed[prevpos] = True

    # print(pushed)

    for newpos, _ in moves:
        x, y = newpos
        dx, dy = invert(instruction)
        prevpos = x+dx, y+dy

        if pushed[prevpos]:
            grid[newpos] = curr[prevpos]
        else:
            grid[newpos] = '.'

pos = x, y
# print_grid(pos)
for i, instruction in enumerate(b):
    moves = attempt(instruction, pos)
    if moves:
        move(moves)

        dx, dy = parse(instruction)
        pos = x, y = x+dx, y+dy




def gps(x, y):
    return y * 100 + x#min(x, w-x-2)


for y in range(h):
    for x in range(w):
        if grid[x, y] == "[":
            # print(x, y, gps(x, y))
            p1 += gps(x, y)

# print_grid(pos)

print(p1)
# print(p2)

##[].......[].[][]##
##......[][]..[]..##