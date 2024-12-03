from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

p1 = p2 = 0

from re import findall

enabled = True
for *x, c, d in findall("mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", contents):
    if c:
        enabled = True
        continue

    if d:
        enabled = False
        continue

    a, b = map(int, x)

    p1 += a*b
    if enabled:
        p2 += a*b

print(p1)
print(p2)
