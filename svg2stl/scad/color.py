from svg2stl.scad.util import render

class Color:
    def __init__(self, color, target):
        self.color = color
        self.target = target

    def render_lines(self, depth = 0):
        yield f"color ({render(self.color.rgb())}) {{", depth
        yield from self.target.render_lines(depth + 1)
        yield f"}}", depth
