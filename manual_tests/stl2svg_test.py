from os import path

import cjlano_svg as svg

from svg2stl.model import Shape
from svg2stl.scad import File as ScadFile
from svg2stl.util import with_remaining, groupby

px = 25.4 / 96

datapath = path.join("..", "testdata")
outputpath = path.join(datapath, "output")
svg_file_name = path.join(datapath, "test3.svg")
scad_file_name = path.join(outputpath, "output.scad")

svg_picture = svg.parse(svg_file_name)
svg_paths = svg_picture.flatten()

precision=1
thickness=1


# Create the shapes
shapes = [Shape.from_svg_path(path, precision) for path in svg_paths]

# Group the shapes by color
groups = groupby(shapes, lambda shape: shape.color)

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

    # Create the groups with their respective color, instantiating all shapes
    scad_file.blank_link()
    for color, shapes in groups.items():
        with scad_file.color(color):
            with scad_file.extrude(thickness):
                with scad_file.union():
                    for shape in shapes:
                        scad_file.instance(shape.module_only_name())
