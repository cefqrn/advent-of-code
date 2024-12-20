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
        if c == 'S':
            ipos = x, y
        if c == 'E':
            epos = x, y

w, h = len(line), len(lines)

from heapq import heappush, heappop

def dist(p, q):
    a, b = p
    c, d = q

    return abs(a-c) + abs(b-d)

def get_surrounding(ipos, max_distance):
    x, y = ipos
    for dx, dy in product(range(-max_distance, max_distance+1), repeat=2):
        npos = nx, ny = x+dx, y+dy
        if npos != ipos and dist(ipos, npos) <= max_distance:
            yield npos

def get_times_no_cheats():
    remaining = [(0, epos)]
    seen = {epos: 0}

    while remaining:
        score, pos = heappop(remaining)
        x, y = pos

        score += 1
        for dx, dy in DIRECTIONS:
            npos = nx, ny = x+dx, y+dy

            if npos in seen:
                continue
            seen[npos] = score

            if grid.get(npos, '#') != '#':
                heappush(remaining, (score, npos))

    return seen

from collections import Counter

def get_path(ipos, time):
    remaining = [(0, ipos)]
    seen = {ipos}

    times = get_times_no_cheats()

    sols = Counter()
    while remaining:
        score, pos = heappop(remaining)
        x, y = pos

        if pos == epos:
            return sum(v for k, v in sols.items() if k <= score - 100)

        for end in get_surrounding(pos, time):
            if grid.get(end, '#') == '#':
                continue

            ncheat = pos, end
            if ncheat in seen:
                continue
            seen.add(ncheat)

            sols[score + dist(pos, end) + times[end]] += 1

        for dx, dy in DIRECTIONS:
            npos = nx, ny = x+dx, y+dy

            if npos in seen:
                continue
            seen.add(npos)

            if grid[npos] != '#':
                heappush(remaining, (score+1, npos))

    return None

print(get_path(ipos, 2))
print(get_path(ipos, 20))
