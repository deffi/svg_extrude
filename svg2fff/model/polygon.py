from dataclasses import dataclass, field
from typing import List, Dict, Iterable

from svg2fff.model import Point


@dataclass()
class Polygon:
    _points: List[Point] = field(default_factory=list)
    _paths: List[List[int]] = field(default_factory=list)
    _point_indices: Dict[Point, int] = field(default_factory=dict)

    def _point_index(self, point: Point) -> int:
        # If we haven't seen the point yet, add it to the list
        if point not in self._point_indices:
            self._point_indices[point] = len(self._points)
            self._points.append(point)

        return self._point_indices[point]

    @staticmethod
    def _import_point(point) -> Point:
        if isinstance(point, tuple):
            return Point(*point)
        else:
            return Point(point.x, point.y)

    def add_subpolygon(self, points: Iterable[Point]) -> None:
        points = map(self._import_point, points)
        index_list: List[int] = [self._point_index(p) for p in points]
        self._paths.append(index_list)

    @property
    def points(self) -> List[Point]:
        return self._points

    @property
    def paths(self) -> List[List[int]]:
        return self._paths
