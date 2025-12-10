# https://colab.research.google.com/github/philzook58/z3_tutorial/blob/master/Z3%20Tutorial.ipynb
# https://z3prover.github.io/api/html/namespacez3py.html

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




from z3 import Int, Solver, sat
from operator import mul
from itertools import count

def solve1(data):
    result = 0

    for line_number, (_, buttons, amounts) in enumerate(data, 1):
        lines = []
        variables = []

        

        constraints = []
        for i, b in enumerate(buttons):
            line = [0] * len(amounts)
            for x in b:
                line[x] = 1
            lines.append(line)
            variables.append(var := Int(f"x{i:03}"))

            constraints.append(var >= 0)
            # s.add(var >= 0)

        for coeffs, required in zip(zip(*lines), amounts):
            terms = sum(map(mul, variables, coeffs), start=-required)
            constraints.append(terms == 0)
            # s.add(terms == 0)

        # print(s.pop())

        variable_sum = sum(variables[1:], start=variables[0])
        # print(variable_sum)
        for i in count(min(amounts)):
            s = Solver()
            for constraint in constraints:
                s.add(constraint)

            s.add(variable_sum == i)
            if s.check() == sat:
                soln = str(s.model())
                print()

                result += sum(map(int, findall(r"\d+(?=[,\]])", soln)))
                break



        print(repr(s.check()))
        print(s.model())
        # sum(variables) == 

        # solve(*constraints)

        print()

        # best = solve(buttons, amounts)
        # result += best
        # print(line_number, result, best)

    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve1(data))
