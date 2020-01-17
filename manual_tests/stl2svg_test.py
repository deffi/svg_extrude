from os import path
import re

import cjlano_svg as svg

from svg2stl.model import Shape, Group, Color
from svg2stl import OutputFile
from svg2stl.scad import render_file

px = 25.4 / 96

datapath = path.join("..", "testdata")
outputpath = path.join(datapath, "output")
svg_file_name = path.join(datapath, "test2.svg")
scad_file_name = path.join(outputpath, "output.scad")

svg_picture = svg.parse(svg_file_name)
svg_paths = svg_picture.flatten()

precision=1
thickness=0.2

available_colors = [Color.from_hsv(i/6, 1, 1) for i in range(6)]


# Create the shapes
shapes = [Shape.from_svg_path(path, precision) for path in svg_paths]

# Group the shapes by color
# groups = Group.by_color(shapes, colormap=lambda color: color.closest_hsv(available_colors))
groups = Group.by_color(shapes)

base_name = re.sub('.svg$', '', svg_file_name)

# TODO calculate scad_file_name like stl_file_name
print(f"Writing to {scad_file_name}")
with open(scad_file_name, "w") as file:
    OutputFile(file).write(shapes, groups, thickness)

for index, group in enumerate(groups):
    svg_file_name = path.join(datapath, "test2.svg")
    stl_file_name = f"{base_name}_{index}_{group.color.to_html()}.stl"
    print(f"Rendering to {stl_file_name}")
    with render_file(stl_file_name) as file:
        OutputFile(file).write(shapes, [group], thickness)
