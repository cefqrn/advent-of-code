from collections.abc import Iterable, Generator
from functools import partial
from itertools import chain
from typing import TypeVar

T = TypeVar("T")

def is_valid_triangle(dimensions: tuple[int, int, int]) -> bool:
    a, b, c = sorted(dimensions)
    return a + b > c

def iter_len(iterable: Iterable) -> int:
    """get the length of an iterable without storing all of its elements"""
    length = 0
    for _ in iterable:
        length += 1

    return length

def batched(iterable: Iterable[T], batch_size: int) -> Generator[tuple[T, ...], None, None]:
    """group elements of an iterable into batches of length batch_size"""
    yield from zip(*batch_size*[iter(iterable)])

with open(0) as f:
    dimensions = [tuple(map(int, line.split())) for line in f.readlines()]

p1 = iter_len(filter(is_valid_triangle, dimensions))

batched_by_3 = partial(batched, batch_size=3)
p2 = iter_len(filter(is_valid_triangle, chain(*map(batched_by_3, zip(*dimensions)))))

print(p1, p2)
