from __future__ import annotations

from typing import NamedTuple, Optional
from math import radians, sin, cos


class Point(NamedTuple):
    x: float = 0
    y: float = 0

    def rotated(self, angle_deg: float, pivot: Optional[Point]=None) -> Point:
        if pivot is None:
            pivot = Point(0, 0)

        px, py = pivot

        x, y = self.x - px, self.y - py

        angle_rad = radians(angle_deg)

        s = sin(angle_rad)
        c = cos(angle_rad)

        x, y = c*x - s*y, s*x + c*y

        return Point(x + px, y + py)
