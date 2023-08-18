from collections import deque
from functools import partial
from itertools import compress
from operator import lt
from hashlib import md5

target = 3, 3
initial_passcode = b"rrrbmfta"

p1 = p2 = None

directions = (
    (b"U", ( 0, -1)),
    (b"D", ( 0,  1)),
    (b"L", (-1,  0)),
    (b"R", ( 1,  0)),
)

possibilities = deque([((0, 0), initial_passcode)])
while possibilities:
    (x, y), passcode = possibilities.popleft()
    if (x, y) == target:
        p2 = len(passcode) - len(initial_passcode)
        if p1 is None:
            p1 = passcode[len(initial_passcode):].decode()

        continue

    for direction, (dx, dy) in compress(directions, map(partial(lt, "a"), md5(passcode).hexdigest())):
        npos = nx, ny = x + dx, y + dy
        if not 0 <= nx < 4 or not 0 <= ny < 4:
            continue

        possibilities.append((npos, passcode + direction))

print(p1, p2)
