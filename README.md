# svg2fff
Converts SVG images to multiple STL files for 3D printing

## Installation

Required packages:
  * tinycss2


## Limitations

All polygons will be rendered using evenodd fill rule, even if set
to nonzero.

## Slicer notes

### PrusaSlicer

STL and AMF objects are always centered on bed, even if the
option is off; 3MF objects are not

Can't be used with elephant's foot compensation as that will
be applied to each object individually.
 
