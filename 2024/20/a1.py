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

def h(x, y):
    # return 0
    return abs(x-epos[0]) + abs(y-epos[0])

from functools import cache
@cache
def get_path_no_cheat(ipos):
    remaining = [(0, ipos)]
    seen = set()
    while remaining:
        score, pos = heappop(remaining)
        x, y = pos

        if pos == epos:
            return score

        for dx, dy in DIRECTIONS:
            npos = nx, ny = x+dx, y+dy

            if grid.get(npos, '#') == '#':
                continue

            if npos in seen:
                continue
            seen.add(npos)

            heappush(remaining, (score+1, npos))

    return None

def get_path(cheats=0, used=None, best=None):
    remaining = [(0, 0, cheats, False, ipos, None)]
    seen = set() if used is None else set(used)
    while remaining:
        _, score, cheating, cheated, pos, cheat = heappop(remaining)
        x, y = pos

        if pos == epos:
            return score, cheat

        if best is not None and score > best:
            continue

        score += 1
        for dx, dy in DIRECTIONS:
            npos = nx, ny = x+dx, y+dy

            if npos not in grid:
                continue

            state = (npos, cheat)
            if state in seen:
                continue
            seen.add(state)

            if cheated and cheating:
                if cheating == 1:
                    if grid.get(npos) == '#':
                        continue

                    nscore = score + get_path_no_cheat(npos)
                    heappush(remaining, (nscore, nscore, cheating-1, cheated, epos, cheat))
                else:
                    heappush(remaining, (score+h(nx,ny), score, cheating-1, cheated, npos, cheat))
            elif grid.get(npos) != '#':
                heappush(remaining, (score+h(nx,ny), score, cheating, cheated, npos, cheat))
            elif cheats and not cheated:
                ncheat = (pos, (dx, dy))
                if ncheat in seen:
                    continue

                heappush(remaining, (score+h(nx,ny), score, cheating-1, True, npos, ncheat))

    return None


no_cheat, z = get_path()
best = no_cheat
print(no_cheat, z)
print('aaaa')
found = set()
while True:
    with_cheat, cheat_used = get_path(2, found, no_cheat)
    if no_cheat - with_cheat < 100:
        break

    print(no_cheat - with_cheat, cheat_used)
    found.add(cheat_used)


# for pos in product(range(w), range(h)):
#     x, y = pos

# for section in sections:
#     section

# for line in lines:
#     line

print(len(found))

# print(p1)
# print(p2)
