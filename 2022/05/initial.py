import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

b1, b2 = blocks
b2 = b2.strip()

from collections import deque

# at first I tried using lines then rotating everything with zip(*lines)
# but the input was automatically getting stripped by the library and I forgot about that
# so I gave up
# thinking about it now I could've selected the lines with multiple cursors
# then erased the newlines
stacks = {
    1: deque(["R", "W", "F", "H", "T", "S"]),
    2: deque(["W", "Q", "D", "G", "S"]),
    3: deque(["W", "T", "B"]),
    4: deque(["J", "Z", "Q", "N", "T", "W", "R", "D"]),
    5: deque(["Z", "T", "V", "L", "G", "H", "B", "F"]),
    6: deque(["G", "S", "B", "V", "C", "T", "P", "L"]),
    7: deque(["P", "G", "W", "T", "R", "B", "Z"]),
    8: deque(["R", "J", "C", "T", "M", "G", "N"]),
    9: deque(["W", "B", "G", "L"]),
}

for l in b2.split('\n'):
    _, a, _, b, _, c = l.split()
    a,b,c = map(int, [a, b, c])

    for i in range(a):
        stacks[c].appendleft(stacks[b].popleft())

for s in stacks.values():
    print(s.popleft(), end='')

print()


from collections import deque

stacks = {
    1: deque(["R", "W", "F", "H", "T", "S"]),
    2: deque(["W", "Q", "D", "G", "S"]),
    3: deque(["W", "T", "B"]),
    4: deque(["J", "Z", "Q", "N", "T", "W", "R", "D"]),
    5: deque(["Z", "T", "V", "L", "G", "H", "B", "F"]),
    6: deque(["G", "S", "B", "V", "C", "T", "P", "L"]),
    7: deque(["P", "G", "W", "T", "R", "B", "Z"]),
    8: deque(["R", "J", "C", "T", "M", "G", "N"]),
    9: deque(["W", "B", "G", "L"]),
}

for l in b2.split('\n'):
    _, a, _, b, _, c = l.split()
    a,b,c = map(int, [a, b, c])

    for x in reversed(list(stacks[b])[:a:]):
        stacks[c].appendleft(x)
        stacks[b].popleft()


for s in stacks.values():
    print(s.popleft(), end='')

print()