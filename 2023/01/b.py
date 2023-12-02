from pathlib import Path

with open(Path(__file__).parent / "input") as f:
    data = f.read().rstrip()

from re import finditer, Match, compile

numbers = "zero, one, two, three, four, five, six, seven, eight, nine".split(", ")

# py3.12 woo
pattern = compile(fr"(?=(\d|{"|".join(numbers)}))")

p1 = p2 = 0
for line in data.splitlines():
    values_1 = []
    values_2 = []

    for m, in map(Match.groups, finditer(pattern, line)):
        try:
            v = int(m)
        except ValueError:
            # values_2[1:] = numbers.index(m),
            values_2.append(numbers.index(m))
        else:
            # values_1[1:] = values_2[1:] = v,
            values_1.append(v)
            values_2.append(v)

    p1 += 10*values_1[0] + values_1[-1]
    p2 += 10*values_2[0] + values_2[-1]

print(p1, p2)
