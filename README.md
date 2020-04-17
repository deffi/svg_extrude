svg2fff
=======

Creates 3D models (suitable for 3D printing) from an SVG file.

The 3D models will consist of polygons generated from the shapes in the SVG
file, extruded to a configurable height. An individual model is created for
every color in the SVG file. Optionally, colors can be replaced by the most
similar color from a given set of colors. 

OpenSCAD is used for 3D model generation.


Invocation
----------

Quick start:
    svg2fff --3mf foo.svg

Useful options:
  * --height 0.2
  * --colors "red,yellow,green,blue,black,white"
  * --overlay 0.8

See svg2fff -h for details.

The overlay will span all shapes, have no color, and be rendered to an
individual file (if individual files are produced).


SVG file preparation
--------------------

Paths may overlap. Paths will be clipped according to their Z order.

It is recommended to avoid coincident paths. Paths may be sampled at different
positions, which can cause small gaps.

Text must be converted to a path.


### Coordinate system

The SVG X axis (right) is mapped to the OpenSCAD X axis (right) and the SVG Y
axis (down) is mapped to the OpenSCAD Y axis (front to back). This means that
the image will be reproduced correctly when view from below (-Z). If you want to
view the image from above, flip either the SVG file or the 3D model as required.

The SVG origin (upper left corner of the page) is mapped to the OpenSCAD origin.


Installation
------------

Required packages:
  * tinycss2


Limitations
-----------

All polygons will be rendered using evenodd fill rule, even if set
to nonzero. This is a limitation of OpenSCAD.

SVG viewbox may not work as expected.

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
