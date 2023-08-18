from __future__ import annotations

from itertools import tee
from time import perf_counter
from typing import Generator, Iterator

s = "1113122113"

def iterate(s: Iterator[str]) -> Generator[str, Iterator[str], None]:
    count = 1
    prev = next(s)
    
    for n in s:
        if prev == n:
            count += 1
        else:
            yield f'{count}'
            yield prev
            prev = n
            count = 1

    yield f'{count}'
    yield prev

def count_next(s: Iterator[str]) -> int:
    c = 2

    prev = next(s)
    for n in s:
        if prev != n:
            c += 2
            prev = n

    return c


st = perf_counter()

s = iter(s)
for i in range(50 - 1):
    s = iterate(s)
    if i == 40 - 1 - 1:
        s, s1 = tee(s)
        print(f'p1: {count_next(s1)} in {perf_counter() - st:.2f} s')

print(f'p2: {count_next(s)} in {perf_counter() - st:.2f} s')