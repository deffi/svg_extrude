from svg2stl.scad import Line, render


class Assignment(Line):
    def __init__(self, name, value):
        super().__init__(f"{name} = {render(value)};")
