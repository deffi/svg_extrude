![Unit tests](https://github.com/deffi/svg_extrude/workflows/Unit%20tests/badge.svg)
![License](https://img.shields.io/github/license/deffi/svg_extrude?color=blue)

svg_extrude
===========

Creates 3D models (suitable for 3D printing) from an SVG file. If the SVG file
contains multiple colors, a separate model will be created for each color. 

OpenSCAD is used for 3D model generation.


Quick start
-----------

Prerequisites:
  * Python >= 3.7
      * tinycss2
      * rapidtables
  * OpenSCAD (in the search path) 

Usage: `svg_extrude --3mf foo.svg`\
This will create files according to the colors in `foo.svg`, e. g.
`foo_red.3mf`. All shapes that have the same color will be part of the same
model.

See the section "SVG file preparation" and "limitations" for futher information.
      

Features
--------

The extrusion height can be configured using the `--height` argument. The
default is 0.2 mm, a typical layer height.

By default, all colors are rounded to the closest CSS color and the name of that
color is used in the output file. You can also configure the available colors.
Examples:
  * `--colors all`: all colors are used as they are in the SVG file; note that
    even slightly different colors will cause shapes to be rendered to different
    output files. Also, the output files will be named according to the HTML
    code of the color rather than its name.
  * `--colors "red,yellow,green,blue,black,white"`: only the specified colors
    are used. All of them must be valid CSS color names. All colors in the SVG
    file will be rounded to the closest of the specified colors, even if they
    are significantly different.
  * `--colors "fire_red:#FF0000, #FFFF00, grass_green:lime, blue`: only the
    specified colors are used. Colors can be:
      * A name and a color code
      * A color code
      * A name and a CSS color name. If the name is also a valid CSS color name,
        it will be overridden.
      * A CSS color name

One or multiple output file formats can be specified:
  * `--3mf`: 3MF format. The recommended format.
  * `--amf`: AMF format.
  * `--stl`: STL format.
  * `--scad`: OpenSCAD format, with colored shapes. This is useful for visually
    checking the interpretation of the SVG file or for including the result in
    another OpenSCAD model.

If you want to print the result without including it into a larger model, you
may want it only a single layer high to minimize the amount of color changes
(especially when changing colors manually). On the other hand, single-layer
print is unlikely to be robust enough. You can make the model thicker by adding
a single-color "overlay", spanning all shapes, by specifying its height (e. g.
`--overlay 0.8` - i. e, 0.8 mm). The overlay will be output as a separate file.
This feature is experimental and likely to change. 

By default, the SVG file will be rendered face down. You can use `--flip` to
change this. If an overlay is enabled, it will be below the object. This feature
is experimental and likely to change.

If rendering is very slow or the output file is very large, you can decrease the
precision by using the `--precision` argument. Larger values mean lower
precision (higher permissible deviation from the ideal shape); the default value
is 1. 


SVG file preparation
--------------------

Shapes in the SVG file are allowed to overlap; they will be clipped according to
their Z order. In fact, it may be better to let shapes overlap instead of
letting them touch because in the latter case, paths might be sampled at
different positions, which can cause small gaps.

By default, the SVG X axis (right) mapped to the OpenSCAD X axis (right) and the
SVG Y axis (down) is mapped to the OpenSCAD Y axis (front to back). This means
that the image will be reproduced correctly when view from below (-Z). If you
want to view the image from above, flip either the SVG file or the generated 3D
model.

With `--flip`, the SVG y axis will be mapped to the OpenSCAD -Y
axis (back to front below). This behavior is experimental and likely to change.

In any case, The SVG origin (upper left corner of the page) is mapped to the
OpenSCAD origin and the model extends from the origin in the +Z direction.


Limitations
-----------

Not all SVG features are supported:
  * All paths will be rendered using evenodd fill rule, even if set to nonzero.
    This is a limitation of OpenSCAD.
  * All shapes must have a solid fill color (i. e., gradients and patterns are
    not supported).
  * Outlined shapes (stroke) are not supported. You can use Inkscape to convert
    the outline to a separate path.
  * Text is not supported. Convert it to paths.
  * SVG viewbox may not work as expected.
  * SVG shapes using the `fill` element attribute rather than the `fill` style
    property will be interpreted as black. This is a limitation of the used SVG
    library.

All output coordinates are rounded to nanometers to avoid very long decimals due
to floating point accuracy limitations.


Slicer notes
------------

### PrusaSlicer

Procedure:
  * Configuration (advanced):
      * Print Settings -> Advanced -> Elephant foot compensation: 0 (advanced)
      * Print Settings -> Output options -> "Label objects": on (advanced)
  * Setup:
      * Import the group models individually
      * If you have an overlay, add it to the appropriate group as a part 
  * G-code post processing: insert M600 between objects:
        ; stop printing object foo id:0 copy 0
        M600
        ; printing object bar id:1 copy 0
  * Notes: with this procedure, multiple objects must be used; multi-part
    objects won't work because the parts will be sliced as one and the "Label
    objects" function won't label the individual parts.
  
Alternative procedure:
  * Configuration:
      * Printer Settings -> General -> Extruders: match the number of models
      * Printer Settings -> General -> Extruders: Single Extruder Multi
        Material: on
      * Printer Settings -> Extruder # -> Extruder Color
      * Printer Settings -> Custom G-code -> Tool change G-code:
            M600
      * Print Settings -> Multiple Extruders -> Wipe tower -> Enable: off
      * Print Settings -> Advanced -> Elephant foot compensation: 0 (advanced)
  * Setup:
      * Import one model
      * Add the other models as parts
  * G-code post processing: remove all tool change commands (T0, T1, ...)

Notes:
  * STL and AMF objects are always centered on the print bed individually, even
    if the "auto-center parts" option is off. 3MF objects (whether in a single
    file or in multiple files) are aligned according to their coordinates. This
    does not seem to be the case for the Z direction, where all object appear to
    be dropped to the print bed.
  * Elephant's foot compensation cannot be used if there are multiple objects in
    the first layer because it will be applied to each object individually.
  * "Complete individual objects" cannot be used because the slicer will refuse
    to slice objects where the bounding boxes (expanded by the horizontal
    clearance) overlap, even if the objects are only a single layer high.
  * PrusaSlicer insists on dropping all objects to the print surface. This means
    that the only way to print with multiple objects (first procedure) is to
    have the groups on the bed and the overlay (if any) as "part" of one of the
    group objects. Future workaround: anchor geometry.
