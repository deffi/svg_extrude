from collections import namedtuple
from dataclasses import dataclass
from typing import Tuple, Optional, List
from math import sqrt

Rgb = namedtuple("Rgb", ["r", "g", "b"])
Xyz = namedtuple("Xyz", ["x", "y", "z"])
Lab = namedtuple("Lab", ["l", "a", "b"])


@dataclass(frozen=True)
class Color:
    r: float
    g: float
    b: float
    name: Optional[str] = None

    def display_name(self) -> str:
        if self.name:
            return self.name
        else:
            return self.html()

    ##############
    ## Creation ##
    ##############

    @classmethod
    def from_html(cls, value: str, name: Optional[str] = None) -> "Color":
        if len(value) == 6:
            r = int(value[0:2], 16) / 255
            g = int(value[2:4], 16) / 255
            b = int(value[4:6], 16) / 255
            return cls(r, g, b, name)
        elif len(value) == 7 and value[0] == "#":
            return cls.from_html(value[1:], name)
        else:
            raise ValueError(f"Unrecognized HTML color: {html}")

    ################
    ## Conversion ##
    ################

    def rgb(self) -> Tuple[float, float, float]:
        return Rgb(self.r, self.g, self.b)

    def html(self) -> str:
        return "".join(f"{round(x*255):02X}" for x in self.rgb())

    def xyz(self):
        # TODO verify and add reference
        def linear(v):
            if v <= 0.04045:
                return v / 12.92
            else:
                return ((v + 0.055) / 1.055) ** 2.4

        lr = linear(self.r)
        lg = linear(self.g)
        lb = linear(self.b)

        x = 0.412424  * lr + 0.357579 * lg + 0.180464  * lb
        y = 0.212656  * lr + 0.715158 * lg + 0.0721856 * lb
        z = 0.0193324 * lr + 0.119193 * lg + 0.950444  * lb

        return Xyz(x, y, z)

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

        return Lab(L, a, b)

    #################
    ## Calculation ##
    #################

    def delta_e(self, other: "Color") -> float:
        """Color distance ΔE according to CIE76"""

        self_lab = self.lab()
        other_lab = other.lab()

        delta_l = self_lab.l - other_lab.l
        delta_a = self_lab.a - other_lab.a
        delta_b = self_lab.b - other_lab.b

        return sqrt(delta_l**2 + delta_a**2 + delta_b**2)
