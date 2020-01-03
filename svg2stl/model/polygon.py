from svg2stl.model import Point


class Polygon:
    def __init__(self):
        self._points = list()
        self._paths = list()
        self._point_indices = dict()

    def _point_index(self, point):
        # If we haven't seen the point yet, add it to the list
        if point not in self._point_indices:
            self._point_indices[point] = len(self._points)
            self._points.append(point)

        return self._point_indices[point]

    @staticmethod
    def _import_point(point):
        if isinstance(point, tuple):
            return Point(*point)
        else:
            return Point(point.x, point.y)

    def add_subpolygon(self, points):
        points = map(self._import_point, points)
        index_list = [self._point_index(p) for p in points]
        self._paths.append(index_list)

    @property
    def points(self):
        return self._points

    @property
    def paths(self):
        return self._paths
