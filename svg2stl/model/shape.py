from svg2stl.model import Polygon


class Shape:
    def __init__(self, name):
        self.name = name
        self.color = None
        self.polygon = Polygon()

    def __repr__(self):
        return f"Shape({self.name})"
