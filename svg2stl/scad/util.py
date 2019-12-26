from numbers import Number


def render(value):
    """Renders a value to OpenSCAD representation

    The following types are supported:
      * numbers.Number - rendered as literal
      * list and tuple - rendered recursively as vectors
      * model.Point - by virtue of being a (named)tuple

    Other types raise a ValueError.

    """

    if isinstance(value, Number):
        return f"{value}"
    elif isinstance(value, (list, tuple)):
        return f'[{", ".join(render(v) for v in value)}]'
    else:
        raise ValueError(f"Don't know how to render {value!r}")
