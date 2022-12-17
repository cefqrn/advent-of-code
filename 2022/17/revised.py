from itertools import cycle


rocks: list[tuple[tuple[int, int], ...]] = [
    ((2, 0), (3, 0), (4, 0), (5, 0)),
    ((2, 1), (3, 0), (3, 1), (3, 2), (4, 1)),
    ((2, 0), (3, 0), (4, 0), (4, 1), (4, 2)),
    ((2, 0), (2, 1), (2, 2), (2, 3)),
    ((2, 0), (2, 1), (3, 0), (3, 1))
]


g = [["."] * 7 for _ in range(50000)]
def move_rock(rock, direction):
    if direction == 'v':
        for x, y in rock:
            if y-1 < 0:
                raise ValueError
            if g[y-1][x] != ".":
                raise ValueError
        
        return tuple((x, y-1) for x, y in rock)
    elif direction == '>':
        for x, y in rock:
            if g[y][x+1] != ".":
                raise IndexError

        return tuple((x+1, y) for x, y in rock) 
    elif direction == '<':
        for x, y in rock:
            if x-1 < 0:
                raise IndexError
            if g[y][x-1] != ".":
                raise IndexError
            
        return tuple((x-1, y) for x, y in rock)
    else:
        raise KeyError


inp = cycle(open(0).read().rstrip())

max_height = 0

height_diffs = []
for i, rock in enumerate(cycle(rocks)):
    if i == 8000:
        break

    rock = tuple((x, y + max_height+3) for x, y in rock)

    try:
        while True:
            try:
                rock = move_rock(rock, next(inp))
            except IndexError:
                pass
            rock = move_rock(rock, 'v')
    except ValueError:
        pass

    prev_height = max_height
    for x, y in rock:
        if y + 1 > max_height:
            max_height = y + 1

    height_diffs.append(max_height - prev_height)

    for x, y in rock:
        g[y][x] = "O"


print(sum(height_diffs[:2022]))

cycle_leadup = height_cycle = None
diffs = ''.join(map(str, height_diffs))
for cycle_len in range(5, len(diffs) // 2):
    for i in range(len(diffs) - cycle_len):
        c1 = diffs[i:i+cycle_len]
        c2 = diffs[i+cycle_len:i+2*cycle_len]

        if c1 == c2 and diffs.count(c1) == (len(diffs) - i) // cycle_len:
            cycle_leadup = height_diffs[:i]
            height_cycle = height_diffs[i:i+cycle_len]
            break
    else:
        continue

    break

if cycle_leadup is None or height_cycle is None:
    raise ValueError

G = 1000000000000
cycle_count, final_index = divmod(G - len(cycle_leadup), len(height_cycle))

print(sum(map(int, cycle_leadup)) + cycle_count * sum(map(int, height_cycle)) + sum(map(int, height_cycle[:final_index])))
