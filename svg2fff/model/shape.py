import logging
from dataclasses import dataclass, field
from typing import Iterable

from svg2fff.model import Polygon, Point, Color
from svg2fff.util import filter_repetition
from svg2fff.css import extract_color, extract_fill_rule, extract_stroke

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Shape:
    name: str
    color: Color
    polygon: Polygon = field(default_factory=Polygon)

    @classmethod
    def from_svg_path(cls, svg_path, precision: float) -> "Shape":
        fill_rule = extract_fill_rule(svg_path)
        if not (fill_rule is None or fill_rule == "evenodd"):
            logger.warning("%s: fill rule %s not supported. Using evenodd instead.", svg_path.id, fill_rule)

        stroke = extract_stroke(svg_path)
        if not (stroke is None or stroke == "none"):
            logger.warning("%s: stroked paths are not supported. Ignoring stroke.", svg_path.id)

        shape = Shape(svg_path.id, extract_color(svg_path))
        for subpath in svg_path.segments(precision):
            # 1 px is 1/96 inch; we use mm
            # TODO use m, but we need to convert it to mm when writing the SCAD file.
            px = 25.4/96
            shape.polygon.add_subpolygon((Point(p.x*px, p.y*px) for p in filter_repetition(subpath)))

        return shape

    def __repr__(self):
        return f"Shape({self.name})"
