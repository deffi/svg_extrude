from dataclasses import dataclass
from typing import Tuple, Optional, List
import colorsys
import random
from math import sqrt

from svg2fff.util import closest

@dataclass()
class Color:
    _r: float
    _g: float
    _b: float
    _name: Optional[str]

    def __init__(self):
        pass

    def __repr__(self):
        return f"Color.from_rgb({self._r}, {self._g}, {self._b}, {self._name!r})"

    def __hash__(self):
        return hash(self.rgb())

    # TODO from dataclass?
    def __eq__(self, other):
        return (isinstance(other, Color)
            and other._r == self._r
            and other._g == self._g
            and other._b == self._b
            and other._name == self._name)

    # TODO can dataclass do this?
    @property
    def name(self) -> Optional[str]:
        return self._name

    def display_name(self) -> str:
        if self._name:
            return self._name
        else:
            return self.to_html()

    def rgb(self) -> Tuple[float, float, float]:
        return (self._r, self._g, self._b)

    def hsv(self):
        return colorsys.rgb_to_hsv(*self.rgb())

    def xyz(self):
        # TODO verify and add reference
        def linear(v):
            if v <= 0.04045:
                return v / 12.92
            else:
                return ((v + 0.055) / 1.055) ** 2.4

        lr = linear(self._r)
        lg = linear(self._g)
        lb = linear(self._b)

        x = 0.412424  * lr + 0.357579 * lg + 0.180464  * lb
        y = 0.212656  * lr + 0.715158 * lg + 0.0721856 * lb
        z = 0.0193324 * lr + 0.119193 * lg + 0.950444  * lb

        return (x, y, z)

    def lab(self, observer=10):
        # TODO verify and add reference
        def root(v):
            if v < 216/24389:
                return (24389/27 * v + 16) / 116
            else:
                return v ** (1 / 3)

        if observer == 2:
            xn, yn, zn = 0.95047, 1.00000, 1.08883  # 2°, D65
        elif observer == 10:
            xn, yn, zn = 0.94811, 1.00000, 1.07304  # 10°, D65
        else:
            raise ValueError(f"Invalid observer: {observer}°")

        x, y, z = self.xyz()

        rootx = root(x/xn)
        rooty = root(y/yn)
        rootz = root(z/zn)

        L = 116 * rooty - 16
        a = 500 * (rootx - rooty)
        b = 200 * (rooty - rootz)

        return (L, a, b)

    @classmethod
    def from_rgb(cls, r: float, g: float, b: float, name: Optional[str]) -> "Color":
        color = cls()
        color._r = r
        color._g = g
        color._b = b
        color._name = name
        return color

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float, name: Optional[str]) -> "Color":
        return cls.from_rgb(*colorsys.hsv_to_rgb(h, s, v), name)

    @classmethod
    def from_html(cls, html: str, name: Optional[str]) -> "Color":
        if len(html) != 6:
            raise ValueError(f"Unrecognized HTML color: {html}")

        r = int(html[0:2], 16)
        g = int(html[2:4], 16)
        b = int(html[4:6], 16)

        return cls.from_rgb(r/255, g/255, b/255, name)

    def to_html(self) -> str:
        return "".join(f"{round(x*255):02X}" for x in self.rgb())

    @classmethod
    def random_hsv(cls, *, h: Optional[float] = None, s: Optional[float] = None, v: Optional[float] = None) -> "Color":
        if h is None: h = random.uniform(0, 1)
        if s is None: s = random.uniform(0, 1)
        if v is None: v = random.uniform(0, 1)
        return cls.from_hsv(h, s, v)

    def closest(self, available: List["Color"]) -> "Color":
        """Finds the closest color according to color distance ΔE according to CIE76"""

        def delta_e(a: Color, b: Color):
            a = a.lab()
            b = b.lab()
            dl = b[0] - a[0]
            da = b[1] - a[1]
            db = b[2] - a[2]
            return sqrt(dl**2 + da**2 + db**2)

        return closest(available, self, delta_e)
