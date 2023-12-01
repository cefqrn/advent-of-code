from contextlib import suppress
from pathlib import Path

with open(Path(__file__).parent / "input") as f:
    data = f.read().rstrip()

blocks = data.split("\n\n")
lines = data.split()
with suppress(ValueError):
    ints = list(map(int, lines))

from itertools import groupby

s = 0
for line in lines:
    a = ''.join(filter(str.isdigit, line))
    s += int(a[0] + a[-1])

print(s)


numbers = "zero, one, two, three, four, five, six, seven, eight, nine".split(", ")
numbers_last = "zero, one, two, three, four, five, six, seven, eight, nine"[::-1].split(" ,")[::-1]

from re import findall
pattern = '|'.join(numbers)
pattern_last = '|'.join(numbers_last)

s = 0
for line in lines:
    values = []
    for is_digit, g in groupby(line, str.isdigit):
        x = ''.join(g)
        if is_digit:
            values += map(int, x)
        else:
            values += map(numbers.index, findall(pattern, x))

    values_last = []
    for is_digit, g in groupby(line[::-1], str.isdigit):
        x = ''.join(g)
        if is_digit:
            values_last += map(int, x)
        else:
            values_last += map(numbers_last.index, findall(pattern_last, x))

    s += int(str(values[0]) + str(values_last[0]))

print(s)
