from svg2stl.model import Polygon, Point
from svg2stl.util import filter_repetition
from svg2stl.css import extract_color


class Shape:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.polygon = Polygon()

    @classmethod
    def from_svg_path(cls, svg_path, precision):
        shape = Shape(svg_path.id, extract_color(svg_path))
        for subpath in svg_path.segments(precision):
            shape.polygon.add_subpolygon((Point(p.x, -p.y) for p in filter_repetition(subpath)))

        return shape

    def __repr__(self):
        return f"Shape({self.name})"

    def points_name(self):
        return f"{self.name}_points"

    def path_name(self, index):
        return f"{self.name}_path_{index}"

    def path_names(self):
        return (f"{self.name}_path_{index}" for index in range(len(self.polygon.paths)))

    def module_name(self):
        return self.name

    def module_only_name(self):
        return f"{self.name}_only"
