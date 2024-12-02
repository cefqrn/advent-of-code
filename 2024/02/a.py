from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

from itertools import pairwise

def is_safe(data):
    for a, b in pairwise(data):
        d = abs(a-b)
        if d < 1 or d > 3:
            return 0

    s = -1 if data[0] - data[1] < 0 else 1
    for a, b in pairwise(data[1:]):
        if s != (-1 if a - b < 0 else 1):
            return 0

    return 1

p1 = 0
p2 = 0
for line in lines:
    line = list(map(int, line.split()))
    if is_safe(line):
        p1 += 1
        p2 += 1
        continue

    for i in range(len(line)):
        new_line = line[:i] + line[i+1:]
        if is_safe(new_line):
            p2 += 1
            break

print(p1, p2)
