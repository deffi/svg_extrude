from dataclasses import dataclass
from typing import Tuple

from svg2fff.model import Point


@dataclass(frozen=True)
class Polygon:
    paths: Tuple[Tuple[Point, ...], ...]

    def index_paths(self):
        """Returns points, index_paths"""
        points = list()
        point_indices = dict()

        # Collect all of the points
        for path in self.paths:
            for point in path:
                if point not in points:
                    point_indices[point] = len(points)
                    points.append(point)

        # Build the index paths
        index_paths = []
        for path in self.paths:
            index_path = [point_indices[point] for point in path]
            index_paths.append(index_path)

        return points, index_paths
