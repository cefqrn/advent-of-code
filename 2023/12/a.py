from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from functools import cache


@cache
def check(line: str, required: tuple[int, ...]):
    if not required:
        return '#' not in line

    s = 0
    current = required[0]
    for i in range(len(line) - sum(required) - len(required) + 2):
        if '#' in line[:i] or line[i+current:].startswith('#'):
            continue

        segment = line[i:i+current]
        if not all(c in "#?" for c in segment):
            continue

        s += check(line[i+current+1:], required[1:])

    return s


for repetitions in 1, 5:
    s = 0
    for line in lines:
        line, required = line.split()
        required = eval(required)

        line = "?".join((line,)*repetitions)
        required *= repetitions

        s += check(line, required)

    print(s)
