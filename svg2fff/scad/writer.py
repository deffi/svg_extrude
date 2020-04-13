from typing import Iterable, Iterator
from contextlib import contextmanager
from io import IOBase

from svg2fff.scad.util import Identifier
from svg2fff.scad.util import render


class Writer:
    def __init__(self, file: IOBase, *, indent: str = "    ", depth: int = 0):
        self._file: IOBase = file
        self._indent: str = indent
        self._depth: int = depth

    def print(self, *args) -> None:
        if len(args):
            print(self._indent * self._depth + str(args[0]), *args[1:], file=self._file)
        else:
            print(file=self._file)

    def blank_line(self) -> None:
        self.print()

    def comment(self, text: str) -> None:
        for line in text.splitlines():
            self.print(f"// {line}")

    def assignment(self, name: str, value) -> None:
        self.print(f"{name} = {render(value)};")

    def instance(self, name: str) -> None:
        self.print(f"{name} ();")

    def instances(self, names: Iterable[str]) -> None:
        for name in names:
            self.instance(name)

    @contextmanager
    def indented(self) -> Iterator[None]:
        self._depth += 1
        yield
        self._depth -= 1

    @contextmanager
    def block(self, statement: str) -> Iterator[None]:
        self.print(f"{statement} {{")
        with self.indented():
            yield
        self.print("}")

    @contextmanager
    def color(self, color) -> Iterator[None]:  # TODO type - depend on sfg2fff.model? If so, explicitly handle model classes in render() and use frozen dataclasses.
        # TODO not really an identifier
        with self.block(f"color (\"#{render(Identifier(color.html()))}\")"):
            yield

    @contextmanager
    def translate(self, vector) -> Iterator[None]:  # TODO class?
        with self.block(f"translate ({render(vector)})"):
            yield

    @contextmanager
    def extrude(self, thickness: float) -> Iterator[None]:
        with self.block(f"linear_extrude ({render(thickness)})"):
            yield

    @contextmanager
    def define_module(self, name: str) -> Iterator[None]:
        with self.block(f"module {name} ()"):
            yield

    @contextmanager
    def difference(self) -> Iterator[None]:
        with self.block(f"difference ()"):
            yield

    @contextmanager
    def union(self) -> Iterator[None]:
        with self.block("union ()"):
            yield

    @contextmanager
    def intersection(self) -> Iterator[None]:
        with self.block("intersection ()"):
            yield

    def polygon(self, polygon, points, paths) -> None:  # TODO types
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
