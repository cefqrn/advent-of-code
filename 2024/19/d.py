from itertools import groupby, product
from pathlib import Path
from re import findall

p1 = p2 = 0

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
ints = list(map(int, findall(r"[-+]?\d+", contents)))
lines = contents.splitlines()
sections = [
    list(section)
    for has_content, section in groupby(lines, bool)
    if has_content
]

def batched(it, n):
    return list(zip(*n*[iter(it)]))

DIRECTIONS = (0, -1), (1, 0), (0, 1), (-1, 0)
UP, RIGHT, DOWN, LEFT = NORTH, EAST, SOUTH, WEST = DIRECTIONS

def    left(d): return DIRECTIONS[DIRECTIONS.index(d)-1]
def inverse(d): return DIRECTIONS[DIRECTIONS.index(d)-2]
def   right(d): return DIRECTIONS[DIRECTIONS.index(d)-3]
def  others(d): return left(d), inverse(d), right(d)
def   sides(d): return left(d), right(d)

grid = {}
ipos = None
epos = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        grid[x, y] = c
        if c == '':
            ipos = x, y
        if c == '':
            epos = x, y

w, h = len(line), len(lines)

a, b = sections
patterns, = a

patterns = patterns.split(", ")


from functools import cache

@cache
def can_create(design, i=0):
    if i >= len(design):
        return 1

    s = 0
    for pattern in patterns:
        if design.startswith(pattern, i):
            pattern_length = len(pattern)
            s += can_create(design, i+pattern_length)

    return s

for design in b:
    c = can_create(design)
    p1 += bool(c)
    p2 += c

print(p1)
print(p2)
