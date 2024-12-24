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


from operator import *
from itertools import chain, count
def solve(combs, swaps):
  def get(v):
    if v in initial:
      return initial[v]

    AND = and_
    OR = or_
    XOR = xor

    a, b, c = combs[v]
    return eval(b)(get(a),get(c))  

  names = [*combs, *initial]
  def to_int(c):
    zs = sorted(x for x in names if x[0] == c)[::-1]
    return int("".join(map(str, map(get, zs))), 2)

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


  x = to_int('x')
  y = to_int('y')

  if not swaps:
    if to_int('z') == x+y:
      return ()
    else:
      return None

  correct = set()
  for i in count():
    if not check(i):
      break

    correct.update(get_inputs(f"z{i:02}"))

  inputs = get_inputs(f"z{i:02}") - correct
  possible = set(combs) - correct

  for a in inputs:
    for b in possible:
      if a == b: continue
      p = a, b
    
      do([p])
      try:
        if check(i):
          s = solve(combs.copy(), swaps-1)
          if s is not None:
            return p, *s
      except RecursionError: pass
      finally: undo([p])

  return None

def get(v):
  if v in initial:
    return initial[v]

  AND = and_
  OR = or_
  XOR = xor

  a, b, c = combs[v]
  return eval(b)(get(a),get(c))  

def to_int(c):
  zs = sorted(x for x in names if x[0] == c)[::-1]
  return int("".join(map(str, map(get, zs))), 2)

a, b = sections

initial = {}
for line in a:
  x, i = line.split(": ")
  initial[x] = int(i)

combs = {}
for line in b:
  *f, d = findall("\w+", line)
  combs[d] = tuple(f)

names = list(chain(combs, initial))
print(to_int('z'))
print(",".join(sorted(chain.from_iterable(solve(combs, 4)))))

