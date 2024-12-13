from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

grid = {}
ipos = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        grid[x, y] = c
        if c == '':
            ipos = x, y

w, h = len(line), len(lines)

p1 = p2 = 0

from functools import cache
from re import findall

inf = float("inf")

@cache
def find(prize, a, b):
    if prize == (0, 0):
        return 0

    if prize[0] < 0 or prize[1] < 0:
        return inf

    px, py = prize
    ax, ay = a
    bx, by = b

    return min(
        3 + find((px-ax, py-ay), a, b),
        1 + find((px-bx, py-by), a, b),
    )

from fractions import Fraction
from math import gcd

for section in sections:
    a, b, prize = section.split('\n')

    a = ax, ay = *map(int, findall(r"X\+(\d+), Y\+(\d+)", a)[0]),
    b = bx, by = *map(int, findall(r"X\+(\d+), Y\+(\d+)", b)[0]),
    prize = px, py = *map(int, findall(r"X=(\d+), Y=(\d+)", prize)[0]),

    if (z := find(prize, a, b)) != inf:
        p1 += z

    px, py = 10000000000000 + px, 10000000000000 + py

    if px % gcd(ax, bx) != 0 or py % gcd(ay, by) != 0:
        continue

    for z in range(3):
        b = Fraction(py - Fraction(px*ay - z*bx*ay, ax) - z*by, 3*by - Fraction(3*bx*ay, ax))
        a = Fraction(px - 3*b*bx - z*bx, ax)

        if b.denominator != 1:
            continue

        if a.denominator != 1:
            continue

        p2 += a*3 + b*3 + z

print(p1)
print(p2)
