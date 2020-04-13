import unittest

from svg2fff.model import Group, Shape, Color, ColorSet


class GroupTest(unittest.TestCase):
    def test_by_color(self):
        red = Color(255, 0, 0)
        red2 = Color(255, 0, 64)
        yellow = Color(255, 255, 0)
        green = Color(0, 255, 0)

        strawberry = Shape("strawberry", red, None)
        raspberry = Shape("raspberry", red2, None)
        cranberry = Shape("cranberry", red, None)
        banana = Shape("banana", yellow, None)
        lemon = Shape("lemon", yellow, None)
        pear = Shape("pear", green, None)

        #         red         yellow  green red        red        green
        shapes = [strawberry, banana, pear, raspberry, cranberry, lemon]

        # Without color mapping
        self.assertEqual([
            Group(red, (strawberry, cranberry, )),
            Group(yellow, (banana, lemon, )),
            Group(green, (pear, )),
            Group(red2, (raspberry,))
        ], list(Group.by_color(shapes)))

        # With color mapping
        available_colors = ColorSet({red, yellow, green})
        self.assertEqual([
            Group(red, (strawberry, raspberry, cranberry, )),
            Group(yellow, (banana, lemon, )),
            Group(green, (pear, )),
        ], list(Group.by_color(shapes, color_mapping=available_colors.closest)))


if __name__ == '__main__':
    unittest.main()
