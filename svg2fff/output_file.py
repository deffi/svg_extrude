from typing import List
from io import IOBase
from itertools import count

from svg2fff.model import Shape, Group
from svg2fff.util import factorydict
from svg2fff.scad import File as ScadFile
from svg2fff.scad.util import identifier_part
from svg2fff.util import with_remaining

# Invalid characters in IDs are replaced with underscores.
# ID collisions and collisions with reserved words are resolved by appending a
# number (separated by underscore).
# We could also have escaped invalid characters (and the escape character
# itself), and appended an underscore to reserved words. We might even keep
# underscores as long as they don't cause collisions.

class ShapeNames:
    def __init__(self, name: str, path_count: int):
        self.points = f"{name}_points"
        self.paths = [f"{name}_path_{index}" for index in range(path_count)]
        self.shape = f"{name}"  # TODO potential collision
        self.clipped_shape = f"{name}_clipped"


class GroupNames:
    def __init__(self, name: str):
        self.group = f"group_{name}"  # TODO potential collision with shapes


# TODO factor out
class Namespace:
    def __init__(self):
        self._map = factorydict(self.build)
        # Builtins::init and Builtins::keywordList.insert
        self._reserved = {
            "abs", "acos", "asin", "assert", "assign", "atan", "atan2", "ceil", "child", "children",
            "chr", "circle", "color", "concat", "cos", "cross", "cube", "cylinder", "difference",
            "dxf_cross", "dxf_dim", "dxf_linear_extrude", "dxf_rotate_extrude", "each", "echo",
            "else", "exp", "false", "floor", "for", "function", "group", "hull", "if", "import",
            "import_dxf", "import_off", "import_stl", "include", "intersection", "intersection_for",
            "is_bool", "is_function", "is_list", "is_num", "is_string", "is_undef", "len", "let",
            "linear_extrude", "ln", "log", "lookup", "max", "min", "minkowski", "mirror", "module",
            "multmatrix", "norm", "offset", "ord", "parent_module", "polygon", "polyhedron", "pow",
            "projection", "rands", "render", "resize", "rotate", "rotate_extrude", "round", "scale",
            "search", "sign", "sin", "sphere", "sqrt", "square", "str", "surface", "tan", "text",
            "translate", "true", "undef", "union", "use", "version", "version_num" }

    def get(self, name: str) -> str:
        return self._map[name]

    def build(self, name: str) -> str:
        def candidates():
            identifier = identifier_part(name)
            yield identifier
            for i in count(1):
                yield f"{identifier}_{i}"

        existing = set(self._map.values())
        for candidate in candidates():
            if candidate not in self._reserved and candidate not in existing:
                return candidate


class OutputFile:
    def __init__(self, file: IOBase):
        self.scad_file = ScadFile(file)
        self._namespace = Namespace()
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
