from typing import NamedTuple

class Vec2(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        x, y = other
        return Vec2(self.x + x, self.y + y)

    __radd__ = __add__

dpad_positions = {}
dpad = {}
for y, line in enumerate([" ^A", "<v>"]):
    for x, c in enumerate(line):
        if c == " ": continue
        dpad[x, y] = c
        dpad_positions[c] = x, y

npad_positions = {}
npad = {}
for y, line in enumerate(["789", "456", "123", " 0A"]):
    for x, c in enumerate(line):
        if c == " ": continue
        npad[x, y] = c
        npad_positions[c] = x, y

DIRECTIONS = Vec2(0, -1), Vec2(1, 0), Vec2(0, 1), Vec2(-1, 0)

def steps(ipos, epos):
    x, y = ipos
    ex, ey = epos
    d = []
    while x < ex:  # right
        x += 1
        d += DIRECTIONS[1],
    while y > ey:  # up
        y -= 1
        d += DIRECTIONS[0],
    while y < ey:  # down
        y += 1
        d += DIRECTIONS[2],
    while x > ex:  # left
        x -= 1
        d += DIRECTIONS[3],

    return d

from collections import Counter
from itertools import chain, permutations, repeat, starmap
from functools import cache

def steps_to(ipos, epos, iothers, grid=dpad):
    best = None
    best_others = None
    for possibility in permutations(Counter(steps(ipos, epos)).items()):
        others = iothers
        pos = ipos

        s = 0
        for d in chain.from_iterable(starmap(repeat, possibility)):
            pos += d
            if grid.get(pos, " ") == " ":
                break

            cost, others = solve(show_d(d), others)
            s += cost
        else:
            cost, others = solve("A", others)
            s += cost

            if best is None or s < best:
                best = s
                best_others = others

    return best or float("inf"), best_others

@cache
def solve(needed_button, bots):
    if not bots:  # press button directly
        return 1, bots

    ipos, iothers = bots[0], bots[1:]
    epos = dpad_positions[needed_button]

    s, others = steps_to(ipos, epos, iothers)

    return s, (epos, *others)

def show_d(d):
    return "^>v<"[DIRECTIONS.index(d)]

def read_d(d):
    return DIRECTIONS["^>v<".index(d)]

with open(0) as f:
    data = f.read()

for bot_count in 2, 25:
    total = 0
    for code in data.splitlines():
        pos = npad_positions["A"]
        others = tuple(repeat(dpad_positions["A"], bot_count))

        s = 0
        for button in code:
            cost, others = steps_to(pos, pos := npad_positions[button], others, npad)
            s += cost

        total += s * int(code[:-1])

    print(total)
