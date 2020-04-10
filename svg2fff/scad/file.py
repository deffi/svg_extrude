from contextlib import contextmanager
from tempfile import mkstemp
import os
import subprocess

from svg2fff.scad.util import Identifier
from svg2fff.scad.util import render


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
        # TODO not really an identifier
        self.print(f"color (\"#{render(Identifier(color.to_html()))}\") {{")
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

    @contextmanager
    def union(self):
        with self.csg("union"):
            yield

    @contextmanager
    def intersection(self):
        with self.csg("intersection"):
            yield

    def polygon(self, polygon, points, paths):
        points = points or render(polygon.points)
        short_paths = (paths is not None)
        paths = paths or list(map(render, polygon.paths))

        if short_paths:
            self.print(f"polygon ({points}, {render(list(map(Identifier, paths)))});")
        else:
            self.print(f"polygon ({points}, [")
            with self.indented():
                for path in paths:
                    self.print(f"{render(path)},")
            self.print("]);")


@contextmanager
def render_file(output_file_name):
    # Create a temporary file
    handle, path = mkstemp(suffix=".scad")

    try:
        with os.fdopen(handle, "w") as scad_file:
            yield scad_file

        # Call OpenSCAD
        command = ["openscad", "-o", output_file_name, path]
        subprocess.run(command, capture_output=True, check=True)
    finally:
        os.remove(path)
