from bisect import bisect_left, bisect_right
from collections import Counter, deque, defaultdict
from fractions import Fraction
from functools import cache, partial
from itertools import chain, cycle, islice, pairwise, combinations, product
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

from itertools import compress, count

def solve(data):
    result = 0

    for i, (_, buttons, amounts) in enumerate(data[50:], 51):
        # @cache
        def solve2(remaining):
            # print(remaining)

            avoid = set()
            needed = set()
            for i, x in enumerate(remaining):
                if not x:
                    avoid.add(i)
                else:
                    needed.add(i)

            allowed = []
            for b in buttons:
                if not avoid.intersection(b):
                    allowed.append(b)

            for b in allowed:
                needed.difference_update(b)
            if needed:
                return inf

            left = []
            for curr, x in enumerate(remaining):
                if not x:
                    continue

                relevant = []
                for b in allowed:
                    if curr in b:
                        relevant.append(b)

                left.append((curr, relevant))

            if not left:
                return 0

            curr, relevant = min(left, key=lambda x: len(x[1]))
            relevant.sort(key=len, reverse=True)


            # print(remaining, relevant)

            left = [(0, 0, remaining)]
            best = inf
            while left:
                cost, current, amounts = left.pop()
                if cost > best:
                    break

                if not amounts[curr]:
                    best = min(best, cost + solve2(tuple(amounts)))
                    continue

                if current >= len(relevant):
                    continue

                for z in count(0):
                    new_amounts = list(amounts)
                    for i in relevant[current]:
                        if new_amounts[i] < z:
                            break

                        new_amounts[i] -= z
                    else:
                        left.append((cost+z, current+1, new_amounts))
                        continue
                    break

            return best

        best = solve2(amounts)
        result += best
        print(i, result, best)

    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
