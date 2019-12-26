from contextlib import contextmanager

from svg2stl.scad import render
from svg2stl.util import render_lines


class File:
    def __init__(self, file, *, indent="    ", depth=0):
        self._file = file
        self._indent = indent
        self._depth = depth

    def indent(self):
        return File(self._file, indent=self._indent, depth=self._depth + 1)

    def print(self, *args):
        print(self._indent * self._depth + str(args[0]), *args[1:], file=self._file)

    def output(self, target):
        for line, depth in target.render_lines():
            self.print(self._indent * depth + line)

    def assignment(self, name, value):
        self.print(f"{name} = {render(value)};")

    @contextmanager
    def color(self, color):
        self.print(f"color ({render(color.rgb())}) {{")
        yield self.indent()
        self.print("}")
