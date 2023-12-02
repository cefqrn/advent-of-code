from contextlib import suppress
from itertools import groupby
from pathlib import Path

with open(Path(__file__).parent / "input") as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]
