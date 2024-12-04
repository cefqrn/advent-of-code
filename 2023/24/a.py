"""
initially solved 2023-12
data now reads from an input file
"""

data = """
[...]
"""
from pathlib import Path
data = (Path(__file__).parent / "input").read_text()

lo = 200000000000000
hi = 400000000000000

lines = data.strip().splitlines()
from re import findall

stones = []
for line in lines:
  stones.append(tuple(map(int, findall(r"-?\d+", line))))

from itertools import combinations
from fractions import Fraction

icount = 0
for a, b in combinations(stones, 2):
  ax, ay, az, avx, avy, avz = a
  bx, by, bz, bvx, bvy, bvz = b

  x = bx - ax
  y = by - ay

  d = avx * -bvy + bvx * avy
  if not d: continue

  t = Fraction(-bvy*x + bvx*y, d)
  s = Fraction(-avy*x + avx*y, d)
  if min(t, s) < 0:continue

  x, y = ax + t*avx, ay + t*avy
  if lo <= x <= hi and lo <= y <= hi:
    icount += 1

print(icount)