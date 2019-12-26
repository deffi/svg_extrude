from svg2stl.scad import Line


class Instance(Line):
    def __init__(self, name):
        super().__init__(f"{name} ();")
