from itertools import groupby, product
from pathlib import Path
from re import findall

p1 = p2 = 0

INPUT_FILE = Path(__file__).parent / "input"
#INPUT_FILE = Path(__file__).parent / "test"

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

locks = []
keys = []
for section in sections:
  z = *map("".join, zip(*section)),
  if z[0][0] == '#':
    print("lock", z)
    locks.append(tuple(map(tuple, z)))
  else:
    keys.append(tuple(map(tuple, z)))
    print("key", z)

for lock in locks:
  for key in keys:
    for a, b in zip(lock, key):
      print(a.count("#"),  b.count("#"))
      if a.count("#") > b.count("."):
        break
    else: p1 += 1

  








for pos in product(range(w), range(h)):
    x, y = pos

for section in sections:
    section

for line in lines:
    line

print(p1)
print(p2)
