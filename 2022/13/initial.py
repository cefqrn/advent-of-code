import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *

def cmp(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left < right

    if isinstance(left, int):
        left = [left]

    if isinstance(right, int):
        right = [right] 

    left = left[:]
    right = right[:]

    while True:
        try:
            a = left.pop(0)
        except:
            return True
        try:
            b = right.pop(0)
        except:
            return False

        if a == b:
            continue

        return cmp(a, b)

lists = []
s = 0
j = 1
for a, b, _ in get_chunks(input_string + '\n\n', 3):
    a = eval(a)
    b = eval(b)

    for i, l in enumerate(lists):
        if cmp(a, l):
            lists.insert(i, a)
            break
    else:
        lists.append(a)

    for i, l in enumerate(lists):
        if cmp(b, l):
            lists.insert(i, b)
            break
    else:
        lists.append(b)

    if cmp(a, b):
        s+=j

    j+=1

print(s)

for i, l in enumerate(lists):
    if cmp([[2]], l):
        lists.insert(i, [[2]])
        break
else:
    lists.append([[2]])

for i, l in enumerate(lists):
    if cmp([[6]], l):
        lists.insert(i, [[6]])
        break
else:
    lists.append([[6]])

print((lists.index([[2]])+1) * (lists.index([[6]])+1))
