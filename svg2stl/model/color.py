import colorsys
import random


class Color:
    def __init__(self):
        self._r = 0
        self._g = 0
        self._b = 0

    def __repr__(self):
        return f"Color.from_rgb({self._r}, {self._g}, {self._b})"

    def __hash__(self):
        return hash(self.rgb())

    def __eq__(self, other):
        return (isinstance(other, Color)
            and other._r == self._r
            and other._g == self._g
            and other._b == self._b)

    def rgb(self):
        return (self._r, self._g, self._b)

    def hsv(self):
        return colorsys.rgb_to_hsv(*self.rgb())

    @classmethod
    def from_rgb(cls, r, g, b):
        color=cls()
        color._r = r
        color._g = g
        color._b = b
        return color

    @classmethod
    def from_hsv(cls, h, s, v):
        return cls.from_rgb(*colorsys.hsv_to_rgb(h, s, v))

    @classmethod
    def from_html(cls, html):
        if len(html) != 6:
            raise ValueError(f"Unrecognized HTML color: {html}")

        r = int(html[0:2], 16)
        g = int(html[2:4], 16)
        b = int(html[4:6], 16)

        return cls.from_rgb(r/255, g/255, b/255)

    def to_html(self):
        return "".join(f"{round(x*255):02X}" for x in self.rgb())

    @classmethod
    def random_hsv(cls, *, h = None, s = None, v = None):
        if h is None: h = random.uniform(0, 1)
        if s is None: s = random.uniform(0, 1)
        if v is None: v = random.uniform(0, 1)
        return cls.from_hsv(h, s, v)
