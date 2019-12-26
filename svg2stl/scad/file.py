from contextlib import contextmanager

from svg2stl.scad import render


class File:
    def __init__(self, file, *, indent="    ", depth=0):
        self._file = file
        self._indent = indent
        self._depth = depth

    def print(self, *args):
        print(self._indent * self._depth + str(args[0]), *args[1:], file=self._file)

    # TODO remove when no longer needed
    def output(self, target):
        for line, depth in target.render_lines():
            self.print(self._indent * depth + line)

    @contextmanager
    def indented(self):
        self._depth += 1
        yield
        self._depth -= 1

    def assignment(self, name, value):
        self.print(f"{name} = {render(value)};")

    def instance(self, name):
        self.print(f"{name} ();")

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
    def module(self, name):
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

