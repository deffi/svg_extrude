from typing import List
from io import IOBase

from svg2fff.model import Shape, Group
from svg2fff.scad import File as ScadFile, reserved_words
from svg2fff.scad.util import identifier_part
from svg2fff.util import with_remaining, Namespace

# Invalid characters in IDs are replaced with underscores.
# ID collisions and collisions with reserved words are resolved by appending a
# number (separated by underscore).
# We could also have escaped invalid characters (and the escape character
# itself), and appended an underscore to reserved words. We might even keep
# underscores as long as they don't cause collisions.

class ShapeNames:
    def __init__(self, name: str, path_count: int):
        self.points = f"points_{name}"
        self.paths = [f"path_{name}_{index}" for index in range(path_count)]
        self.shape = f"shape_{name}"
        self.clipped_shape = f"clipped_{name}"

class GroupNames:
    def __init__(self, name: str):
        self.group = f"group_{name}"


class OutputFile:
    def __init__(self, file: IOBase):
        self.scad_file = ScadFile(file)
        self._namespace = Namespace(identifier_part, reserved_words)
        self._shape_names = dict()
        self._group_names = dict()

    # TODO clean up mechanism
    def shape_names(self, shape: Shape) -> ShapeNames:
        key = id(shape)
        if key not in self._shape_names:
            name = self._namespace.get(shape.name)
            path_count = len(shape.polygon.paths)
            self._shape_names[key] = ShapeNames(name, path_count)

        return self._shape_names[key]

    def group_names(self, group: Group) -> GroupNames:
        key = id(group)
        if key not in self._group_names:
            name = self._namespace.get(group.color.display_name())
            self._group_names[key] = GroupNames(name)

        return self._group_names[key]

    def write_points_and_paths(self, shapes: List[Shape]):
        self.scad_file.blank_line()
        self.scad_file.comment("Points and paths for each shape")

        for shape in shapes:
            self.scad_file.assignment(self.shape_names(shape).points, shape.polygon.points)
            for index, path in enumerate(shape.polygon.paths):
                self.scad_file.assignment(self.shape_names(shape).paths[index], path)

    def write_shapes(self, shapes: List[Shape]):
        self.scad_file.blank_line()
        self.scad_file.comment("Shapes")

        for index, shape in enumerate(shapes):
            self.scad_file.comment(f"{shape.name}")
            names = self.shape_names(shape)
            with self.scad_file.define_module(names.shape):
                self.scad_file.polygon(shape.polygon, names.points, names.paths)

    def write_clipped_shapes(self, shapes: List[Shape]):
        self.scad_file.blank_line()
        self.scad_file.comment("Clipped shapes")

        for shape, remaining in with_remaining(shapes):
            names = self.shape_names(shape)
            with self.scad_file.define_module(names.clipped_shape):
                with self.scad_file.difference():
                    self.scad_file.instance(names.shape)
                    self.scad_file.instances(self.shape_names(s).shape for s in remaining)

    def write_groups(self, groups: List[Group]):
        self.scad_file.blank_line()
        self.scad_file.comment("Groups")

        for group in groups:
            with self.scad_file.define_module(self.group_names(group).group):
                # Implicit union
                for shape in group.shapes:
                    shape_names = self.shape_names(shape)
                    self.scad_file.instance(shape_names.clipped_shape)

    def instantiate_groups(self, groups: List[Group], thickness: float):
        self.scad_file.blank_line()
        self.scad_file.comment("Extrude groups")

        for index, group in enumerate(groups):
            with self.scad_file.color(group.color):
                with self.scad_file.extrude(thickness):
                    self.scad_file.instance(self.group_names(group).group)

    def write(self, shapes: List[Shape], groups: List[Group], thickness: float) -> None:
        self.scad_file.comment("Written by svg2fff")
        self.write_points_and_paths(shapes)
        self.write_shapes(shapes)
        self.write_clipped_shapes(shapes)
        self.write_groups(groups)
        self.instantiate_groups(groups, thickness)
