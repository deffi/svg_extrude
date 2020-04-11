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

The coordinate system used by sgv2fff is x right, y up. 

The SVG origin is at the upper left corner of the page (note that Inkscape uses
a different coordinate system with the origin at the lower left). The SVG origin
will be mapped to the coordinate origin. To preserve handedness, the y axis is
inverted. Work to be done.

 




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
 
