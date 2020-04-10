from typing import Generator

from svg2fff.model import Polygon, Point, Color
from svg2fff.util import filter_repetition
from svg2fff.css import extract_color


class Shape:
    def __init__(self, name: str, color: Color):
        self.name: str = name
        self.color: Color = color
        self.polygon: Polygon = Polygon()

    @classmethod
    def from_svg_path(cls, svg_path, precision: float) -> "Shape":
        shape = Shape(svg_path.id, extract_color(svg_path))
        for subpath in svg_path.segments(precision):
            shape.polygon.add_subpolygon((Point(p.x, -p.y) for p in filter_repetition(subpath)))

        return shape

    def __repr__(self):
        return f"Shape({self.name})"

    def points_name(self) -> str:
        return f"{self.name}_points"

    def path_name(self, index: int) -> str:
        return f"{self.name}_path_{index}"

    def path_names(self) -> Generator[str]:
        return (f"{self.name}_path_{index}" for index in range(len(self.polygon.paths)))

    def module_name(self) -> str:
        return self.name

    def module_only_name(self) -> str:
        return f"{self.name}_only"
