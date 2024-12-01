from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

a, b = zip(*map(str.split, lines))

a = sorted(map(int, a))
b = sorted(map(int, b))

s = 0
for x, y in zip(a, b):
	s += abs(x-y)

print(s)

s = 0
for x in a:
	s += b.count(x) * x

print(s)
