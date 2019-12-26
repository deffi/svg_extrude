import colorsys
import random


class Color:
    def __init__(self):
        self._r = 0
        self._g = 0
        self._b = 0

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
    def random_hsv(cls, *, h = None, s = None, v = None):
        if h is None: h = random.uniform(0, 1)
        if s is None: s = random.uniform(0, 1)
        if v is None: v = random.uniform(0, 1)
        return cls.from_hsv(h, s, v)
