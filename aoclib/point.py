from __future__ import annotations

from typing import NamedTuple, Optional
from math import radians, sin, cos

from typing import Union


__all__ = ["Point", "ORIGIN"]


class Point(NamedTuple):
    x: Union[int, float] = 0
    y: Union[int, float] = 0

    def rotated(self, angle_deg: float, pivot: Optional[Point]=None) -> Point:
        if pivot is None:
            pivot = Point(0, 0)

        if pivot == ORIGIN:
            angle_deg %= 360

            x, y = self

            if angle_deg == 0:
                return Point(x,  y)
            elif angle_deg == 90:
                return Point(y, -x)
            elif angle_deg == 180:
                return Point(-x, -y)
            elif angle_deg == 270:
                return Point(-y,  x)

        px, py = pivot

        x, y = self.x - px, self.y - py

        angle_rad = radians(angle_deg)

        s = sin(angle_rad)
        c = cos(angle_rad)

        x, y = c*x - s*y, s*x + c*y

        return Point(x + px, y + py)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
    
    def __neg__(self) -> Point:
        return Point(-self.x, -self.y)

    def __inv__(self) -> Point:
        if not isinstance(self.x, int) or not isinstance(self.y, int):
            raise ValueError

        return Point(~self.x, ~self.y)


ORIGIN = Point(0, 0)
