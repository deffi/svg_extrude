from typing import Iterable, Iterator, TextIO
from contextlib import contextmanager

from svg2fff.model import Color
from svg2fff.scad.util import Identifier
from svg2fff.scad.util import render


class Writer:
    def __init__(self, file: TextIO, *, indent: str = "    ", depth: int = 0):
        self._file: TextIO = file
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

    def assignment(self, name: Identifier, value) -> None:
        self.print(f"{render(name)} = {render(value)};")

    def instance(self, name: Identifier) -> None:
        self.print(f"{render(name)} ();")

    def instances(self, names: Iterable[Identifier]) -> None:
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
    def color(self, color: Color) -> Iterator[None]:
        with self.block(f"color ({render(color)})"):
            yield

    @contextmanager
    def translate(self, vector: Iterable[float]) -> Iterator[None]:
        with self.block(f"translate ({render(vector)})"):
            yield

    @contextmanager
    def extrude(self, thickness: float) -> Iterator[None]:
        with self.block(f"linear_extrude ({render(thickness)})"):
            yield

    @contextmanager
    def define_module(self, name: Identifier) -> Iterator[None]:
        with self.block(f"module {render(name)} ()"):
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

    def polygon(self, points: Identifier, index_paths: Iterable[Identifier], *, short: bool) -> None:
        if short:
            self.print(f"polygon ({render(points)}, {render(index_paths)});")
        else:
            self.print(f"polygon ({render(points)}, [")
            with self.indented():
                for index_path in index_paths:
                    self.print(f"{render(index_path)},")
            self.print("]);")
