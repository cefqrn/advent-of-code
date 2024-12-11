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
def solve(n, count):
    if count == 0:
        return 1

    return sum(solve(x, count-1) for x in process(n))

print(sum(solve(n, 25) for n in data))
print(sum(solve(n, 75) for n in data))
