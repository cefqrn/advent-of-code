from itertools import groupby, product
from pathlib import Path
from re import findall

p1 = p2 = 0

INPUT_FILE = Path(__file__).parent / "input"
# INPUT_FILE = Path(__file__).parent / "test"

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


from collections import defaultdict
connections = defaultdict(set)



nodes = set()
for line in lines:
  a, b = line.split("-")
  connections[a].add(b)
  connections[b].add(a)
  nodes.add(a)
  nodes.add(b)

connections = {k: frozenset(v) for k, v in connections.items()}

"""
from itertools import combinations
groups = []
for a, b, c in combinations(seen,3):
  if a in connections[b] \
and a in connections[c] \
and b in connections[a] \
and b in connections[c] \
and c in connections[a] \
and b in connections[c]: groups.append((a,b,c))

groups = []
while seen:
  group = set()
  remaining = [seen.pop()]
  while remaining:
    curr = remaining.pop()
    group.add(curr)
    for b in connections[curr]:
      if b in group: continue
      remaining.append(b)
  seen -= group
  print(group)
  groups.append(group)

from math import comb
from itertools import combinations
for c in groups:
  # for c in combinations(group, 3):
    if "t" in "".join(c)[::2]:
      p1 += 1

#  p1 += comb(len(group), 3)
"""

remaining = [(frozenset({x}), connections[x]) for x in nodes]
seen = set()
best = None
while remaining:
  curr, left = remaining.pop() 
  if best is None or len(curr) > len(best):
    best = curr

  if len(curr) == 3:
    p1 += 't' in "".join(curr)[::2]

  for c in left:
    n = curr | {c}
    if n in seen: continue
    seen.add(n)
    remaining.append((
      n,
      left & connections[c]
    ))

print(p1)
print(",".join(sorted(best)))

