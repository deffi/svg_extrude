from dataclasses import dataclass
from typing import List, Tuple

from svg2fff.model import Color, Shape
from svg2fff.util import group_by


@dataclass(frozen=True)
class Group:
    color: Color
    shapes: Tuple[Shape]

    @classmethod
    def by_color(cls, shapes: List[Shape], *, color_mapping=lambda c: c) -> List["Group"]:
        def create_group(color: Color, group_shapes: List[Shape]):
            return Group(color, tuple(group_shapes))

        grouped = group_by(shapes, lambda shape: color_mapping(shape.color))
        return [create_group(color, shapes) for color, shapes in grouped.items()]
