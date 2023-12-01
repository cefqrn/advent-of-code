from pathlib import Path

with open(Path(__file__).parent / "input") as f:
    data = f.read().rstrip()

blocks = data.split("\n\n")
ints = list(map(int, data.split()))
