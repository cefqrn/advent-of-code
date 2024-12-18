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

DIRECTIONS = (0, -1), (1, 0), (0, 1), (-1, 0)
UP, RIGHT, DOWN, LEFT = NORTH, EAST, SOUTH, WEST = DIRECTIONS

def    left(d): return DIRECTIONS[DIRECTIONS.index(d)-1]
def inverse(d): return DIRECTIONS[DIRECTIONS.index(d)-2]
def   right(d): return DIRECTIONS[DIRECTIONS.index(d)-3]
def  others(d): return left(d), inverse(d), right(d)
def   sides(d): return left(d), right(d)

grid = {}
ipos = 0, 0

# w, h = 7, 7
w, h = 71, 71
epos = w-1, h-1

from heapq import heappush, heappop

def get_path():
    remaining = [(0, ipos, {ipos})]
    seen = set()
    while remaining:
        score, pos, history = heappop(remaining)
        x, y = pos

        if pos == epos:
            return history

        for dx, dy in DIRECTIONS:
            npos = nx, ny = x+dx, y+dy

            if grid.get(npos) != '.':
                continue

            if npos in seen:
                continue
            seen.add(npos)

            heappush(remaining, (score+1, npos, history | {npos}))

    return None

for x, y in product(range(w), range(h)):
    grid[x, y] = '.'

for line in lines[:1024]:
    grid[eval(line)] = "#"

print(len(path := get_path()) - 1)

for i, line in enumerate(lines[1024:], 1024):
    pos = eval(line)
    grid[pos] = "#"
    if pos in path:
        path = get_path()
        if path is None:
            print(",".join(map(str, pos)))
            break
