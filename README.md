svg2fff
=======

Converts SVG images to 3D models.


Invocation
----------


SVG file preparation
--------------------

Paths may overlap. Paths will be clipped according to their Z order.

It is recommended to avoid coincident paths. Paths may be sampled at different
positions, which can cause small gaps.


### Coordinate system

The SVG X axis (right) is mapped to the OpenSCAD X axis (right) and the SVG Y
axis (down) is mapped to the OpenSCAD Y axis (front to back). This means that
the image will be reproduced correctly when view from below (-Z). If you want to
view the image from above, flip either the SVG file or the 3D model as required.

The SVG origin (upper left corner of the page) is mapped to the OpenSCAD origin.


## Installation

Required packages:
  * tinycss2


## Limitations

All polygons will be rendered using evenodd fill rule, even if set
to nonzero.

SVG viewbox may not work as expected.


## Slicer notes

### PrusaSlicer

STL and AMF objects are always centered on bed, even if the
option is off; 3MF objects are not

Can't be used with elephant's foot compensation as that will
be applied to each object individually.
 
