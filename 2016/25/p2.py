from itertools import islice
from math import prod, ceil, log
from re import finditer

with open(0) as f:
    x = prod(int(m.group()) for m in islice(finditer(r"-?\d+", f.read()), 2))

print(2 * (4**ceil(log(x*3/2 + 1, 4)) - 1) // 3 - x)

# y = 0
# while y < x:
#     y = 4*y + 2

# print(y - x)
