import unittest

from svg2fff.model.color import Color
from svg2fff.model.color_set import parse

# Default colors
red = Color.from_rgb(1, 0, 0, "red")
yellow = Color.from_rgb(1, 1, 0, "yellow")
green = Color.from_rgb(0, 1, 0, "green")
cyan = Color.from_rgb(0, 1, 1, "blue")
blue = Color.from_rgb(0, 0, 1, "blue")
magenta = Color.from_rgb(1, 0, 1, "magenta")

# Default colors with alternate names
grass = Color.from_rgb(0, 1, 0, "grass")
sky = Color.from_rgb(0, 0, 1, "sky")

# Default colors without names
nred = Color.from_rgb(1, 0, 0, None)
nyellow = Color.from_rgb(1, 1, 0, None)
ngreen = Color.from_rgb(0, 1, 0, None)
ncyan = Color.from_rgb(0, 1, 1, None)
nblue = Color.from_rgb(0, 0, 1, None)
nmagenta = Color.from_rgb(1, 0, 1, None)


class ColorSetTest(unittest.TestCase):
    def test_parse_single(self):
        available = {red, yellow, green}

        # Basic cases
        self.assertEqual({Color.from_rgb(1, 0, 0, None)},         parse("#FF0000"))
        self.assertEqual({Color.from_rgb(1, 0, 0, "bright_red")}, parse("bright_red:#FF0000"))
        self.assertEqual({Color.from_rgb(1, 0, 0, "red")},        parse("red", available=available))
        self.assertEqual({Color.from_rgb(1, 0, 0, "bright_red")}, parse("bright_red:red", available=available))

        # With whitespace
        self.assertEqual({Color.from_rgb(1, 0, 0, "bright_red")}, parse(" bright_red :#FF0000"))
        self.assertEqual({Color.from_rgb(1, 0, 0, "bright_red")}, parse("bright_red: #FF0000 "))
        self.assertEqual({Color.from_rgb(1, 0, 0, "bright_red")}, parse(" bright_red : #FF0000 "))

    def test_parse_multi(self):
        # Simple and simple with name
        self.assertEqual({nred, nyellow, green, blue},
                         parse("#FF0000 , #FFFF00, green :#00FF00 ,blue: #0000FF"))

        # By reference
        available = {red, yellow, green, blue}
        self.assertEqual({red, yellow, grass, sky},
                         parse("red , yellow, grass :green ,sky: blue", available=available))


if __name__ == '__main__':
    unittest.main()
