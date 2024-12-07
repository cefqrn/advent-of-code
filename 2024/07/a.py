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
from itertools import product
from operator import add, mul

def concat(a, b):
    return int(str(a) + str(b))

def solve(funcs, result, ns):
    a, b, *rest = ns
    for fs in product(funcs, repeat=len(ns)-1):
        x = fs[0](a, b)
        for i, n in enumerate(rest, 1):
            x = fs[i](x, n)

        if x == result:
            return result

    return 0

print(sum(map(partial(solve, (add, mul)), results, nums)))
print(sum(map(partial(solve, (add, mul, concat)), results, nums)))
