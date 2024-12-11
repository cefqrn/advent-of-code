from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

p1 = p2 = 0
data = tuple(map(int, contents.split()))

from functools import cache

def process(n):
    if not n:
        return 1,

    if not (len(str(n)) & 1):
        l = len(str(n))
        return int('0' + str(n)[:l//2]), int('0' + str(n)[l//2:])

    return n*2024,

@cache
def solve(l, count):
    if count == 0:
        return len(l)

    s = 0
    for n in l:
        s += solve(process(n), count-1)

    return s

print(solve(data, 25))
print(solve(data, 75))
