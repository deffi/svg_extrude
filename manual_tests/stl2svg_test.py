from os import path

import cjlano_svg as svg

from svg2stl.model import Shape, Group, Color
from svg2stl import OutputFile

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
    output_file = OutputFile(file)
    output_file.write(shapes, groups[0:1], thickness)
