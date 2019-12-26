import cjlano_svg as svg
from os import path

from svg2stl import Polygon, Point, Color, ColorBlock, Extrude
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

with open(scad_file_name, "w") as file:
    for index, path in enumerate(svg_paths):
        polygon = Polygon()
        polygon.thickness = thickness
        polygon.offset = -1 * index * thickness
        for subpath in path.segments(precision):
            polygon.add_subpolygon((Point(p.x, -p.y) for p in filter_repetition(subpath)))

        # print(polygon.to_scad(), file=file)
        # print(polygon.render_lines())
        color = Color.from_hsv(index / len(svg_paths), 1, 1)
        o = ColorBlock(color, polygon)
        print(render_lines(o.render_lines(), "", "    "), file=file)