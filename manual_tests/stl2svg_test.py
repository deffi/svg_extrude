import cjlano_svg as svg
from os import path

from svg2stl.model import Polygon, Point, Color
import svg2stl.scad as s
from svg2stl.util import filter_repetition, render_lines

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
    for subpath in path.segments(precision):
        polygon.add_subpolygon((Point(p.x, -p.y) for p in filter_repetition(subpath)))
    polygons.append(polygon)


def render(target):
    return render_lines(target.render_lines(), "", "    ")


with open(scad_file_name, "w") as file:
    for polygon in polygons:
        points_name = f"{polygon.name}_points"
        print(render(s.Assignment(points_name, polygon.points)), file=file)

        for index, path in enumerate(polygon.paths):
            path_name = f"{polygon.name}_path_{index}"
            print(render(s.Assignment(path_name, path)), file=file)

    print(file=file)
    for index, polygon in enumerate(polygons):
        points_name = f"{polygon.name}_points"
        path_names = (f"{polygon.name}_path_{index}" for index, path in enumerate(polygon.paths))
        poly = s.Polygon(polygon, points_name, path_names)
        module = s.Module(polygon.name, [poly])
        print(render(module), file=file)

    print(file=file)
    for index in range(len(polygons)):
        difference = s.Difference((s.Instance(p.name) for p in polygons[index:]))
        name = f"{polygons[index].name}_only"
        module = s.Module(name, [difference])
        print(render(module), file=file)

    print(file=file)
    for index, polygon in enumerate(polygons):
        color = Color.from_hsv(index / len(polygons), 1, 1)
        instance = s.Instance(f"{polygon.name}_only")
        extrude = s.Extrude(thickness, instance)
        translate = s.Translate((0, 0, 0 * index * thickness), extrude)
        o = s.Color(color, translate)
        print(render(o), file=file)
