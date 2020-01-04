import cjlano_svg as svg
from os import path

from svg2stl.model import Shape
from svg2stl.scad import File as ScadFile

px = 25.4 / 96

datapath = path.join("..", "testdata")
outputpath = path.join(datapath, "output")
svg_file_name = path.join(datapath, "test2.svg")
scad_file_name = path.join(outputpath, "output.scad")

svg_picture = svg.parse(svg_file_name)
svg_paths = svg_picture.flatten()

precision=1
thickness=1


# Create the shapes
shapes = [Shape.from_svg_path(path, precision) for path in svg_paths]

print(f"Writing to {scad_file_name}")
with open(scad_file_name, "w") as file:
    scad_file = ScadFile(file)

    for shape in shapes:
        scad_file.assignment(shape.points_name(), shape.polygon.points)
        for index, path in enumerate(shape.polygon.paths):
            scad_file.assignment(shape.path_name(index), path)

    scad_file.blank_link()
    for index, shape in enumerate(shapes):
        with scad_file.module(shape.name):
            scad_file.polygon(shape.polygon, shape.points_name(), shape.path_names())

    scad_file.blank_link()
    for index in range(len(shapes)):
        with scad_file.module(shapes[index].module_only_name()):
            with scad_file.difference():
                for s in shapes[index:]:
                    scad_file.instance(s.name)

    scad_file.blank_link()
    for index, shape in enumerate(shapes):
        with scad_file.color(shape.color):
            with scad_file.translate((0, 0, index * thickness)):
                with scad_file.extrude(thickness):
                    scad_file.instance(shape.module_only_name())
