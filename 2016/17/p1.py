from functools import partial
from operator import lt
from hashlib import md5
from heapq import heappush, heappop

target = 3, 3
def h(x, y):
    return abs(x - target[0]) + abs(y - target[1])

directions = tuple(zip(
    (b"U", b"D", b"L", b"R"),
    ((0, -1), (0, 1), (-1, 0), (1, 0))
))

initial_passcode = b"rrrbmfta"
possibilities = [(0, 0, (0, 0), initial_passcode)]
while possibilities:
    _, cost, (x, y), passcode = heappop(possibilities)
    if (x, y) == target:
        print(passcode[len(initial_passcode):])
        break

    ncost = cost + 1
    for i, can_move in enumerate(map(partial(lt, "a"), md5(passcode).hexdigest()[:4])):
        if not can_move:
            continue

        dpassword, (dx, dy) = directions[i]
        npos = nx, ny = x + dx, y + dy
        if nx < 0 or nx > 3 or ny < 0 or ny > 3:
            continue

        heappush(possibilities, (
            ncost + h(nx, ny),
            ncost,
            npos,
            passcode + dpassword
        ))
    
    
