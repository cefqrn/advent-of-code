"""
initially solved 2023-12
data now reads from an input file
"""

data = """
[...]
"""
from pathlib import Path
data = (Path(__file__).parent / "input").read_text()

lines = data.strip().splitlines()

from collections import defaultdict
from functools import partial
from itertools import combinations, pairwise, count
from heapq import heappush, heappop
from re import findall

nodes = set(findall(r"\w+", data))
edges = defaultdict(list)
for line in lines:
  component, *connected = findall(r"\w+", line)
  edges[component].extend(connected)
  for c in connected:
    edges[c].append(component)

start = next(iter(nodes))
connections = defaultdict(int)
def shortest_path(start, end, banned=[]):
  remaining = [(0, start, [start])]
  seen = set()
  while remaining:
    step, node, path = heappop(remaining)
    if node == end:
      return path
    for adjacent in edges[node]:
      if frozenset((node, adjacent)) in banned: continue
      if adjacent in seen: continue
      seen.add(adjacent)
      heappush(remaining, (step+1, adjacent, path + [adjacent]))

def find_paths(a, b, banned=set()):
  banned = banned.copy()
  paths = []
  while True:
    path = shortest_path(a, b, banned)
    if path is None:
      return paths
    paths.append(path)
    banned.update(map(frozenset, pairwise(path)))

for a, b in combinations(nodes, 2):
  paths = find_paths(a, b)
  if len(paths) == 3:
    break

bans = set()
for i, path in enumerate(paths):
  for ban in map(frozenset, pairwise(path)):
    if len(find_paths(a, b, bans | {ban})) == 3 - 1 - i:
      break
  bans.add(ban)

seen = set()
remaining = [a]
while remaining:
  node = remaining.pop()
  for adjacent in edges[node]:
    if adjacent in seen: continue
    if frozenset((node, adjacent)) in bans: continue
    seen.add(adjacent)
    remaining.append(adjacent)

print(len(seen) * (len(nodes) - len(seen)))
