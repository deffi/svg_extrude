import logging
from dataclasses import dataclass
from typing import Tuple, Optional

from libs import cjlano_svg

from svg_extrude.model import Polygon, Point, Color
from svg_extrude.util import filter_repetition
from svg_extrude.css import extract_value

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Shape:
    name: str
    color: Color
    polygon: Polygon

    @classmethod
    def from_svg_path(cls, svg_path: cjlano_svg.Path, precision: float, *, snap: Optional[float] = None) -> "Shape":
        fill_rule = extract_value(svg_path.style, "fill-rule")
        if not (fill_rule is None or fill_rule == "evenodd"):
            logger.warning("%s: fill rule %s not supported. Using evenodd instead.", svg_path.id, fill_rule)

        stroke = extract_value(svg_path.style, "stroke")
        if not (stroke is None or stroke == "none"):
            logger.warning("%s: stroked paths are not supported. Ignoring stroke.", svg_path.id)

        # If there is no style or no fill property, use black (SVG 1.1, section
        # 11.3). We can't use the fill attribute because cjlano_svg doesn't
        # provide access to arbitrary attributes.
        fill = extract_value(svg_path.style, "fill") or "#000000"
        if fill:
            fill = Color.from_html(fill, None)

        # 1 px (1/96 inch) in m
        px = 25.4e-3 / 96

        def length(v: float) -> float:
            v = v * px
            if snap:
                v = snap * round(v / snap)
            return v

        def point(svg_point) -> Point:
            x = length(svg_point.x)
            y = length(svg_point.y)
            return Point(x, y)

        def path(segment) -> Tuple[Point]:
            return tuple(point(p) for p in filter_repetition(segment))
        segments = svg_path.segments(precision)
        paths = (path(segment) for segment in segments)
        polygon = Polygon(tuple(paths))

        return Shape(svg_path.id, fill, polygon)
