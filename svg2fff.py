import argparse
import re
import cjlano_svg as svg

from svg2fff.model import Shape, Group, Color
from svg2fff import OutputFile
from svg2fff.scad import render_file as render_scad_file

# available_colors = [Color.from_hsv(i/6, 1, 1) for i in range(6)]


def write_scad_file(base_name, shapes, groups, height):
    file_name = f"{base_name}.scad"
    print(f"Writing to {file_name}")
    with open(file_name, "w") as file:
        OutputFile(file).write(shapes, groups, height)


def render_file(base_name, format, shapes, groups, height):
    for index, group in enumerate(groups):
        file_name = f"{base_name}_{index}_{group.color.to_html()}.{format}"
        print(f"Rendering to {file_name}")
        with render_scad_file(file_name) as file:
            OutputFile(file).write(shapes, [group], height)


def svg2fff(args):
    for svg_file in args.svg_files:
        base_name = re.sub('.svg$', '', svg_file)

        # Read the SVG file, extract the paths, create the shapes, and group
        # them by color
        svg_picture = svg.parse(svg_file)
        svg_paths = svg_picture.flatten()
        shapes = [Shape.from_svg_path(path, args.precision) for path in svg_paths]
        # groups = Group.by_color(shapes, colormap=lambda color: color.closest_hsv(available_colors)) # TODO
        groups = Group.by_color(shapes)

        if args.scad:
            write_scad_file(base_name, shapes, groups, args.height)

        if args.stl:
            render_file(base_name, "stl", shapes, groups, args.height)

        if args.amf:
            render_file(base_name, "amf", shapes, groups, args.height)

        if args.threemf:
            render_file(base_name, "3mf", shapes, groups, args.height)


parser = argparse.ArgumentParser(description="Generates 3D models for 3D printing from an SVG file.")
parser.add_argument("--scad", help="Output an OpenSCAD file", action="store_true")
parser.add_argument("--stl", help="Output STL files, one for each color", action="store_true")
parser.add_argument("--amf", help="Output AMF files, one for each color", action="store_true")
parser.add_argument("--3mf", help="Output 3MF files, one for each color", action="store_true", dest="threemf")
parser.add_argument("--height", help="Extrusion height (thickness)", type=float, default=0.2)
parser.add_argument("--precision", help="Precision", type=float, default=1)
parser.add_argument("svg_files", nargs='*', help="SVG file name")
svg2fff(parser.parse_args())
