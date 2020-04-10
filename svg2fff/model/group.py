from typing import List

from svg2fff.model import Color, Shape
from svg2fff.util import groupby

class Group:
    def __init__(self, name: str, color: Color, shapes: List[Shape]):
        self.name: str = name
        self.color: Color = color
        self.shapes: List[Shape] = shapes

    @classmethod
    def by_color(cls, shapes: List[Shape], *, colormap=lambda c: c) -> List["Group"]:
        def create_group(color: Color, group_shapes: List[Shape]):
            return Group(f"group_{color.to_html()}", color, group_shapes)

        grouped = groupby(shapes, lambda shape: colormap(shape.color))
        return [create_group(color, shapes) for color, shapes in grouped.items()]
