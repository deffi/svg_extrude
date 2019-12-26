class Line:
    def __init__(self, code):
        self._code = code

    def render_lines(self, depth=0):
        yield self._code, depth