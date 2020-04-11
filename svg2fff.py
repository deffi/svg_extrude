import argparse
import re

from svg2fff.model import Shape, Group, Color, Scene
from svg2fff import OutputFile
from svg2fff.scad import render_file as render_scad_file

# available_colors = [Color.from_hsv(i/6, 1, 1) for i in range(6)]


def write_scad_file(base_name, scene: Scene, height):
    file_name = f"{base_name}.scad"
    print(f"Writing to {file_name}")
    with open(file_name, "w") as file:
        OutputFile(file).write(scene.shapes, scene.groups, height)


def render_file(base_name, format, scene, height):
    for index, group in enumerate(scene.groups):
        file_name = f"{base_name}_{index}_{group.color.to_html()}.{format}"
        print(f"Rendering to {file_name}")
        with render_scad_file(file_name) as file:
            OutputFile(file).write(scene.shapes, [group], height)


def svg2fff(args):
    for svg_file in args.svg_files:
        # Determine the base file name for the output
        base_name = re.sub('.svg$', '', svg_file)

        # Read the scene from the SVG file
        scene: Scene = Scene.from_svg(svg_file, args.precision)

        # Write the output files
        if args.scad:    write_scad_file(base_name, scene, args.height)
        if args.stl:     render_file(base_name, "stl", scene, args.height)
        if args.amf:     render_file(base_name, "amf", scene, args.height)
        if args.threemf: render_file(base_name, "3mf", scene, args.height)


parser = argparse.ArgumentParser(description="Generates 3D models for 3D printing from an SVG file.")
parser.add_argument("--scad", help="Output an OpenSCAD file", action="store_true")
parser.add_argument("--stl", help="Output STL files, one for each color", action="store_true")
parser.add_argument("--amf", help="Output AMF files, one for each color", action="store_true")
parser.add_argument("--3mf", help="Output 3MF files, one for each color", action="store_true", dest="threemf")
parser.add_argument("--height", help="Extrusion height (thickness)", type=float, default=0.2)
parser.add_argument("--precision", help="Precision", type=float, default=1)
parser.add_argument("svg_files", nargs='*', help="SVG file name")
svg2fff(parser.parse_args())
