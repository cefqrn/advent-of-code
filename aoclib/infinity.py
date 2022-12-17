from __future__ import annotations

from functools import total_ordering
from typing import Any, Literal


@total_ordering
class Infinity:
    """
    class of objects that are greater/smaller than everything except other Infinity objects
    used in defaultdicts that default to infinity
    """
    def __init__(self, is_negative: bool=False) -> None:
        self.is_negative = is_negative

    def __add__(self, other: Any) -> Infinity:
        if isinstance(other, Infinity) and self.is_negative ^ other.is_negative:
            raise ValueError("Can't add Infinity to Infinity of opposing sign.")

        return Infinity(self.is_negative)
    
    def __sub__(self, other: Any) -> Infinity:
        if isinstance(other, Infinity) and self.is_negative == other.is_negative:
            raise ValueError("Can't subtract Infinity from Infinity of same sign.")
        
        return Infinity(self.is_negative)

    def __mul__(self, other: Any) -> Infinity:
        try:
            return Infinity(self.is_negative ^ (other < 0))
        except TypeError:
            return Infinity(self.is_negative)

    def __truediv__(self, other: Any) -> Infinity:
        if isinstance(other, Infinity):
            raise ValueError("Can't divide Infinity by Infinity.")
        
        try:
            return Infinity(self.is_negative ^ (other < 0))
        except TypeError:
            return Infinity(self.is_negative)

    def __rtruediv__(self, _: Any) -> Literal[0]:
        # Infinity / Infinity is handled in __truediv__
        return 0

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__

    def __neg__(self) -> Infinity:
        return Infinity(not self.is_negative)

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Infinity):
            return other.is_negative > self.is_negative

        return not self.is_negative
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Infinity) and self.is_negative == other.is_negative

    def __repr__(self) -> str:
        return '-inf' if self.is_negative else 'inf'
    
    __str__ = __repr__


class InfinityPositive(Infinity):
    def __init__(self):
        super().__init__(False)


class InfinityNegative(Infinity):
    def __init__(self):
        super().__init__(True)


INFINITY          = InfinityPositive()
INFINITY_NEGATIVE = InfinityNegative()
