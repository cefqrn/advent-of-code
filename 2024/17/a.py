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

DIRECTIONS = (0, -1), (1, 0), (0, 1), (-1, 0)
UP, RIGHT, DOWN, LEFT = NORTH, EAST, SOUTH, WEST = DIRECTIONS

def    left(d): return DIRECTIONS[DIRECTIONS.index(d)-1]
def inverse(d): return DIRECTIONS[DIRECTIONS.index(d)-2]
def   right(d): return DIRECTIONS[DIRECTIONS.index(d)-3]
def  others(d): return left(d), inverse(d), right(d)
def   sides(d): return left(d), right(d)

grid = {}
ipos = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        grid[x, y] = c
        if c == '':
            ipos = x, y

w, h = len(line), len(lines)

from re import findall

a, b = sections

def batched(it, n):
    return list(zip(*n*[iter(it)]))

from functools import cache

@cache
def get_val(n):
    possible = []
    for a in range(1<<10):
        if (1 ^ (a%8) ^ (a >> ((a%8) ^ 2))) % 8 == n:
            possible += a,

    return possible

def run(program, a, b=0, c=0):
    output = []
    while a:
        output += (1 ^ (a%8) ^ (a >> ((a%8) ^ 2))) % 8,
        a >>= 3

    return tuple(output)

program = tuple(map(int, b[0].split(": ")[1].split(",")))

print(','.join(map(str, run(program, *map(int, findall(r"\d+", "".join(a)))))))

possible = set(get_val(program[-1]))
best = None
for i, needed in enumerate(program[:-1][::-1], 1):
    new_possible = set()
    for a in possible:
        if run(program, a)[-i:] == program[-i:]:
            new_possible.add(a)

    for a, b in product(possible, get_val(needed)):
        b_len = b.bit_length()
        new = (a << 3) | b
        if run(program, new)[-i:] == program[-i:]:
            new_possible.add(new)

    possible = new_possible
    for a in possible:
        output = run(program, a, 0, 0)

        if output != program:
            continue

        if best is None or best > a:
            best = a

print(best)
