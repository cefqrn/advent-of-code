with open("day03/input") as f:
    inp = f.read()

houses: set[tuple[int, int]] = {(0, 0)}
coords = [0, 0]
coords2 = [0, 0]

a = 0
for instruction in inp:
    if a:
        c = coords
    else:
        c = coords2

    if instruction == ">":
        c[0] += 1
    if instruction == "<":
        c[0] -= 1
    if instruction == "^":
        c[1] += 1
    if instruction == "v":
        c[1] -= 1

    a = not a
    houses.add(tuple(c))

print(len(houses))