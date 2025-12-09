from itertools import combinations, count
from math import inf

def parse(s):
    result = []

    for line in s.splitlines():
        result.append(eval(line))

    return result

def is_valid(data, curr):
    i, j = curr

    p, q = data[i], data[j]

    lo_x, hi_x = sorted([p[0], q[0]])
    lo_y, hi_y = sorted([p[1], q[1]])

    for p, q in zip(count(i), count(i+1)):
        p %= len(data)
        q %= len(data)

        if q == i:
            return True

        x1, y1 = data[p]
        x2, y2 = data[q]

        assert (x1 == x2) ^ (y1 == y2)

        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])

        if x1 == x2 and lo_x < x1 and x2 < hi_x and (
                (y1 <= lo_y and lo_y <  y2)
             or (y1 <  hi_y and hi_y <= y2)
             or (lo_y <  y1 and y1 <  hi_y)
             or (lo_y <  y2 and y2 <  hi_y)):
            return False
        elif lo_y < y1 and y2 < hi_y and (
                (x1 <= lo_x and lo_x <  x2)
             or (x1 <  hi_x and hi_x <= x2)
             or (lo_x <  x1 and x1 <  hi_x)
             or (lo_x <  x2 and x2 <  hi_x)):
            return False

def solve(data):
    result = -inf
    for i, j in combinations(range(len(data)), 2):
        a, b = data[i], data[j]

        x1, y1 = a
        x2, y2 = b

        area = -~abs(x2 - x1) * -~abs(y2 - y1)
        if area < result:
            continue

        if is_valid(data, (i, j)):
            result = max(area, result)

    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
