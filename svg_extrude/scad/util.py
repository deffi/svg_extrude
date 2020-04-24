from numbers import Number

from svg_extrude.model import Point, Color
from svg_extrude.scad import StringLiteral, Identifier, RawCode


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
        x = value.x/mm
        y = value.y/mm
        # Round to nm to avoid rounding errors
        x = round(x, 6)
        y = round(y, 6)
        return f"[{x}, {y}]"

    elif isinstance(value, Color):
        return f"\"#{value.html()}\""

    elif isinstance(value, (list, tuple)):
        return f'[{", ".join(render(v) for v in value)}]'

    elif isinstance(value, Identifier):
        return value.value

    elif isinstance(value, RawCode):
        return value.code

    elif isinstance(value, StringLiteral):
        raise NotImplementedError("String escaping not implemented")

    elif isinstance(value, str):
        raise ValueError("Interpretation of str value is ambiguous. Use Identifier, StringLiteral, or Raw class.")

    else:
        raise ValueError(f"Don't know how to render {value!r}")
