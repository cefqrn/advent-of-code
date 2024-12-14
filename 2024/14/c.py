from collections import Counter
from itertools import count
from re import findall

dimensions = w, h = 101, 103

def get_score(robots):
    a=b=c=d=0
    for x, y in robots:
        if x < w//2:
            if y < h//2:
                a += 1
            elif y > h//2:
                b += 1
        elif x > w//2:
            if y < h//2:
                c += 1
            elif y > h//2:
                d += 1

    return a*b*c*d

def solve_p1(robots):
    grid = []
    for px, py, vx, vy in robots:
        pos = (px+vx*100)%w, (py+vy*100)%h
        grid += pos,

    return get_score(grid)

def find_lines(robots, axis, start=0):
    """find moment with at least 2 lines in selected axis"""
    for time in count(start):
        counts = Counter()
        for px, py, vx, vy in robots:
            pos, v = (px, py), (vx, vy)

            c = (pos[axis] + v[axis]*time) % dimensions[axis]
            counts[c] += 1

        # at least 2 lines of length 15
        if counts.most_common(2)[1][1] > 15:
            return time

with open(0) as f:
    robots = [
        tuple(map(int, findall(r"-?\d+", line)))
        for line in f.readlines()
    ]

# find vertical lines
a0 = find_lines(robots, 0)
a1 = find_lines(robots, 0, a0+1)
a_len = a1 - a0  # guaranteed to be <= w since p + v*w congruent to p mod w

# find horizontal lines
b0 = find_lines(robots, 1)
b1 = find_lines(robots, 1, b0+1)
b_len = b1 - b0  # guaranteed to be <= h since p + v*h congruent to p mod h

def solve(a, b):
    quotients = []
    while b != 0:
        (d, b), a = divmod(a, b), b
        quotients.append(d)

    quotients.pop()

    s, t = 1, -quotients.pop()
    while quotients:
        s, t = t, s + t * -quotients.pop()

    return a, s, t

gcd, s, t = solve(a_len, b_len)

k, r = divmod(b0 - a0, gcd)
assert not r

sol = a0 + (k*s)*a_len
lcm = a_len*b_len // gcd

print(solve_p1(robots))
print(sol % lcm)

# print(a0 + k*s * a_len)
# print(b0 + k*t * b_len)

# print(k*s, k*t)
# print(k*s * a_len + k*t * b_len)

# a0 + x*a_len = sol for some x
# b0 + y*b_len = sol for some y
# a0 + x*a_len = b0 + y*b_len
# x*a_len - y*b_len = b0 - a0
# s*a_len + t*b_len = gcd(a_len, b_len) for some s, t
# b0 - a0 = k * gcd(a_len, b_len) for some k
#         = k * (s*a_len + t*b_len)
#         = k*s * a_len + (-k*t) * b_len
#         =  x  * a_len -    y   * b_len
# so x = k*s, y = -k*t
# so sol = a0 + k*s * a_len = b0 + -k*t * b_len
# want smallest positive solution
# so take sol % lcm(a_len, b_len)

# 33 = 2 * 12 + 9
# 12 = 1 *  9 + 3
#  9 = 3 *  3 + 0 stop, gcd = 3

# a     _   b    _
#       d   a    b
# 240 = 5 * 46 + 10    10 = 240 - 5 * 46
#  46 = 4 * 10 +  6     6 =  46 - 4 * 10
#  10 = 1 * 6  +  4     4 =  10 - 1 *  6
#   6 = 1 * 4  +  2     2 =   6 - 1 *  4
#   4 = 2 * 2  +  0   stop, gcd = 2

# 2 =  1 *   6 - 1 * 4
# 2 =  1 *   6 - 1 * (10 - 1 * 6)
# 2 = -1 *  10 + 2 * 6 
# 2 = -1 *  10 + 2 * (46 - 4 * 10)
# 2 =  2 *  46 - 9 * 10
# 2 =  2 *  46 - 9 * (240 - 5 * 46)
# 2 = -9 * 240 + 47 * 46
