from dataclasses import dataclass
from typing import Iterable, Tuple, Generator

from svg2fff.model import Color, Shape
from svg2fff.util import group_by


@dataclass(frozen=True)
class Group:
    color: Color
    shapes: Tuple[Shape, ...]

    @classmethod
    def by_color(cls, shapes: Iterable[Shape], *, color_mapping=lambda c: c) -> Generator["Group", None, None]:
        def create_group(color: Color, group_shapes: Iterable[Shape]):
            return Group(color, tuple(group_shapes))

        grouped = group_by(shapes, lambda shape: color_mapping(shape.color))
        return (create_group(color, shapes) for color, shapes in grouped.items())
