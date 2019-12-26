import cjlano_svg as svg
from os import path

from svg2stl.model import Polygon, Point, Color
import svg2stl.scad as s
from svg2stl.util import filter_repetition, render_lines

px = 25.4 / 96

datapath = path.join("..", "testdata")
outputpath = path.join(datapath, "output")
svg_file_name = path.join(datapath, "test.svg")
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
        print(render(s.Line(f"{polygon.name}_points = {s.render(polygon.points)};")), file=file)

    print(file=file)

    for index, polygon in enumerate(polygons):
        color = Color.from_hsv(index / len(polygons), 1, 1)
        poly = s.Polygon(polygon, f"{polygon.name}_points", None)
        extrude = s.Extrude(thickness, poly)
        o = s.Color(color, extrude)
        print(render(o), file=file)
