from itertools import groupby, product
from pathlib import Path
from re import findall

p1 = p2 = 0

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
ints = list(map(int, findall(r"[-+]?\d+", contents)))
lines = contents.splitlines()
sections = [
    list(section)
    for has_content, section in groupby(lines, bool)
    if has_content
]

def batched(it, n):
    return list(zip(*n*[iter(it)]))

DIRECTIONS = (0, -1), (1, 0), (0, 1), (-1, 0)
UP, RIGHT, DOWN, LEFT = NORTH, EAST, SOUTH, WEST = DIRECTIONS

def    left(d): return DIRECTIONS[DIRECTIONS.index(d)-1]
def inverse(d): return DIRECTIONS[DIRECTIONS.index(d)-2]
def   right(d): return DIRECTIONS[DIRECTIONS.index(d)-3]
def  others(d): return left(d), inverse(d), right(d)
def   sides(d): return left(d), right(d)

grid = {}
ipos = None
epos = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        grid[x, y] = c
        if c == '':
            ipos = x, y
        if c == '':
            epos = x, y

w, h = len(line), len(lines)

def get_next(n):
    n ^= n * 64
    n %= 16777216

    n ^= n // 32
    n %= 16777216

    n ^= n * 2048
    n %= 16777216

    return n

def iterate(f, n):
    yield n
    while True:
        n = f(n)
        yield n

from itertools import pairwise, starmap, islice
from operator import sub
def diffs(it):
    yield from starmap(sub, map(reversed, pairwise(it)))

def ones(n):
    return n % 10

prices = []
sequences = []
for n in ints:
    secret = tuple(islice(iterate(get_next, n), 2000+1))
    price = tuple(map(ones, secret))
    sequence = tuple(diffs(price))

    prices.append(price)
    sequences.append(sequence)

    p1 += secret[-1]

from string import ascii_lowercase

def try_seq(seq):
    seq = "".join(map(ascii_lowercase.__getitem__, seq))
    s = 0
    for initial, price, sequence in zip(ints, prices, sequences):
        sequence = "".join(map(ascii_lowercase.__getitem__, sequence))
        j = sequence.find(seq)

        if j < 0:
            continue

        s += price[j+4]

    return s

from collections import Counter
from itertools import tee

def nwise(it, n):
    yield from zip(*(islice(x, i, None) for i, x in enumerate(tee(it, n))))

found = Counter()
for price, sequence in zip(prices, sequences):
    seen = set()
    for p, seq in zip(price[4:], nwise(sequence, 4)):
        if seq in seen: continue
        seen.add(seq)

        found[seq] += p

print(p1)
print(max(found.values()))
