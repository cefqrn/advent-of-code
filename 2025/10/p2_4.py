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

        a = bytes(map(".#".find, a[1:-1]))


        b = tuple(bytes(map(int, findall(r"-?\d+", k))) for k in b)
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

    for i, (_, b, c) in enumerate(data):
        @cache
        def solve2(left, buttons):
            if not any(left):
                return 0

            new_buttons = []
            for i, z in enumerate(left):
                if z == 0:
                    for b in buttons:
                        if i not in b:
                            new_buttons.append(b)

                    buttons = new_buttons
                    new_buttons = []

            buttons = tuple(buttons)
            if not buttons:
                return inf

            for i, z in enumerate(left):
                if z:
                    for b in buttons:
                        if i in b:
                            break
                    else:
                        return inf
            # print(left, buttons)



            na = bytearray(left)




            best = inf
            if not buttons:
                return best
            x = buttons[0]
            rest = buttons[1:]

            solves = []
            for z in count(1):
                for i in x:
                    if not na[i]:
                        break
                    na[i] -= 1
                else:
                    solves.append((z, bytes(na)))
                    continue

                break

            best = min(best, solve2(left, rest))
            for z, na in solves:
                if z >= best:
                    break

                best = min(best, z+solve2(bytes(na), rest))


            return best

        best = solve2(bytes(eval(c[1:-1])), b)

        # left = []
        result += best

        print(i, best)

        # break


    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
