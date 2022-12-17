from __future__ import annotations

from collections.abc import Iterable
from typing import overload


class IntRange:
    @overload
    def __init__(self, a: int, b: int, /) -> None: ...

    @overload
    def __init__(self, a: Iterable[tuple[int, int]], /) -> None: ...

    @overload
    def __init__(self, a: IntRange, /) -> None: ...

    @overload
    def __init__(self, /) -> None: ...

    def __init__(self, a=None, b=None, /):
        self._ranges: tuple[tuple[int, int], ...]
        if isinstance(a, IntRange) and b is None:
            self._ranges = a._ranges
        elif isinstance(a, Iterable) and b is None:
            self._ranges = tuple(a)
        elif isinstance(a, int) and isinstance(b, int):
            self._ranges = (a, b),
        elif a is None and b is None:
            self._ranges = ()
        else:
            raise TypeError

    def __or__(self, other: IntRange) -> IntRange:
        new_ranges = []

        for lo, hi in sorted([*self._ranges, *other._ranges]):
            if new_ranges and new_ranges[-1][1] >= lo - 1:
                new_ranges[-1] = (new_ranges[-1][0], max(hi, new_ranges[-1][1]))
            else:
                new_ranges.append((lo, hi))
        
        return IntRange(new_ranges)
    
    def __sub__(self, other: int) -> IntRange:
        for i, (lo, hi) in enumerate(self._ranges):
            if lo < other <= hi:
                middle = []

                if lo != other:
                    middle.append((lo, other-1))

                if hi != other:
                    middle.append((other+1, hi))

                new_ranges = (*self._ranges[:i], *middle, *self._ranges[i+1:])
                return IntRange(new_ranges)

        return self

    def __len__(self) -> int:
        s = 0
        for lo, hi in self._ranges:
            s += hi - lo + 1

        return s

    def __contains__(self, other: int) -> bool:
        for lo, hi in self._ranges:
            if lo < other <= hi:
                return True
        
        return False
