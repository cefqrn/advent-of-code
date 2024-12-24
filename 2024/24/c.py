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


def solve(combs, swaps):
  def get(v):
    if v in initial:
      return initial[v]

    a, b, c = combs[v]
    return eval(f"{b}(get('{a}'),get('{c}'))")  

  names = [*combs, *initial]
  def to_int(c):
    zs = sorted(x for x in names if x[0] == c)[::-1]
    return int("".join(map(str, map(get, zs))), 2)


  x = (to_int('x'))
  y = (to_int('y'))

  def do(pairs):
    for a, b in pairs:
      combs[a], combs[b] = combs[b], combs[a]

  def undo(pairs):
    for a, b in pairs[::-1]:
      combs[a], combs[b] = combs[b], combs[a]

  def get_wrong():
    wrong = (x+y) ^ to_int('z')
    return [f'z{i:02}' for i, v in enumerate(bin(wrong)[::-1]) if v == '1']

  def get_inputs(n):
    inputs = set()
    remaining = [n]
    while remaining:
      curr = remaining.pop()
      inputs.add(curr)
      a, _, b = combs[curr]
      if a not in inputs and a not in initial:
        remaining.append(a)
      if b not in inputs and b not in initial:
        remaining.append(b)
    return inputs

  def getn(v):
    if v in initial:
      return v

    a, b, c = combs[v]
    return f"{v}({getn(a)}){b}({getn(c)})"  
  """
  for n in range(10):
    print(n, "AND", getn(f"z{n:02}").count("AND"))
    print(n, "OR ", getn(f"z{n:02}").count("OR"))
    print(n, "XOR", getn(f"z{n:02}").count("XOR"))
  """

  # swap 1
  """
  for n in combs:
    v = getn(n)
    if v.count("AND") != 2*11-1:
      continue
    if v.count("XOR") != 11+1:
      continue

    print(v)
    print()
  """

  def check(n):
    if n < 2: return True

    v = getn(f"z{n:02}")
    if v.count("AND") != 2*n-1:
      return False
    if v.count("XOR") != n+1:
      return False
    if v.count("OR") != 2*n:
      return False
    if (get(f"z{n:02}") ^ ((x+y) >> n)) & 1:
      return False

    return True

  print(bin(x+y)[::-1])
  print(bin(to_int('z'))[::-1])

  #do([("vkq", "z11")])
  swaps = 4#-1

  from itertools import count, combinations
  correct = set()

  while swaps:
    for i in count():
      if not check(i):
        break

      correct.update(get_inputs(f"z{i:02}"))

    inputs = get_inputs(f"z{i:02}") - correct
    possible = set(combs) - correct

    print(i)

    from itertools import chain
    from heapq import heappush, heappop
    remaining = [(0, (), inputs)]
    while remaining:
      swapped, curr, left = heappop(remaining)
      print(curr, swapped, end='\r')

      do(curr)
      try:
        if check(i):
          swaps -= swapped
          correct -= inputs
          print(curr)
          break
      except RecursionError:
        undo(curr)
        continue

      undo(curr)
      if swapped == swaps:
        continue

      seen = set(chain.from_iterable(curr))
      for a in left:
        for b in possible:
          if a == b: continue
          if b in seen: continue
          p = a, b
        
          heappush(remaining, (
            swapped + 1,
            (*curr, p),
            left.difference(p)
          ))
    else:
      raise ValueError

    print(to_int('z'))
    print(x+y)


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



