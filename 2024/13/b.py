from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
sections = contents.split("\n\n")

from fractions import Fraction
from re import findall

def solve(prize, a, b):
    ax, ay = a
    bx, by = b
    px, py = prize

    b_count = Fraction(py*ax - px*ay, by*ax - bx*ay)
    a_count = Fraction(px - b_count*bx, ax)

    if a_count.denominator == b_count.denominator == 1:
        return 3*a_count + b_count

    return 0

p1 = p2 = 0
for section in sections:
    a, b, prize = section.split('\n')

    a = *map(int, findall(r"X\+(\d+), Y\+(\d+)", a)[0]),
    b = *map(int, findall(r"X\+(\d+), Y\+(\d+)", b)[0]),
    prize = px, py = *map(int, findall(r"X=(\d+), Y=(\d+)", prize)[0]),

    p1 += solve(prize, a, b)
    p2 += solve((px + 10000000000000, py + 10000000000000), a, b)

print(p1)
print(p2)
