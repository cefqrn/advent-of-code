from typing import NamedTuple

class Vec2(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        x, y = other
        return Vec2(self.x + x, self.y + y)

    __radd__ = __add__

dpad_buttons = {}
dpad = {}
for y, line in enumerate([" ^A", "<v>"]):
    for x, c in enumerate(line):
        if c == " ": continue
        dpad[x, y] = c
        dpad_buttons[c] = x, y

npad_buttons = {}
npad = {}
for y, line in enumerate(["789", "456", "123", " 0A"]):
    for x, c in enumerate(line):
        if c == " ": continue
        npad[x, y] = c
        npad_buttons[c] = x, y


from heapq import heappop, heappush

DIRECTIONS = Vec2(0, -1), Vec2(1, 0), Vec2(0, 1), Vec2(-1, 0)

def show_d(d):
    return "^>v<"[DIRECTIONS.index(d)]

def read_d(d):
    return DIRECTIONS["^>v<".index(d)]

from functools import cache
@cache
def can_activate(button, others, needed, last_npad):
    grid = npad if last_npad else dpad

    pos, nothers = others[0], others[1:]
    if not nothers:
        if button == "A":
            if grid[pos] == needed[0]:
                return True, (pos,), needed[1:]
            else:
                return False, (pos,), needed

        npos = pos + read_d(button)
        return (grid.get(npos, " ") != " "), (npos,), needed

    if button == "A":
        can, nothers, nneeded = can_activate(dpad[pos], nothers, needed, last_npad)
        return can, (pos, *nothers), nneeded

    npos = pos + read_d(button)
    return (dpad.get(npos, " ") != " "), (npos, *nothers), needed

# from collections import defaultdict
from itertools import repeat
def solve(code, nbots, last_npad):
    ipos = dpad_buttons["A"]

    if last_npad:
        iothers = *repeat(ipos, nbots-1), npad_buttons["A"]
    else:
        iothers = tuple(repeat(ipos, nbots))

    istate = ipos, iothers, code
    remaining = [(0, -1, DIRECTIONS[-1], ipos, iothers, code, "")]

    seen = {istate}
    while remaining:
        score, _, pd, pos, others, needed, history = heappop(remaining)

        if not needed:
            return history

        for d in DIRECTIONS:
            npos = pos + d
            if dpad.get(npos, " ") == " ":
                continue

            nstate = npos, others, needed
            if nstate in seen: continue
            seen.add(nstate)

            heappush(remaining, (score + 1, (show_d(pd) + "><^v").index(show_d(d)), d, npos, others, needed, history + show_d(d)))

        can, nothers, nneeded = can_activate(dpad[pos], others, needed, last_npad)
        if not can:
            continue

        if nneeded != needed:
            remaining = []
            seen = set()

        heappush(remaining, (score + 1, -1, DIRECTIONS[-1], pos, nothers, nneeded, history + "A"))

# grid.get(pos + d, " ") != " "
with open(0) as f:
    data = f.read()

p1 = 0
for icode in data.splitlines():
    p1 += len(solve(icode, 2, True)) * int(icode[:-1])


    # find upper bound?
    # code = solve(icode, 1, True)
    # code = solve(code, 1, False) # 3
    # print(3, len(code))
    # code = solve(code, 1, False) # 5
    # print(5, len(code))
    # code = solve(code, 1, False) # 7
    # print(7, len(code))
    # print(len(solve(icode, 7, True)))
    # code = solve(code, 1, False) # 9
    # print(9, len(code))
    # code = solve(code, 1, False) # 11
    # print(11, len(code))
    # code = solve(code, 1, False) # 13
    # print(13, len(code))
    # code = solve(code, 1, False) # 15
    # print(15, len(code))
    # code = solve(code, 1, False) # 17
    # print(17, len(code))
    # code = solve(code, 1, False) # 19
    # print(19, len(code))
    # code = solve(code, 1, False) # 21
    # print(21, len(code))
    # code = solve(code, 1, False) # 23
    # print(23, len(code))
    # code = solve(code, 1, False) # 25
    # print(25, len(code))
    # print(len(solve(icode, 3, True)))

print(p1)
