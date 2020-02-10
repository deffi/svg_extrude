from svg2fff.util import groupby

class Group:
    def __init__(self, name, color, shapes):
        self.name = name
        self.color = color
        self.shapes = shapes

    @classmethod
    def by_color(cls, shapes, *, colormap=lambda c: c):
        def create_group(color, group_shapes):
            return Group(f"group_{color.to_html()}", color, group_shapes)

        grouped = groupby(shapes, lambda shape: colormap(shape.color))
        return [create_group(color, shapes) for color, shapes in grouped.items()]
