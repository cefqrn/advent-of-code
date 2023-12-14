from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]


def rotate(lines):
    # clockwise
    return tuple(x[::-1] for x in zip(*lines))


def fall(lines):
    new_lines = []
    for x, col in enumerate(zip(*lines)):
        col_l = len(col)
        new_col = ['.']*col_l
        new_lines.append(new_col)
        i = 0
        for y, c in enumerate(col, 1):
            if c == '#':
                new_col[y-1] = c
                i = y
            if c == 'O':
                new_col[i] = c
                i += 1

    return tuple(zip(*new_lines))


def print_lines(lines):
    print('\n'.join(map("".join,lines)))


def cycle_lines(lines):
    for _ in range(4):
        lines = rotate(fall(lines))

    return lines


def calculate_load(lines):
    return sum(
        y * row.count('O')
        for y, row in enumerate(reversed(lines), 1)
    )


print(calculate_load(fall(lines)))

from itertools import count

# enter the cycle
tortoise = hare = lines
for i in count(1):
    tortoise = cycle_lines(tortoise)
    hare = cycle_lines(cycle_lines(hare))

    if tortoise == hare:
        break

initial = i

# find the length of the smallest cycle
for i in count(1):
    tortoise = cycle_lines(tortoise)

    if tortoise == hare:
        break

cycle_length = i
initial += cycle_length

n = 1000000000

for _ in range((n - initial) % cycle_length):
    tortoise = cycle_lines(tortoise)

print(calculate_load(tortoise))
