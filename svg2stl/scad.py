from contextlib import contextmanager
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
    elif isinstance(value, str):
        # TODO do we need an Identifier class? A Text class with escaping?
        return value
    else:
        raise ValueError(f"Don't know how to render {value!r}")


class File:
    def __init__(self, file, *, indent="    ", depth=0):
        self._file = file
        self._indent = indent
        self._depth = depth

    def print(self, *args):
        if len(args):
            print(self._indent * self._depth + str(args[0]), *args[1:], file=self._file)
        else:
            print(file=self._file)

    @contextmanager
    def indented(self):
        self._depth += 1
        yield
        self._depth -= 1

    def blank_link(self):
        self.print()

    def assignment(self, name, value):
        self.print(f"{name} = {render(value)};")

    def instance(self, name):
        self.print(f"{name} ();")

    def instances(self, names):
        for name in names:
            self.instance(name)

    @contextmanager
    def color(self, color):
        self.print(f"color ({render(color.rgb())}) {{")
        with self.indented():
            yield
        self.print("}")

    @contextmanager
    def translate(self, vector):
        self.print(f"translate ({render(vector)}) {{")
        with self.indented():
            yield
        self.print("}")

    @contextmanager
    def extrude(self, thickness):
        self.print(f"linear_extrude ({render(thickness)}) {{")
        with self.indented():
            yield
        self.print("}")

    @contextmanager
    def define_module(self, name):
        self.print(f"module {name} () {{")
        with self.indented():
            yield
        self.print("}")

    @contextmanager
    def csg(self, type):
        self.print(f"{type} () {{")
        with self.indented():
            yield
        self.print("}")

    @contextmanager
    def difference(self):
        with self.csg("difference"):
            yield

    def polygon(self, polygon, points, paths):
        points = points or render(polygon.points)
        short_paths = (paths is not None)
        paths = paths or list(map(render, polygon.paths))

        if short_paths:
            self.print(f"polygon ({points}, {render(list(paths))});")
        else:
            self.print(f"polygon ({points}, [")
            with self.indented():
                for path in paths:
                    self.print(f"{render(path)},")
            self.print("]);")
