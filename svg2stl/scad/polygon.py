from svg2stl.scad import render


class Polygon:
    def __init__(self, polygon, points = None, paths = None):
        self._polygon = polygon

        self._points = points
        self._paths = paths

    def render_lines(self, depth = 0):
        if self._points:
            points = self._points
        else:
            points = render(self._polygon.points)

        if self._paths:
            paths = self._paths
        else:
            paths = map(render, self._polygon.paths)

        yield f"polygon (", depth
        yield f"{points},", depth + 1
        yield f"[", depth + 1
        for path in paths:
            yield f"{path},", depth + 2
        yield f"]", depth + 1
        yield f");", depth
