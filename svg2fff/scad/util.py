from numbers import Number
import re

from svg2fff.model import Point
from svg2fff.scad.types import StringLiteral, Identifier


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

    elif isinstance(value, (list, tuple)):
        return f'[{", ".join(render(v) for v in value)}]'

    elif isinstance(value, Identifier):
        return value

    elif isinstance(value, StringLiteral):
        raise NotImplementedError("String escaping not implemented")

    elif isinstance(value, str):
        raise ValueError("Interpretation of str value is ambiguous. Use Identifier or StringLiteral class.")

    else:
        raise ValueError(f"Don't know how to render {value!r}")


def identifier_part(string: str) -> str:
    """Creates a string that can be used as part of an identifier, based on the
    supplied string.

    The result is not necessarily a valid identifier: it might be an OpenSCAD
    reserved word or consist only of digits.
    """


    # OpenSCAD does not seem to document the rules for identifiers, but looking
    # at its lexer.l, it seems that only latin letters, digits, and underscores
    # are allowed.
    return re.sub(r'[^a-zA-Z0-9_]', '_', string)
