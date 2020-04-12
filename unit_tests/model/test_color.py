import unittest

from svg2fff.model import Color


class ColorTest(unittest.TestCase):
    def assertSequenceAlmostEqual(self, expected, actual, places=None, msg=None, delta=None):
        self.assertEqual(type(expected), type(actual))
        self.assertEqual(len(expected), len(actual))
        for a, b in zip(expected, actual):
            msg = msg or f"\nExpected: {expected}\nActual:   {actual}"
            self.assertAlmostEqual(a, b, places, msg, delta)

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

    def test_to_xyz(self):
        # Values from colormine (http://colormine.org/convert/rgb-to-xyz).
        
        self.assertSequenceAlmostEqual((0.0000, 0.0000, 0.0000), Color.from_html("000000", None).xyz(), places=3)
        self.assertSequenceAlmostEqual((0.9505, 1.0000, 1.0890), Color.from_html("FFFFFF", None).xyz(), places=3)

        self.assertSequenceAlmostEqual((0.4124, 0.2126, 0.0193), Color.from_html("FF0000", None).xyz(), places=3)
        self.assertSequenceAlmostEqual((0.3576, 0.7152, 0.1192), Color.from_html("00FF00", None).xyz(), places=3)
        self.assertSequenceAlmostEqual((0.1805, 0.0722, 0.9505), Color.from_html("0000FF", None).xyz(), places=3)

        self.assertSequenceAlmostEqual((0.3186, 0.2390, 0.0416), Color.from_html("d2691e", None).xyz(), places=3)
        self.assertSequenceAlmostEqual((0.5028, 0.3702, 0.1208), Color.from_html("ff7f50", None).xyz(), places=3)
        self.assertSequenceAlmostEqual((0.3058, 0.1604, 0.0576), Color.from_html("dc143c", None).xyz(), places=3)

    def test_to_lab(self):
        # Values from the tested method, checked with colormine[1]. The values
        # are a bit off, but that may be due to different parameter choice. The
        # value for white (FFFFFF) is significantly off (colormine value: 100,
        # 0.005, -0.010). Further investigation may be in order.
        # [1] http://colormine.org/convert/rgb-to-lab

        self.assertSequenceAlmostEqual((  0.000, 0.000,  0.000), Color.from_html("000000", None).lab(), places=3)
        self.assertSequenceAlmostEqual((100.000, 0.414, -0.985), Color.from_html("FFFFFF", None).lab(), places=3)

        self.assertSequenceAlmostEqual((53.239,  80.404,   66.947), Color.from_html("FF0000", None).lab(), places=3)
        self.assertSequenceAlmostEqual((87.735, -85.884,   82.713), Color.from_html("00FF00", None).lab(), places=3)
        self.assertSequenceAlmostEqual((32.299,  79.430, -108.798), Color.from_html("0000FF", None).lab(), places=3)

        self.assertSequenceAlmostEqual((55.989, 37.338, 56.410), Color.from_html("d2691e", None).lab(), places=3)
        self.assertSequenceAlmostEqual((67.294, 45.686, 47.020), Color.from_html("ff7f50", None).lab(), places=3)
        self.assertSequenceAlmostEqual((47.035, 71.203, 33.228), Color.from_html("dc143c", None).lab(), places=3)


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
