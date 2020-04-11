import unittest

from svg2fff.model import Color
from svg2fff.model.color import svg as svg_colors


class ColorTest(unittest.TestCase):
    def test_hsv(self):
        self.assertEqual(Color.from_hsv(0/6, 1, 1, None).rgb(), (1.0, 0.0, 0.0))
        self.assertEqual(Color.from_hsv(1/6, 1, 1, None).rgb(), (1.0, 1.0, 0.0))
        self.assertEqual(Color.from_hsv(2/6, 1, 1, None).rgb(), (0.0, 1.0, 0.0))
        self.assertEqual(Color.from_hsv(3/6, 1, 1, None).rgb(), (0.0, 1.0, 1.0))
        self.assertEqual(Color.from_hsv(4/6, 1, 1, None).rgb(), (0.0, 0.0, 1.0))
        self.assertEqual(Color.from_hsv(5/6, 1, 1, None).rgb(), (1.0, 0.0, 1.0))

    def test_to_html(self):
        self.assertEqual("000000", Color.from_rgb(0, 0,   0.000/255, None).to_html())
        self.assertEqual("000000", Color.from_rgb(0, 0,   0.499/255, None).to_html())
        self.assertEqual("000001", Color.from_rgb(0, 0,   0.501/255, None).to_html())
        self.assertEqual("000001", Color.from_rgb(0, 0,   1.000/255, None).to_html())
        self.assertEqual("000001", Color.from_rgb(0, 0,   1.499/255, None).to_html())
        self.assertEqual("000002", Color.from_rgb(0, 0,   1.501/255, None).to_html())
        self.assertEqual("0000FE", Color.from_rgb(0, 0, 254.499/255, None).to_html())
        self.assertEqual("0000FF", Color.from_rgb(0, 0, 254.501/255, None).to_html())
        self.assertEqual("0000FF", Color.from_rgb(0, 0, 255.000/255, None).to_html())
        self.assertEqual("ABFA11", Color.from_rgb(0.671, 0.980, 0.067, None).to_html())
        self.assertEqual("FFFFFF", Color.from_rgb(1, 1, 1, None).to_html())

    # TODO explicitly test Color.xyz and Color.rgb for some colors, confirm the
    # values with another source

    # Needs the colormath package, but note that that pulls in numpy
    # def test_xyz(self):
    #     from colormath.color_objects import sRGBColor
    #     from colormath.color_conversions import RGB_to_XYZ
    #
    #     for color in svg_colors:
    #         # Use colormath to calculate the reference as tuple (x, y, z)
    #         reference = sRGBColor(*color.rgb())
    #         reference = RGB_to_XYZ(reference)
    #         reference = (reference.xyz_x, reference.xyz_y, reference.xyz_z)
    #
    #         self.assertSequenceEqual(reference, color.xyz())

    # Needs the colormath package, but note that that pulls in numpy
    # def test_lab(self):
    #     # For the 10°-observer, Colormath uses slightly rounded values for some
    #     # constants, so the values will be slightly off.
    #     observer = 2
    #
    #     from colormath.color_objects import sRGBColor
    #     from colormath.color_conversions import RGB_to_XYZ, XYZ_to_Lab
    #
    #     for color in svg_colors:
    #         # Use colormath to calculate the reference as tuple (L, a, b)
    #         reference = sRGBColor(*color.rgb())
    #         reference = RGB_to_XYZ(reference)
    #         reference.set_observer(str(observer))
    #         reference = XYZ_to_Lab(reference)
    #         reference = (reference.lab_l, reference.lab_a, reference.lab_b)
    #
    #         self.assertSequenceEqual(reference, color.lab(observer))


if __name__ == '__main__':
    unittest.main()
