from collections.__init__ import namedtuple


class Point(namedtuple("Point", ("x", "y"))):
    def to_scad(self):
        return f"[{self.x}, {self.y}]"