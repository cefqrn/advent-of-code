from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from itertools import islice


def iterate(f, x):
    while True:
        yield x
        x = f(x)


_NO_ARGUMENT = object()
def nth(iterable, i, default=_NO_ARGUMENT):
    s = islice(iterable, i, None)
    if default is _NO_ARGUMENT:
        return next(s)
    else:
        return next(s, default)


def transposed(platform):
    return tuple(zip(*platform))


def rotated(platform):
    # clockwise
    return transposed(reversed(platform))


def tilted(platform):
    new_lines = []
    for col in transposed(platform):
        col_l = len(col)
        new_col = ['.']*col_l
        new_lines.append(new_col)
        i = 0
        for y, c in enumerate(col):
            match c:
                case '#':
                    new_col[y] = c
                    i = y
                case 'O':
                    new_col[i] = c
                case '.':
                    continue

            i += 1

    return transposed(new_lines)


def calculate_load(lines):
    return sum(
        y * row.count('O')
        for y, row in enumerate(reversed(lines), 1)
    )


def cycle_lines(platform):
    return nth(iterate(lambda p: rotated(tilted(p)), platform), 4)


platform = tuple(map(tuple, lines))

print(calculate_load(tilted(lines)))

values = []
for i, x in enumerate(iterate(cycle_lines, lines)):
    with suppress(ValueError):
        cycle_start = values.index(x)
        cycle_length = i - cycle_start
        cycle_initial = x
        break

    values.append(x)

n = 1000000000

print(calculate_load(nth(iterate(cycle_lines, cycle_initial), (n - cycle_start) % cycle_length)))
