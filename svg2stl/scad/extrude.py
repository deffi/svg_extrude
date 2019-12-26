class Extrude:
    def __init__(self, thickness, target):
        self.thickness = thickness
        self.target = target

    def render_lines(self, depth = 0):
        yield f"linear_extrude ({self.thickness}) {{", depth
        yield from self.target.render_lines(depth + 1)
        yield f"}}", depth
