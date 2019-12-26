class Csg:
    def __init__(self, type, contents):
        self._type = type
        self._contents = contents

    def render_lines(self, depth = 0):
        yield f"{self._type} () {{", depth
        for content in self._contents:
            yield from content.render_lines(depth + 1)
        yield f"}}", depth

class Difference(Csg):
    def __init__(self, contents):
        super().__init__("difference", contents)