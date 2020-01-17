from svg2stl.scad import File as ScadFile
from svg2stl.util import with_remaining


class OutputFile:
    def __init__(self, file):
        self.file = file

    def write(self, shapes, groups, thickness):
        scad_file = ScadFile(self.file)

        # Define the points and paths for all shapes
        for shape in shapes:
            scad_file.assignment(shape.points_name(), shape.polygon.points)
            for index, path in enumerate(shape.polygon.paths):
                scad_file.assignment(shape.path_name(index), path)

        # Create modules for the individual shapes
        scad_file.blank_link()
        for index, shape in enumerate(shapes):
            with scad_file.define_module(shape.name):
                scad_file.polygon(shape.polygon, shape.points_name(), shape.path_names())

        # Create modules for the individual clipped shapes
        scad_file.blank_link()
        for shape, remaining in with_remaining(shapes):
            with scad_file.define_module(shape.module_only_name()):
                with scad_file.difference():
                    scad_file.instance(shape.name)
                    scad_file.instances(s.name for s in remaining)

        # Create modules for the individual color groups
        scad_file.blank_link()
        for group in groups:
            with scad_file.define_module(group.name):
                # Implicit union
                for shape in group.shapes:
                    scad_file.instance(shape.module_only_name())

        # Instantiate the groups with their respective color
        scad_file.blank_link()
        for index, group in enumerate(groups):
            with scad_file.color(group.color):
                # with scad_file.translate([0, 0, 0 * index]):
                with scad_file.extrude(thickness):
                    scad_file.instance(group.name)
