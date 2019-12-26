from svg2stl.util import render_lines

class File:
    def __init__(self, file):
        self._file = file

    @staticmethod
    def render(target):
        return render_lines(target.render_lines(), "", "    ")

    def output(self, target):
        print(self.render(target), file=self._file)
