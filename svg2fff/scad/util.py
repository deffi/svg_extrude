from numbers import Number
import re

from svg2fff.model import Point, Color
from svg2fff.scad import StringLiteral, Identifier


def render(value) -> str:
    """Renders a value to OpenSCAD representation

    The following types are supported explicitly:
      * numbers.Number - rendered as literal
      * list and tuple - rendered recursively as vectors
      * StringLiteral - rendered as string literal with quoting and escaping
        (not implemented)
      * Identifier - rendered as identifier without quoting or escaping

    Also supported:
      * model.Point - by virtue of being a (named)tuple of numbers

    Other types raise a ValueError.
    """

    if isinstance(value, Number):
        return f"{value}"

    elif isinstance(value, Point):
        # OpenSCAD uses millimeters
        mm = 1e-3
        return f"[{value.x / mm}, {value.y / mm}]"

    elif isinstance(value, Color):
        return f"\"#{value.html()}\""

    elif isinstance(value, (list, tuple)):
        return f'[{", ".join(render(v) for v in value)}]'

    elif isinstance(value, Identifier):
        return value.value

    elif isinstance(value, StringLiteral):
        raise NotImplementedError("String escaping not implemented")

    elif isinstance(value, str):
        raise ValueError("Interpretation of str value is ambiguous. Use Identifier or StringLiteral class.")

    else:
        raise ValueError(f"Don't know how to render {value!r}")
