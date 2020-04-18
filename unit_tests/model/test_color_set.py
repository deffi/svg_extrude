import unittest

from svg_extrude.model import Color, ColorSet

# Default colors
red = Color(1, 0, 0, "red")
yellow = Color(1, 1, 0, "yellow")
green = Color(0, 1, 0, "green")
cyan = Color(0, 1, 1, "blue")
blue = Color(0, 0, 1, "blue")
magenta = Color(1, 0, 1, "magenta")

# Default colors with alternate names
grass = Color(0, 1, 0, "grass")
sky = Color(0, 0, 1, "sky")

# Default colors without names
nred = Color(1, 0, 0)
nyellow = Color(1, 1, 0)
ngreen = Color(0, 1, 0)
ncyan = Color(0, 1, 1)
nblue = Color(0, 0, 1)
nmagenta = Color(1, 0, 1)


class ColorSetTest(unittest.TestCase):
    def test_equality(self):
        cs = ColorSet({red, yellow, ngreen, nblue})
        self.assertEqual({ngreen, yellow, nblue, red}, cs)

    def test_by_name(self):
        cs = ColorSet({red, yellow, ngreen, nblue})
        self.assertEqual({"red": red, "yellow": yellow}, cs.by_name)

    def test_parse_single(self):
        available = ColorSet({red, yellow, green})

        # Basic cases
        self.assertEqual({Color(1, 0, 0)},               ColorSet.parse("#FF0000"))
        self.assertEqual({Color(1, 0, 0, "bright_red")}, ColorSet.parse("bright_red:#FF0000"))
        self.assertEqual({Color(1, 0, 0, "red")},        ColorSet.parse("red", available=available))
        self.assertEqual({Color(1, 0, 0, "bright_red")}, ColorSet.parse("bright_red:red", available=available))

        # With whitespace
        self.assertEqual({Color(1, 0, 0, "bright_red")}, ColorSet.parse(" bright_red :#FF0000"))
        self.assertEqual({Color(1, 0, 0, "bright_red")}, ColorSet.parse("bright_red: #FF0000 "))
        self.assertEqual({Color(1, 0, 0, "bright_red")}, ColorSet.parse(" bright_red : #FF0000 "))

        # Invalid reference
        with self.assertRaises(ValueError):
            ColorSet.parse("invalid")
        with self.assertRaises(ValueError):
            ColorSet.parse("inv:invalid")

    def test_parse_multi(self):
        # Simple and simple with name
        self.assertEqual({nred, nyellow, green, blue},
                         ColorSet.parse("#FF0000 , #FFFF00, green :#00FF00 ,blue: #0000FF"))

        # By reference
        available = ColorSet({red, yellow, green, blue})
        self.assertEqual({red, yellow, grass, sky},
                         ColorSet.parse("red , yellow, grass :green ,sky: blue", available=available))

    def test_closest(self):
        available = ColorSet({red, yellow, green})

        self.assertEqual(red,    available.closest(Color(1.0, 0.0, 0.0, "fire")))
        self.assertEqual(red   , available.closest(Color(1.0, 0.1, 0.0)))
        self.assertEqual(red   , available.closest(Color(1.0, 0.2, 0.0)))
        self.assertEqual(red   , available.closest(Color(1.0, 0.3, 0.0)))
        self.assertEqual(red   , available.closest(Color(1.0, 0.4, 0.0)))
        self.assertEqual(red   , available.closest(Color(1.0, 0.5, 0.0)))
        self.assertEqual(red   , available.closest(Color(1.0, 0.6, 0.0)))
        self.assertEqual(yellow, available.closest(Color(1.0, 0.7, 0.0)))
        self.assertEqual(yellow, available.closest(Color(1.0, 0.8, 0.0)))
        self.assertEqual(yellow, available.closest(Color(1.0, 0.9, 0.0)))
        self.assertEqual(yellow, available.closest(Color(1.0, 1.0, 0.0, "sun")))


if __name__ == '__main__':
    unittest.main()
