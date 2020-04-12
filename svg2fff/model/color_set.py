from typing import Set, Dict
import re

from svg2fff.model import Color


# TODO should be public and in Color? ColorSet(FrozenSet) as parameter.
def _parse_color(string: str, available: Dict[str, Color]):
    """Parses a single color, with optional name.

    Simple color specification:
        "#FF0000" -> Color(1, 0, 0, None)

    With name:
        "bright_red:#FF0000" -> Color(1, 0, 0, "bright_red")

    Select from available colors (keeps the name):
        "red" -> Color(1, 0, 0, "red")

    Select from available colors (specifying a new name):
      * "bright_red:red" -> Color(1, 0, 0, "bright_red")
    """
    if ":" in string:
        name, spec = (s.strip() for s in string.split(":", 1))
    else:
        name, spec = None, string.strip()

    if re.fullmatch('#[0-9A-Fa-f]{6}', spec):
        return Color.from_html(spec[1:], name)
    elif spec in available:
        if name:
            return Color.from_rgb(*available[spec].rgb(), name)
        else:
            return available[spec]
    else:
        raise ValueError(f"Color specification not recognized: {spec!r}")


def parse(string: str, available: Set[Color] = None) -> Set[Color]:
    available = available or set()
    available = { color.name: color for color in available }

    return { _parse_color(s, available) for s in string.split(",") }
