from dataclasses import dataclass
from typing import Tuple, Optional, List

import colorsys
import random

from svg2fff.util import closest


@dataclass()
class Color:
    _r: float = 0
    _g: float = 0
    _b: float = 0

    def __init__(self):
        pass

    def __repr__(self):
        return f"Color.from_rgb({self._r}, {self._g}, {self._b})"

    def __hash__(self):
        return hash(self.rgb())

    def __eq__(self, other):
        return (isinstance(other, Color)
            and other._r == self._r
            and other._g == self._g
            and other._b == self._b)

    def rgb(self) -> Tuple[float, float, float]:
        return (self._r, self._g, self._b)

    def hsv(self):
        return colorsys.rgb_to_hsv(*self.rgb())

    @classmethod
    def from_rgb(cls, r: float, g: float, b: float) -> "Color":
        color = cls()
        color._r = r
        color._g = g
        color._b = b
        return color

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float) -> "Color":
        return cls.from_rgb(*colorsys.hsv_to_rgb(h, s, v))

    @classmethod
    def from_html(cls, html: str) -> "Color":
        if len(html) != 6:
            raise ValueError(f"Unrecognized HTML color: {html}")

        r = int(html[0:2], 16)
        g = int(html[2:4], 16)
        b = int(html[4:6], 16)

        return cls.from_rgb(r/255, g/255, b/255)

    def to_html(self) -> str:
        return "".join(f"{round(x*255):02X}" for x in self.rgb())

    @classmethod
    def random_hsv(cls, *, h: Optional[float] = None, s: Optional[float] = None, v :Optional[float] = None) -> "Color":
        if h is None: h = random.uniform(0, 1)
        if s is None: s = random.uniform(0, 1)
        if v is None: v = random.uniform(0, 1)
        return cls.from_hsv(h, s, v)

    def invert(self) -> "Color":
        return Color.from_rgb(1 - self._r, 1 - self._g, 1 - self._b)

    def closest_hsv(self, available: List["Color"]) -> "Color":
        def d_squared(a: Color, b: Color):
            a = a.hsv()
            b = b.hsv()
            dh = 0.5 - abs(b[0] - a[0] - 0.5)  # Wrapping; TODO MH test
            ds = b[1] - a[1]
            dv = b[2] - a[2]
            return dh**2 + ds**2 + dv**2

        return closest(available, self, d_squared)
