import numpy as np


def solve(inp: str) -> tuple[int, int]:
    lights1 = np.zeros((1000, 1000), np.uint8)
    # uint8 is faster but could overflow
    lights2 = np.zeros((1000, 1000), np.uint16)

    for command in inp.strip().split('\n'):
        *_, c, p1, _, p2 = command.split(' ')
        x1, y1 = p1.split(',')
        x2, y2 = p2.split(',')

        s = (slice(int(x1), int(x2)+1), slice(int(y1), int(y2)+1))

        if c == "on":
            lights1[s] = 1
            lights2[s] += 1
        elif c == "off":
            lights1[s] = 0

            # overflowed uint (inf) > 0 (done like this because uint seems slightly faster)
            l = lights2[s]
            l[:] = np.minimum(l - 1, l)
        else:  # toggle
            lights1[s] ^= 1
            lights2[s] += 2
    
    return int(np.sum(lights1)), int(np.sum(lights2))


from time import perf_counter
from sys import stdin, argv
from os import isatty

if len(argv) == 2:
    with open(argv[1]) as f:
        s = f.read()
elif not isatty(0):  # check if stdin is a file
    s = stdin.read()
else:
    print("input not given")
    exit(1)

st = perf_counter()
p1, p2 = solve(s)
print(f'p1: {p1}')
print(f'p2: {p2}')
print(f'done in {perf_counter() - st:.5f} s')