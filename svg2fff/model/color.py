from dataclasses import dataclass
from typing import Tuple, Optional, List

import colorsys
import random

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
        return f"Color.from_rgb({self._r}, {self._g}, {self._b})"

    def __hash__(self):
        return hash(self.rgb())

    def __eq__(self, other):
        return (isinstance(other, Color)
            and other._r == self._r
            and other._g == self._g
            and other._b == self._b)

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

    def closest_hsv(self, available: List["Color"]) -> "Color":
        def d_squared(a: Color, b: Color):
            a = a.hsv()
            b = b.hsv()
            dh = 0.5 - abs(b[0] - a[0] - 0.5)  # Wrapping; TODO MH test
            ds = b[1] - a[1]
            dv = b[2] - a[2]
            return dh**2 + ds**2 + dv**2

        return closest(available, self, d_squared)

# CSS colors from https://www.w3.org/TR/css-color-3/
css_default = [
    Color.from_html("000000", "black"),
    Color.from_html("C0C0C0", "silver"),
    Color.from_html("808080", "gray"),
    Color.from_html("FFFFFF", "white"),
    Color.from_html("800000", "maroon"),
    Color.from_html("FF0000", "red"),
    Color.from_html("800080", "purple"),
    Color.from_html("FF00FF", "fuchsia"),
    Color.from_html("008000", "green"),
    Color.from_html("00FF00", "lime"),
    Color.from_html("808000", "olive"),
    Color.from_html("FFFF00", "yellow"),
    Color.from_html("000080", "navy"),
    Color.from_html("0000FF", "blue"),
    Color.from_html("008080", "teal"),
    Color.from_html("00FFFF", "aqua"),
]

svg = [
    Color.from_html("f0f8ff", "aliceblue"),
    Color.from_html("faebd7", "antiquewhite"),
    Color.from_html("00ffff", "aqua"),
    Color.from_html("7fffd4", "aquamarine"),
    Color.from_html("f0ffff", "azure"),
    Color.from_html("f5f5dc", "beige"),
    Color.from_html("ffe4c4", "bisque"),
    Color.from_html("000000", "black"),
    Color.from_html("ffebcd", "blanchedalmond"),
    Color.from_html("0000ff", "blue"),
    Color.from_html("8a2be2", "blueviolet"),
    Color.from_html("a52a2a", "brown"),
    Color.from_html("deb887", "burlywood"),
    Color.from_html("5f9ea0", "cadetblue"),
    Color.from_html("7fff00", "chartreuse"),
    Color.from_html("d2691e", "chocolate"),
    Color.from_html("ff7f50", "coral"),
    Color.from_html("6495ed", "cornflowerblue"),
    Color.from_html("fff8dc", "cornsilk"),
    Color.from_html("dc143c", "crimson"),
    Color.from_html("00ffff", "cyan"),
    Color.from_html("00008b", "darkblue"),
    Color.from_html("008b8b", "darkcyan"),
    Color.from_html("b8860b", "darkgoldenrod"),
    Color.from_html("a9a9a9", "darkgray"),
    Color.from_html("006400", "darkgreen"),
    Color.from_html("a9a9a9", "darkgrey"),
    Color.from_html("bdb76b", "darkkhaki"),
    Color.from_html("8b008b", "darkmagenta"),
    Color.from_html("556b2f", "darkolivegreen"),
    Color.from_html("ff8c00", "darkorange"),
    Color.from_html("9932cc", "darkorchid"),
    Color.from_html("8b0000", "darkred"),
    Color.from_html("e9967a", "darksalmon"),
    Color.from_html("8fbc8f", "darkseagreen"),
    Color.from_html("483d8b", "darkslateblue"),
    Color.from_html("2f4f4f", "darkslategray"),
    Color.from_html("2f4f4f", "darkslategrey"),
    Color.from_html("00ced1", "darkturquoise"),
    Color.from_html("9400d3", "darkviolet"),
    Color.from_html("ff1493", "deeppink"),
    Color.from_html("00bfff", "deepskyblue"),
    Color.from_html("696969", "dimgray"),
    Color.from_html("696969", "dimgrey"),
    Color.from_html("1e90ff", "dodgerblue"),
    Color.from_html("b22222", "firebrick"),
    Color.from_html("fffaf0", "floralwhite"),
    Color.from_html("228b22", "forestgreen"),
    Color.from_html("ff00ff", "fuchsia"),
    Color.from_html("dcdcdc", "gainsboro"),
    Color.from_html("f8f8ff", "ghostwhite"),
    Color.from_html("ffd700", "gold"),
    Color.from_html("daa520", "goldenrod"),
    Color.from_html("808080", "gray"),
    Color.from_html("008000", "green"),
    Color.from_html("adff2f", "greenyellow"),
    Color.from_html("808080", "grey"),
    Color.from_html("f0fff0", "honeydew"),
    Color.from_html("ff69b4", "hotpink"),
    Color.from_html("cd5c5c", "indianred"),
    Color.from_html("4b0082", "indigo"),
    Color.from_html("fffff0", "ivory"),
    Color.from_html("f0e68c", "khaki"),
    Color.from_html("e6e6fa", "lavender"),
    Color.from_html("fff0f5", "lavenderblush"),
    Color.from_html("7cfc00", "lawngreen"),
    Color.from_html("fffacd", "lemonchiffon"),
    Color.from_html("add8e6", "lightblue"),
    Color.from_html("f08080", "lightcoral"),
    Color.from_html("e0ffff", "lightcyan"),
    Color.from_html("fafad2", "lightgoldenrodyellow"),
    Color.from_html("d3d3d3", "lightgray"),
    Color.from_html("90ee90", "lightgreen"),
    Color.from_html("d3d3d3", "lightgrey"),
    Color.from_html("ffb6c1", "lightpink"),
    Color.from_html("ffa07a", "lightsalmon"),
    Color.from_html("20b2aa", "lightseagreen"),
    Color.from_html("87cefa", "lightskyblue"),
    Color.from_html("778899", "lightslategray"),
    Color.from_html("778899", "lightslategrey"),
    Color.from_html("b0c4de", "lightsteelblue"),
    Color.from_html("ffffe0", "lightyellow"),
    Color.from_html("00ff00", "lime"),
    Color.from_html("32cd32", "limegreen"),
    Color.from_html("faf0e6", "linen"),
    Color.from_html("ff00ff", "magenta"),
    Color.from_html("800000", "maroon"),
    Color.from_html("66cdaa", "mediumaquamarine"),
    Color.from_html("0000cd", "mediumblue"),
    Color.from_html("ba55d3", "mediumorchid"),
    Color.from_html("9370db", "mediumpurple"),
    Color.from_html("3cb371", "mediumseagreen"),
    Color.from_html("7b68ee", "mediumslateblue"),
    Color.from_html("00fa9a", "mediumspringgreen"),
    Color.from_html("48d1cc", "mediumturquoise"),
    Color.from_html("c71585", "mediumvioletred"),
    Color.from_html("191970", "midnightblue"),
    Color.from_html("f5fffa", "mintcream"),
    Color.from_html("ffe4e1", "mistyrose"),
    Color.from_html("ffe4b5", "moccasin"),
    Color.from_html("ffdead", "navajowhite"),
    Color.from_html("000080", "navy"),
    Color.from_html("fdf5e6", "oldlace"),
    Color.from_html("808000", "olive"),
    Color.from_html("6b8e23", "olivedrab"),
    Color.from_html("ffa500", "orange"),
    Color.from_html("ff4500", "orangered"),
    Color.from_html("da70d6", "orchid"),
    Color.from_html("eee8aa", "palegoldenrod"),
    Color.from_html("98fb98", "palegreen"),
    Color.from_html("afeeee", "paleturquoise"),
    Color.from_html("db7093", "palevioletred"),
    Color.from_html("ffefd5", "papayawhip"),
    Color.from_html("ffdab9", "peachpuff"),
    Color.from_html("cd853f", "peru"),
    Color.from_html("ffc0cb", "pink"),
    Color.from_html("dda0dd", "plum"),
    Color.from_html("b0e0e6", "powderblue"),
    Color.from_html("800080", "purple"),
    Color.from_html("ff0000", "red"),
    Color.from_html("bc8f8f", "rosybrown"),
    Color.from_html("4169e1", "royalblue"),
    Color.from_html("8b4513", "saddlebrown"),
    Color.from_html("fa8072", "salmon"),
    Color.from_html("f4a460", "sandybrown"),
    Color.from_html("2e8b57", "seagreen"),
    Color.from_html("fff5ee", "seashell"),
    Color.from_html("a0522d", "sienna"),
    Color.from_html("c0c0c0", "silver"),
    Color.from_html("87ceeb", "skyblue"),
    Color.from_html("6a5acd", "slateblue"),
    Color.from_html("708090", "slategray"),
    Color.from_html("708090", "slategrey"),
    Color.from_html("fffafa", "snow"),
    Color.from_html("00ff7f", "springgreen"),
    Color.from_html("4682b4", "steelblue"),
    Color.from_html("d2b48c", "tan"),
    Color.from_html("008080", "teal"),
    Color.from_html("d8bfd8", "thistle"),
    Color.from_html("ff6347", "tomato"),
    Color.from_html("40e0d0", "turquoise"),
    Color.from_html("ee82ee", "violet"),
    Color.from_html("f5deb3", "wheat"),
    Color.from_html("ffffff", "white"),
    Color.from_html("f5f5f5", "whitesmoke"),
    Color.from_html("ffff00", "yellow"),
    Color.from_html("9acd32", "yellowgreen"),
]
