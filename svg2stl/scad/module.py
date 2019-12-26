class Module:
    def __init__(self, name, contents):
        self._name = name
        self._contents = contents

    def render_lines(self, depth = 0):
        yield f"module {self._name} () {{", depth
        for content in self._contents:
            yield from content.render_lines(depth + 1)
        yield f"}}", depth
