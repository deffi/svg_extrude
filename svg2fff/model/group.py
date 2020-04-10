from dataclasses import dataclass
from typing import List

from svg2fff.model import Color, Shape
from svg2fff.util import groupby

@dataclass()
class Group:
    name: str
    color: Color
    shapes: List[Shape]

    @classmethod
    def by_color(cls, shapes: List[Shape], *, colormap=lambda c: c) -> List["Group"]:
        def create_group(color: Color, group_shapes: List[Shape]):
            return Group(f"group_{color.to_html()}", color, group_shapes)

        grouped = groupby(shapes, lambda shape: colormap(shape.color))
        return [create_group(color, shapes) for color, shapes in grouped.items()]
