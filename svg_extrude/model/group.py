from dataclasses import dataclass
from typing import Iterable, Tuple, Generator

from svg_extrude.model import Color, Shape
from svg_extrude.util import group_by, identity


@dataclass(frozen=True)
class Group:
    color: Color
    shapes: Tuple[Shape, ...]

    @classmethod
    def by_color(cls, shapes: Iterable[Shape], *, color_mapping=None) -> Generator["Group", None, None]:
        def create_group(color: Color, group_shapes: Iterable[Shape]):
            return Group(color, tuple(group_shapes))

        if color_mapping is None:
            color_mapping = identity

        grouped = group_by(shapes, lambda shape: color_mapping(shape.color))
        return (create_group(color, shapes) for color, shapes in grouped.items())
