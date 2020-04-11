from typing import List
from dataclasses import dataclass

from svg2fff.model import Shape, Group

import cjlano_svg as svg


@dataclass()
class Scene:
    """Contains a list of shapes and a list of groups.

    The list of shapes is ordered from back to front; i. e., shapes are clipped
    by shapes that appear later in the list.

    The groups contain references to shapes.
    """

    shapes: List[Shape]
    groups: List[Group]

    @classmethod
    def from_svg(cls, file_name: str, precision: float):
        # Read the SVG file
        svg_picture: svg.Svg = svg.parse(file_name)

        # Extract paths, disregard SVG groups. The paths are in the order as
        # defined in the SVG file. According to the SVG specification (version
        # 1.1, section 3.3), this is the order from back to front.
        # https://www.w3.org/TR/SVG11/render.html#RenderingOrder
        svg_paths = svg_picture.flatten()

        # Create the shapes
        shapes = [Shape.from_svg_path(path, precision) for path in svg_paths]

        # Group the shapes by color
        groups = Group.by_color(shapes)
        # groups = Group.by_color(shapes, colormap=lambda color: color.closest_hsv(available_colors)) # TODO

        return cls(shapes=shapes, groups=groups)
