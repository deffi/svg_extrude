from svg2stl import Point, Color


class Polygon:
    def __init__(self, color = None):
        self._points = list()
        self._paths = list()
        self.color = color
        self.thickness = 0
        self.offset = 0

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

    def to_scad(self):
        def path_string(path):
            return ", ".join(f"{index}" for index in path)

        points_string = ", ".join(p.to_scad() for p in self._point_indices)

        if self.color is None:
            color_string = ""
        else:
            color_string = f"color([{self.color.r}, {self.color.g}, {self.color.b}]) "

        if self.offset:
            offset_string = f"translate([0, 0, {self.offset}]) "
        else:
            offset_string = ""

        extrude_string = f"linear_extrude({self.thickness}) "

        lines = list()

        # paths_string = "\n".join(f"[    {path_string}]" for path_string in path_strings)
        lines.append(f"{color_string}{offset_string}{extrude_string}polygon(")
        lines.append(f"    [{points_string}],")
        lines.append(f"    [")
        lines.append(",\n".join(f"     [{path_string(path)}]" for path in self._paths))
        lines.append(f"    ]")
        # lines.append(f"    [{paths_string}]]")
        lines.append(f");")
        return "\n".join(lines)


if __name__ == "__main__":
    p = Polygon()
    p.color = Color.random_hsv(s=1, v=1)
    p.add_subpolygon(((0, 0), (40, 0), (40, 30)))
    p.add_subpolygon(((0, 0), (30, 5), (30, 35)))

    with open("testdata/output.scad", "w") as file:
        print(p.to_scad(), file=file)
