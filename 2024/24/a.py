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

a, b = sections


initial = {}
for line in a:
  x, i = line.split(": ")
  initial[x] = int(i)


from operator import *
AND = and_
OR = or_
XOR = xor

combs = {}
for line in b:
  *f, d = findall("\w+", line)
  combs[d] = tuple(f)

def get(v):
  if v in initial:
    return initial[v]

  a, b, c = combs[v]
  return eval(f"{b}(get('{a}'),get('{c}'))")  

names = [*combs, *initial]
def to_int(c):
  zs = sorted(x for x in names if x[0] == c)[::-1]
  return int("".join(map(str, map(get, zs))), 2)


flips = 4

x = (to_int('x'))
y = (to_int('y'))

"""
from math import comb
from itertools import combinations
print(comb(len(names), 2))
non_out = [n for n in combs if n[0] != 'z']
left = []
allowed = frozenset(combinations(non_out, 2))
"""

def do(pairs):
  for a, b in pairs:
    combs[a], combs[b] = combs[b], combs[a]

def undo(pairs):
  for a, b in pairs[::-1]:
    combs[a], combs[b] = combs[b], combs[a]

def get_wrong():
  wrong = (x+y) ^ to_int('z')
  return [f'z{i:02}' for i, v in enumerate(bin(wrong)[::-1]) if v == '1']


from itertools import combinations, chain
from math import comb

def get_allowed():
  to_check = set(get_wrong())
  remaining = list(to_check)
  while remaining:
    curr = remaining.pop()
    a, _, b = combs[curr]
    if a not in to_check and a not in initial:
      to_check.add(a)
      remaining.append(a)
    if b not in to_check and b not in initial:
      to_check.add(b)
      remaining.append(b)

  allowed = [v for v in to_check if v[0] != 'z']

  pairs = set(map(frozenset, combinations(allowed, 2)))
  return pairs


def has_cycle():
  remaining = [(v, {v}) for v in combs]
  while remaining:
    curr, seen = remaining.pop()
    if curr in seen:
      return True
    remaining

remaining = [(flips, (), get_allowed())]
left = []
while remaining:
  l, c, pairs = remaining.pop()

  try:
    do(c)

    npairs = pairs & get_allowed()
    if l == 2*abs(((x+y) ^ to_int('z')).bit_count()):
      print(c)
      print(sorted([*c, *get_wrong()]), sep=',')
      left.append(c)
  except RecursionError:
    continue
  finally:
    undo(c)

  if l == 0:
    continue

  print(len(pairs), len(npairs))
  for p in npairs:
    if set(p) & set(chain.from_iterable(c)):
      continue
    remaining.append((
      l-1,
      (*c, p),
      npairs
    ))

print(len(left))
print(left)
