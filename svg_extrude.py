from typing import Optional
import argparse
import re
import sys
from os import path

import rapidtables as rt

from svg_extrude.model import Scene, ColorSet
from svg_extrude import OutputWriter
from svg_extrude.scad import Renderer as ScadRenderer
from svg_extrude import css
from svg_extrude.util.text import count


def write_scad_file(base_name, scene: Scene, height, overlay_height, flip):
    file_name = f"{base_name}.scad"
    print(f"Writing to {file_name}")
    with open(file_name, "w") as file:
        OutputWriter(file).write(scene.shapes, scene.groups, thickness=height,
                                 overlay_thickness=overlay_height,
                                 flip=flip)


def render_file(base_name, output_format, scene, height, overlay_height, flip):
    for group in scene.groups:
        file_name = f"{base_name}_{group.color.display_name()}.{output_format}"
        print(f"Rendering to {file_name}")
        with ScadRenderer().render_file(file_name) as scad_file:
            OutputWriter(scad_file).write(scene.shapes, [group], thickness=height,
                                          overlay_thickness=None,
                                          flip=flip)

    if overlay_height:
        # TODO code duplication
        # TODO possible collision with color "overlay"
        file_name = f"{base_name}_overlay.{output_format}"
        print(f"Rendering to {file_name}")
        with ScadRenderer().render_file(file_name) as scad_file:
            OutputWriter(scad_file).write(scene.shapes, [], thickness=height,
                                          overlay_thickness=overlay_height,
                                          flip=flip)


def show_info(scene: Scene):
    table = []
    for group in scene.groups:
        name = group.color.display_name()
        shape_count = len(group.shapes)
        max_delta_e = max(shape.color.delta_e(group.color) for shape in group.shapes)
        table.append({
            "prefix": "   ",
            "name": f"{name}:",
            "shape_count": f"{count(shape_count, 'shape', 'shapes')},",
            "max_delta_e": f"max ΔE =",
            "max_delta_e_value": f"{max_delta_e:.2f}"
        })

    print("Groups:")
    print(rt.format_table(table, generate_header=False, separator=" "))


def svg_extrude(args):
    for svg_file in args.svg_files:
        # Determine the base file name for the output
        base_name = re.sub('.svg$', '', svg_file)

        if args.flip:
            flip = args.height + args.overlay
        else:
            flip = None

        # Create the colors
        colors: Optional[ColorSet]
        if   args.colors == "all":     colors = None
        elif args.colors == "basic":   colors = css.default_colors
        elif args.colors == "default": colors = css.colors
        else: colors = ColorSet.parse(args.colors, available=css.colors)

        # Read the scene from the SVG file
        scene: Scene = Scene.from_svg(svg_file, precision=args.precision, available_colors=colors)
        show_info(scene)

        # Write the output files
        if args.scad:    write_scad_file(base_name, scene, args.height, args.overlay, flip)
        if args.stl:     render_file(base_name, "stl", scene, args.height, args.overlay, flip)
        if args.amf:     render_file(base_name, "amf", scene, args.height, args.overlay, flip)
        if args.threemf: render_file(base_name, "3mf", scene, args.height, args.overlay, flip)


parser = argparse.ArgumentParser(description="Generates 3D models (for 3D printing) from an SVG file.")
parser.add_argument("--scad", action="store_true",
                    help="Output an OpenSCAD file")
parser.add_argument("--stl", action="store_true",
                    help="Output STL files, one for each color")
parser.add_argument("--amf", action="store_true",
                    help="Output AMF files, one for each color")
parser.add_argument("--3mf", action="store_true", dest="threemf",
                    help="Output 3MF files, one for each color")
parser.add_argument("--height", type=float, default=0.2,
                    help="Extrusion height (thickness) in mm")
parser.add_argument("--precision", type=float, default=1,
                    help="Precision for approximating curves; smaller is more precise.")
parser.add_argument("--colors", default="default",
                    help="'default', 'all', 'basic', or comma-separated list of colors. " 
                         "Colors can be specified by value (e. g. #4682b4) or CSS name (e. g. steelblue). "
                         "Optionally, a name can be specified (e. g. my_blue:#4682b4 or my_blue:steelblue).")
parser.add_argument("--overlay", type=float, default=None,
                    help="Height of the overlay layer in mm (experimental!)")
parser.add_argument("--flip", action="store_true",
                    help="Flip around the x axis (experimental!)")
parser.add_argument("svg_files", nargs='+', help="SVG file name")
svg_extrude(parser.parse_args())