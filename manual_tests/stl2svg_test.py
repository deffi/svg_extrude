from os import path

import cjlano_svg as svg

from svg2stl.model import Shape, Group, Color
from svg2stl.scad import File as ScadFile
from svg2stl.util import with_remaining, groupby

px = 25.4 / 96

datapath = path.join("..", "testdata")
outputpath = path.join(datapath, "output")
svg_file_name = path.join(datapath, "test2.svg")
scad_file_name = path.join(outputpath, "output.scad")

svg_picture = svg.parse(svg_file_name)
svg_paths = svg_picture.flatten()

precision=1
thickness=1

available_colors = [Color.from_hsv(i/6, 1, 1) for i in range(6)]


# Create the shapes
shapes = [Shape.from_svg_path(path, precision) for path in svg_paths]

# Group the shapes by color
# groups = Group.by_color(shapes, colormap=lambda color: color.closest_hsv(available_colors))
groups = Group.by_color(shapes)

print(f"Writing to {scad_file_name}")
with open(scad_file_name, "w") as file:
    scad_file = ScadFile(file)

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
            with scad_file.translate([0, 0, 0*index]):
                with scad_file.extrude(thickness):
                    scad_file.instance(group.name)
