from svg2stl.scad import render

class Translate:
    def __init__(self, vector, target):
        self._vector = vector
        self._target = target

    def render_lines(self, depth = 0):
        yield f"translate ({render(self._vector)}) {{", depth
        yield from self._target.render_lines(depth + 1)
        yield f"}}", depth
