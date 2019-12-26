import cjlano_svg as svg
from os import path

from svg2stl.model import Polygon, Point
import svg2stl.scad as s
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

# Create the polygons
polygons=list()
for index, path in enumerate(svg_paths):
    polygon = Polygon(path.id)
    # TODO color should not be part of the polygon - create a shape class that
    # has the object names, the color, the polygon
    polygon.color = extract_color(path)
    for subpath in path.segments(precision):
        polygon.add_subpolygon((Point(p.x, -p.y) for p in filter_repetition(subpath)))
    polygons.append(polygon)




with open(scad_file_name, "w") as file:
    scad_file = s.File(file)

    for polygon in polygons:
        points_name = f"{polygon.name}_points"
        scad_file.assignment(points_name, polygon.points)

        for index, path in enumerate(polygon.paths):
            path_name = f"{polygon.name}_path_{index}"
            scad_file.assignment(path_name, path)

    print(file=file)
    for index, polygon in enumerate(polygons):
        points_name = f"{polygon.name}_points"
        path_names = (f"{polygon.name}_path_{index}" for index, path in enumerate(polygon.paths))
        poly = s.Polygon(polygon, points_name, path_names)
        with scad_file.module(polygon.name):
            scad_file.output(poly)

    print(file=file)
    for index in range(len(polygons)):
        difference = s.Difference((s.Instance(p.name) for p in polygons[index:]))
        name = f"{polygons[index].name}_only"
        # module = s.Module(name, [difference])
        #scad_file.output(module)
        with scad_file.module(name):
            scad_file.output(difference)

    print(file=file)
    for index, polygon in enumerate(polygons):
        with scad_file.color(polygon.color):
            with scad_file.translate((0, 0, index * thickness)):
                with scad_file.extrude(thickness):
                    scad_file.instance(f"{polygon.name}_only")
