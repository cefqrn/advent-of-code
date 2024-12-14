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

grid = {}
ipos = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        grid[x, y] = c
        if c == '':
            ipos = x, y

w, h = 101, 103

def get_score(robots):
    a=b=c=d=0
    for x, y in robots:
        if x < w//2:
            if y < h//2:
                a += 1
            elif y > h//2:
                b += 1
        elif x > w//2:
            if y < h//2:
                c += 1
            elif y > h//2:
                d += 1

    return a*b*c*d



def display(robots):
    grid = [[" " for _ in range(w)] for _ in range(h)]
    for x, y in robots:
        grid[y][x] = "x"

    print("\n".join(map(" ".join, grid)))

def to_grid(robots):
    grid = [[" " for _ in range(w)] for _ in range(h)]
    for x, y in robots:
        grid[y][x] = "x"

    return list(map("".join, grid))

def iter_len(it):
    return sum(1 for _ in it)

from re import findall

def solve_p1():
    robots = []
    for line in lines:
        px, py, vx, vy = (map(int, findall(r"-?\d+", line)))
        pos = (px+vx*100)%w, (py+vy*100)%h
        robots += pos,

    return get_score(robots)

from itertools import count
seen = set()
for i in count():
    robots = []
    for line in lines:
        px, py, vx, vy = (map(int, findall(r"-?\d+", line)))

        pos = (px+vx*i)%w, (py+vy*i)%h
        robots += pos,

    grid = to_grid(robots)
    for l in grid:
        for v, g in groupby(l):
            if v == "x" and iter_len(g) > 10:
                display(robots)
                a = input()
                if a in "yY":
                    print(solve_p1())
                    print(i)
                    exit()
