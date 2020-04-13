import unittest

from svg2fff.model import Color
from svg2fff.model.color import Xyz, Lab

# Default colors
red = Color(1, 0, 0, "red")
yellow = Color(1, 1, 0, "yellow")
green = Color(0, 1, 0, "green")
cyan = Color(0, 1, 1, "cyan")
blue = Color(0, 0, 1, "blue")
magenta = Color(1, 0, 1, "magenta")

# Default colors without names
nred = Color(1, 0, 0)
nyellow = Color(1, 1, 0)
ngreen = Color(0, 1, 0)
ncyan = Color(0, 1, 1)
nblue = Color(0, 0, 1)
nmagenta = Color(1, 0, 1)


class ColorTest(unittest.TestCase):
    def assertSequenceAlmostEqual(self, expected, actual, places=None, msg=None, delta=None):
        self.assertEqual(type(expected), type(actual))
        self.assertEqual(len(expected), len(actual))
        for a, b in zip(expected, actual):
            msg = msg or f"\nExpected: {expected}\nActual:   {actual}"
            self.assertAlmostEqual(a, b, places, msg, delta)

    def test_repr(self):
        self.assertEqual("Color(r=1, g=0, b=0, name=None)", repr(Color(1, 0, 0)))
        self.assertEqual("Color(r=0, g=1, b=0, name='green')", repr(Color(0, 1, 0, "green")))

    def test_equality(self):
        # Equality
        self.assertEqual(Color(1, 0, 0, "red"), red)
        self.assertEqual(Color(1, 0, 0), nred)

        # Equality includes the name
        self.assertNotEqual(red, nred)

    def test_hashing(self):
        colors = {red, green, nblue}

        self.assertIn(red, colors)
        self.assertNotIn(yellow, colors)
        self.assertIn(green, colors)
        self.assertIn(nblue, colors)

        objects = {red: "fire", green: "grass", nblue: "sky"}

        self.assertIn(red, colors)
        self.assertNotIn(yellow, colors)
        self.assertIn(green, colors)
        self.assertIn(nblue, colors)

        self.assertEqual("fire", objects[red])
        self.assertEqual("grass", objects[green])
        self.assertEqual("sky", objects[nblue])

    def test_display_name(self):
        self.assertEqual("red", red.display_name())                    # Yes name
        self.assertEqual("FF0000", nred.display_name())                # No name
        self.assertEqual("FF0000", Color(1, 0, 0, "").display_name())  # Empty name

    def test_rgb(self):
        self.assertEqual((1, 0, 0), red.rgb())
        self.assertEqual((1, 0, 0), nred.rgb())

    def test_from_html(self):
        self.assertEqual(Color(      0,       0,       0), Color.from_html("000000"))
        self.assertEqual(Color(      0,       0,   1/255), Color.from_html("000001"))
        self.assertEqual(Color(      0,       0,   2/255), Color.from_html("000002"))
        self.assertEqual(Color(      0,       0, 254/255), Color.from_html("0000FE"))
        self.assertEqual(Color(      0,       0,       1), Color.from_html("0000FF"))
        self.assertEqual(Color(171/255, 250/255,  17/255), Color.from_html("ABFA11"))
        self.assertEqual(Color(      1,       1,       1), Color.from_html("FFFFFF"))

    def test_html(self):
        self.assertEqual("000000", Color(0    , 0    ,   0.000/255).html())
        self.assertEqual("000000", Color(0    , 0    ,   0.499/255).html())
        self.assertEqual("000001", Color(0    , 0    ,   0.501/255).html())
        self.assertEqual("000001", Color(0    , 0    ,   1.000/255).html())
        self.assertEqual("000001", Color(0    , 0    ,   1.499/255).html())
        self.assertEqual("000002", Color(0    , 0    ,   1.501/255).html())
        self.assertEqual("0000FE", Color(0    , 0    , 254.499/255).html())
        self.assertEqual("0000FF", Color(0    , 0    , 254.501/255).html())
        self.assertEqual("0000FF", Color(0    , 0    , 255.000/255).html())
        self.assertEqual("ABFA11", Color(0.671, 0.980,   0.067    ).html())
        self.assertEqual("FFFFFF", Color(1    , 1    ,   1        ).html())

    def test_xyz(self):
        # Values from colormine (http://colormine.org/convert/rgb-to-xyz).
        
        self.assertSequenceAlmostEqual(Xyz(0.0000, 0.0000, 0.0000), Color.from_html("000000").xyz(), places=3)
        self.assertSequenceAlmostEqual(Xyz(0.9505, 1.0000, 1.0890), Color.from_html("FFFFFF").xyz(), places=3)

        self.assertSequenceAlmostEqual(Xyz(0.4124, 0.2126, 0.0193), Color.from_html("FF0000").xyz(), places=3)
        self.assertSequenceAlmostEqual(Xyz(0.3576, 0.7152, 0.1192), Color.from_html("00FF00").xyz(), places=3)
        self.assertSequenceAlmostEqual(Xyz(0.1805, 0.0722, 0.9505), Color.from_html("0000FF").xyz(), places=3)

        self.assertSequenceAlmostEqual(Xyz(0.3186, 0.2390, 0.0416), Color.from_html("d2691e").xyz(), places=3)
        self.assertSequenceAlmostEqual(Xyz(0.5028, 0.3702, 0.1208), Color.from_html("ff7f50").xyz(), places=3)
        self.assertSequenceAlmostEqual(Xyz(0.3058, 0.1604, 0.0576), Color.from_html("dc143c").xyz(), places=3)

    def test_lab(self):
        # Values from the tested method, checked with colormine[1]. The values
        # are a bit off, but that may be due to different parameter choice. The
        # value for white (FFFFFF) is significantly off (colormine value: 100,
        # 0.005, -0.010). Further investigation may be in order.
        # [1] http://colormine.org/convert/rgb-to-lab

        self.assertSequenceAlmostEqual(Lab(  0.000, 0.000,  0.000), Color.from_html("000000").lab(10), places=3)
        self.assertSequenceAlmostEqual(Lab(100.000, 0.412, -0.990), Color.from_html("FFFFFF").lab(10), places=3)

        self.assertSequenceAlmostEqual(Lab(53.237,  80.402,   66.945), Color.from_html("FF0000").lab(10), places=3)
        self.assertSequenceAlmostEqual(Lab(87.736, -85.884,   82.713), Color.from_html("00FF00").lab(10), places=3)
        self.assertSequenceAlmostEqual(Lab(32.301,  79.432, -108.802), Color.from_html("0000FF").lab(10), places=3)

        self.assertSequenceAlmostEqual(Lab(55.988, 37.334, 56.408), Color.from_html("d2691e").lab(10), places=3)
        self.assertSequenceAlmostEqual(Lab(67.293, 45.683, 47.016), Color.from_html("ff7f50").lab(10), places=3)
        self.assertSequenceAlmostEqual(Lab(47.033, 71.202, 33.224), Color.from_html("dc143c").lab(10), places=3)

    def test_delta_e(self):
        colors = {red, yellow, green, Color.from_html("0FF1CE"), Color.from_html("BADA55")}

        # It's symmetric
        for c1 in colors:
            for c2 in colors:
                self.assertEqual(c1.delta_e(c2), c2.delta_e(c1))

        # Colormine (http://colormine.org/delta-e-calculator) gives 58.9127.
        # Further investigation may be in order.
        self.assertAlmostEqual(62.741, Color.from_html("0FF1CE").delta_e(Color.from_html("BADA55")), places=3)

    # Needs the colormath package, but note that that pulls in numpy
    # def test_xyz_colormath(self):
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
    # def test_lab_colormath(self):
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
