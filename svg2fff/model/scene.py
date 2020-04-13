from typing import List, Optional
from dataclasses import dataclass

from svg2fff.model import Shape, Group, ColorSet
from svg2fff.util import identity

import cjlano_svg as svg


@dataclass()
class Scene:
    """Contains a list of shapes and a list of groups.

    The list of shapes is ordered from back to front; i. e., shapes are clipped
    by shapes that appear later in the list.

    A group can contain shapes that are not adjacent in the Z order. For
    example, the list of shapes might be [A, B, C], with group 1 [A, C] and
    group 2 [B]. In this case, shape B will clip shape A, but will be clipped by
    shape C.
    """

    shapes: List[Shape]
    groups: List[Group]

    @classmethod
    def from_svg(cls, file_name: str, *, precision: float, available_colors: Optional[ColorSet]):
        # Read the SVG file
        svg_picture: svg.Svg = svg.parse(file_name)

        # Extract paths, disregard SVG groups. The paths are in the order as
        # defined in the SVG file. According to the SVG specification (version
        # 1.1, section 3.3), this is the order from back to front.
        # https://www.w3.org/TR/SVG11/render.html#RenderingOrder
        svg_paths = svg_picture.flatten()

        # Create the shapes
        shapes = [Shape.from_svg_path(path, precision) for path in svg_paths]

        # Create the color mapping
        if available_colors:
            color_mapping = available_colors.closest
        else:
            color_mapping = identity

        # Group the shapes by color
        groups = Group.by_color(shapes, color_mapping=color_mapping)

        return cls(shapes=shapes, groups=groups)
