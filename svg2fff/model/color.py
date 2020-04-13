from collections import namedtuple
from dataclasses import dataclass
from typing import Tuple, Optional, List
from math import sqrt

Rgb = namedtuple("Rgb", ["r", "g", "b"])
Xyz = namedtuple("Xyz", ["x", "y", "z"])
Lab = namedtuple("Lab", ["l", "a", "b"])

Illuminant = namedtuple("Illuminant", ["xn", "yn", "zn"])
illuminant_d65 = {
    # https://en.wikipedia.org/wiki/Illuminant_D65
    2: Illuminant(0.95047, 1.0000, 1.08883),  # 2° observer
    10: Illuminant(0.948110, 1.0000, 1.07304),  # 10° observer
}


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
        """Assumes sRGB"""

        # https://en.wikipedia.org/wiki/SRGB

        def gamma_inv(u):
            if u <= 0.04045:
                return 25*u / 323
            else:
                return ((200*u + 11) / 211) ** (12/5)

        # Linear values
        lr = gamma_inv(self.r)
        lg = gamma_inv(self.g)
        lb = gamma_inv(self.b)

        x = 0.41239080*lr + 0.35758434*lg + 0.18048079*lb
        y = 0.21263901*lr + 0.71516868*lg + 0.07219232*lb
        z = 0.01933082*lr + 0.11919478*lg + 0.95053215*lb

        return Xyz(x, y, z)

    def lab(self, observer=None):
        """Assumes Illuminant D65 because that's what's used for sRGB.
        Observer can be 2 or 10."""

        # https://en.wikipedia.org/wiki/CIELAB_color_space

        observer = observer or 10

        def f(t):
            delta = 6/29
            if t > delta**3:
                return t ** (1 / 3)
            else:
                return t / (3 * delta ** 2) + 4 / 29

        x, y, z = self.xyz()
        xn, yn, zn = illuminant_d65[observer]

        fx = f(x/xn)
        fy = f(y/yn)
        fz = f(z/zn)

        L = 116 * fy - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)

        return Lab(L, a, b)

    #################
    ## Calculation ##
    #################

    def delta_e(self, other: "Color", observer=None) -> float:
        """Color distance ΔE according to CIE76"""

        self_lab = self.lab(observer=observer)
        other_lab = other.lab()

        delta_l = self_lab.l - other_lab.l
        delta_a = self_lab.a - other_lab.a
        delta_b = self_lab.b - other_lab.b

        return sqrt(delta_l**2 + delta_a**2 + delta_b**2)
