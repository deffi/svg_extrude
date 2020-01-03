import cjlano_svg as svg
from os import path

from svg2stl.model import Shape, Point
from svg2stl.scad import File as ScadFile
from svg2stl.util import filter_repetition
from svg2stl.css import extract_color

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
shapes=list()
for index, path in enumerate(svg_paths):
    shape = Shape(path.id)
    shape.color = extract_color(path)
    for subpath in path.segments(precision):
        shape.polygon.add_subpolygon((Point(p.x, -p.y) for p in filter_repetition(subpath)))
    shapes.append(shape)

print(f"Writing to {scad_file_name}")
with open(scad_file_name, "w") as file:
    scad_file = ScadFile(file)

    for shape in shapes:
        points_name = f"{shape.name}_points"
        scad_file.assignment(points_name, shape.polygon.points)

        for index, path in enumerate(shape.polygon.paths):
            path_name = f"{shape.name}_path_{index}"
            scad_file.assignment(path_name, path)

    print(file=file)
    for index, shape in enumerate(shapes):
        points_name = f"{shape.name}_points"
        path_names = (f"{shape.name}_path_{index}" for index, path in enumerate(shape.polygon.paths))
        with scad_file.module(shape.name):
            scad_file.polygon(shape.polygon, points_name, path_names)

    print(file=file)
    for index in range(len(shapes)):
        with scad_file.module(f"{shapes[index].name}_only"):
            with scad_file.difference():
                for s in shapes[index:]:
                    scad_file.instance(s.name)

    print(file=file)
    for index, shape in enumerate(shapes):
        with scad_file.color(shape.color):
            with scad_file.translate((0, 0, index * thickness)):
                with scad_file.extrude(thickness):
                    scad_file.instance(f"{shape.name}_only")
