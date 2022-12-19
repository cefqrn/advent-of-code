from itertools import permutations, product
from re import findall


# lines defined by their value at x=0 (slope is 1 or -1)
ranges_a = []  # like / /
ranges_b = []  # like \ \

scanners = []
with open(0) as f:
    for line in f:
        x, y, bx, by = map(int, findall(r"-?\d+", line))
        dist = abs(x-bx) + abs(y-by)

        scanners.append((x, y, dist))

        ranges_a.append((y-x-dist, y-x+dist))
        ranges_b.append((y+x-dist, y+x+dist))

# find places where a banned range ends 2 before another one starts
a_candidates = set(hi1+1 for (_, hi1), (lo2, _) in permutations(ranges_a, r=2) if hi1 + 2 == lo2)
b_candidates = set(hi1+1 for (_, hi1), (lo2, _) in permutations(ranges_b, r=2) if hi1 + 2 == lo2)

for a, b in product(a_candidates, b_candidates):
    # x + a = b - x
    # 2x = b - a
    # x = (b - a) / 2
    p2x = b - a
    if p2x & 1:
        continue

    px = p2x >> 1
    py = px + a
    # check if the point is in the range of a scanner
    for sx, sy, dist in scanners:
        if abs(sx - px) + abs(sy - py) <= dist:
            break
    else:
        print(px, py, px * 4000000 + py)
        break
