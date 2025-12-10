from bisect import bisect_left, bisect_right
from collections import Counter, deque, defaultdict
from fractions import Fraction
from functools import cache, partial
from itertools import chain, cycle, islice, pairwise, combinations, product, permutations
from heapq import heappop, heappush
from math import inf, dist, prod
from re import findall, match

directions = (0, 1), (1, 0), (0, -1), (-1, 0)

def parse(s):
    result = []

    for line in s.splitlines():
        a, *b, c = line.split()

        a = tuple(map(".#".find, a[1:-1]))
        b = tuple(tuple(map(int, findall(r"-?\d+", k))) for k in b)
        c = tuple(map(int, c[1:-1].split(',')))
        result.append((a, b, c))




    return result


from contextlib import contextmanager

@contextmanager
def removed(amount, buttons):
    for i in buttons:
        amount[i] -= 1

    try:
        yield
    finally:
        for i in buttons:
            amount[i] += 1

# @cache
# def break_down(n, into):
#     if into == 0:
#         if n:
#             return ()

#         return (),

#     if into == 1:
#         return (n,),

#     result = []
#     for i in range(n+1):
#         for rest in break_down(n-i, into-1):
#             result.append((i, *rest))

#     return tuple(result)


def break_down(n, into):
    if into == 0:
        if not n:
            yield ()

        return

    if into == 1:
        yield n,
        return

    for i in range(n+1):
        for rest in break_down(n-i, into-1):
            yield i, *rest


from itertools import compress, count
from matrix import solve_augmented_matrix, Matrix
from fractions import Fraction
from operator import mul

def solve3(buttons, amounts):
    best = sum(amounts)
    def solve2(m, n):
        nonlocal best
        a, b = solve_augmented_matrix(m, n)

        # print(m)
        # print(n)

        # print()

        # print(a)
        # print(b)

        # print()
        # print()

        # print(a)

        # print(a.transposed)
        # print(b)

        free = []
        for i, row in enumerate(a.transposed):
            if sum(1 for _ in filter(None, row)) > 1:
                free.append(i)

        constraints = []
        for row, (n,) in zip(a, b):
            constraint = []
            for i, c in enumerate(row):
                if i in free:
                    constraint.append(-c)

            constraints.append((n, constraint))

        # print(*constraints, sep='\n')

        for attempt in range(best):
            values = break_down

            for values in break_down(attempt, len(free)):
                if sum(values) > best:
                    continue

                assignments = [0]*len(m.columns)
                free_assignments = []
                for i, (f, v) in enumerate(zip(free, values)):
                    assignments[f] = v
                    free_assignments.append(v)

                i = 0
                for n, values in constraints:
                    while i in free:
                        i += 1
                    # print(n, values, i)

                    if n:
                        assignments[i] = n - sum(map(mul, values, free_assignments))
                        if assignments[i] < 0:
                            break
                        if assignments[i].denominator != 1:
                            break

                    i += 1
                else:
                    curr = sum(assignments)

                    # print(assignments, curr)
                    best = min(best, curr)

        # print(best)
        best = int(best)
        return best

    for buttons in permutations(buttons):
        lines = []
        for b in buttons:
            line = []
            for i in range(len(amounts)):
                line.append(Fraction(i in b))
            lines.append(line)

        solve2(Matrix(lines).transposed, Matrix([amounts]).transposed)

    return best


def solve(data):
    result = 0

    for line_number, (_, buttons, amounts) in enumerate(data, 1):

        best = solve3(buttons, amounts)
        result += best
        print(line_number, result, best)


        # break


        # print(buttons, amounts)

    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
