from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")

from operator import sub, mul

a, b = zip(*map(str.split, lines))

a = sorted(map(int, a))
b = sorted(map(int, b))

print(sum(map(abs, map(sub, a, b))))
print(sum(map(mul, a, map(b.count, a))))
