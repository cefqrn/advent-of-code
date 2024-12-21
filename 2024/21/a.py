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

dpad_grid = {}
dpad_buttons = {}
dpad = [" ^A", "<v>"]
for y, line in enumerate(dpad):
    for x, c in enumerate(line):
        if c == " ": continue
        dpad_grid[x, y] = c
        dpad_buttons[c] = x, y

npad_grid = {}
npad_buttons = {}
npad = ["789", "456", "123", " 0A"]
for y, line in enumerate(npad):
    for x, c in enumerate(line):
        if c == " ": continue
        npad_grid[x, y] = c
        npad_buttons[c] = x, y


def show_dir(d):
    return "^>v<"[DIRECTIONS.index(d)]

def read_dir(d):
    return DIRECTIONS["^>v<".index(d)]


from functools import cache
from heapq import heappush, heappop

# @cache
def get_cost(grid, buttons, ibut, ebut):
    ipos = buttons[ibut]

    remaining = [(0, ipos, "")]
    seen = {ipos: None}

    epos = buttons[ebut]

    histories = []
    best = None
    while remaining:
        score, pos, history = heappop(remaining)
        x, y = pos

        if best and score > best:
            break

        if pos == epos:
            best = score
            histories.append(history + "A")

            continue

        score += 1
        for d in DIRECTIONS:
            dx, dy = d
            npos = nx, ny = x+dx, y+dy

            if npos not in grid:
                continue

            # if npos in seen:
            #     continue
            # seen[npos] = pos

            heappush(remaining, (score, npos, history + show_dir(d)))

    return histories


# def get_code_cost(grid, buttons, code, prev="A"):
#     history = ""
#     for target in code:
#         history += get_cost(grid, buttons, prev, target)
#         prev = target

#     return history

from itertools import chain

def get_code_cost(grid, buttons, code, prev="A"):
    if code == "":
        yield ""
        return

    # return set(chain.from_iterable(
    yield from set(chain.from_iterable(
        map(x.__add__, get_code_cost(grid, buttons, code[1:], code[0]))
        for x in get_cost(grid, buttons, prev, code[0])
    ))
    # for x in get_cost(grid, buttons, prev, code[0]):
    #     yield from set(map(x.__add__, get_code_cost(grid, buttons, code[1:], code[0])))

def solve(possible, nbots):
    if nbots == 0:
        yield from set(possible)
        return

    yield from set(chain.from_iterable(
        solve(get_code_cost(dpad_grid, dpad_buttons, code), nbots-1)
        for code in possible
    ))
    # for code in possible:
    #     yield from set(solve(get_code_cost(dpad_grid, dpad_buttons, code), nbots-1))

        # for x in :
            # yield code + x
    # for code in possible:
        # yield from get_code_cost(dpad_grid, dpad_buttons, code)


for icode in lines[3:]:
    # print(solve(get_code_cost(npad_grid, npad_buttons, icode), 2))
    print(icode)
    code = get_code_cost(npad_grid, npad_buttons, icode)
    # print(code)
    # print(solve(code, 1))
    possible = solve(code, 2)
    # print(*code, sep='\n')
    # code = get_code_cost(dpad_grid, dpad_buttons, code)
    # print(code)
    # code = get_code_cost(dpad_grid, dpad_buttons, code)
    # print(code)
    # print(icode)
    # _, code, _ = get_code_cost(npad_grid, npad_buttons, icode)
    # print(code)
    # _, code, _ = get_code_cost(dpad_grid, dpad_buttons, code)
    # print(code)
    # _, code, _ = get_code_cost(dpad_grid, dpad_buttons, code)
    # print(code)

    code = min(possible, key=len)
    # for code in possible:
    print(code)
    print(len(code), int(icode[:-1]))
    p1 += len(code) * int(icode[:-1])

    print()

    # break

print(p1)
# print(p2)
