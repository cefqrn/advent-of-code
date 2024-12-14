from itertools import groupby, product
from pathlib import Path

p1 = p2 = 0

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.splitlines()
sections = [
    list(section)
    for has_content, section in groupby(lines, bool)
    if has_content
]

grid = {}
ipos = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        grid[x, y] = c
        if c == '':
            ipos = x, y

w, h = len(line), len(lines)










for pos in product(range(w), range(h)):
    x, y = pos

for section in sections:
    section

for line in lines:
    line

print(p1)
print(p2)
