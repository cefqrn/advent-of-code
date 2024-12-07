from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

p1 = p2 = 0

results = []
nums = []
for line in lines:
    a, b = line.split(": ")
    results.append(int(a))
    nums.append(eval(b.replace(*" ,")))

from functools import partial
from operator import add, mul

def concat(a, b):
    return int(str(a) + str(b))

def solve(funcs, result, ns):
    left = [ns]
    while left:
        ns = left.pop()
        try:
            a, b = ns[:2]
        except ValueError:
            continue

        for f in funcs:
            if (v := f(a, b)) == result and len(ns) == 2:
                return result

            left.append([v, *ns[2:]])

    return 0

print(sum(map(partial(solve, (add, mul)), results, nums)))
print(sum(map(partial(solve, (add, mul, concat)), results, nums)))
