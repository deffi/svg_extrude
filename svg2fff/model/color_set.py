from typing import Dict, Optional
import re

from svg2fff.model import Color
from svg2fff.util import arg_min


def _parse_color(string: str, available: Dict[str, Color]):
    if ":" in string:
        name, spec = (s.strip() for s in string.split(":", 1))
    else:
        name, spec = None, string.strip()

    if re.fullmatch('#[0-9A-Fa-f]{6}', spec):
        return Color.from_html(spec[1:], name)
    elif spec in available:
        if name:
            return Color(*available[spec].rgb(), name)
        else:
            return available[spec]
    else:
        raise ValueError(f"Color specification not recognized: {spec!r}")


class ColorSet(frozenset):
    def __new__(cls, seq=()):
        return frozenset.__new__(cls, seq)

    def __init__(self, seq=()):
        super().__init__()
        self._by_name = None

    @property
    def by_name(self):
        if self._by_name is None:
            self._by_name = {color.name: color
                             for color in self
                             if color.name is not None}

        return self._by_name

    @classmethod
    def parse(cls, string: str, available: Optional["ColorSet"] = None) -> "ColorSet":
        """Parses a comma-separated list of colors.

        Simple color specification:
            "#FF0000" -> Color(1, 0, 0)

        With name:
            "bright_red:#FF0000" -> Color(1, 0, 0, "bright_red")

        Select from available colors (keeps the name):
            "red" -> Color(1, 0, 0, "red")

        Select from available colors (specifying a new name):
            "bright_red:red" -> Color(1, 0, 0, "bright_red")
        """
        available = available or ColorSet()
        return cls(_parse_color(s, available.by_name) for s in string.split(","))

    def closest(self, color: Color) -> "Color":
        return arg_min(self, color.delta_e)
