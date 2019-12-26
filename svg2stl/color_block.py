class ColorBlock:
    def __init__(self, color, target):
        self.color = color
        self.target = target

    def render_lines(self, depth = 0):
        yield f"color ({self.color.to_scad()}) {{", depth
        yield from self.target.render_lines(depth + 1)
        yield f"}}", depth
