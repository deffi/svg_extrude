import unittest

from svg_extrude.model import Point, Color
from svg_extrude.scad import Identifier, StringLiteral
from svg_extrude.scad.util import render


class TestUtil(unittest.TestCase):
    def test_render(self):
        # Number
        self.assertEqual("42", render(42))
        self.assertEqual("42.0", render(42.0))

        # Point
        mm = 1e-3
        p1 = Point(11 * mm, 12 * mm)
        p2 = Point(21 * mm, 22 * mm)
        self.assertEqual("[11.0, 12.0]", render(p1))
        self.assertEqual("[21.0, 22.0]", render(p2))
        self.assertEqual("[[11.0, 12.0], [21.0, 22.0]]", render([p1, p2]))

        # Color
        self.assertEqual('"#FF8000"', render(Color(1, 0.5, 0)))

        # List, tuple
        self.assertEqual("[1, 2, 33]", render([1, 2, 33]))
        self.assertEqual("[1, 2, 33]", render((1, 2, 33)))

        # Identifier
        self.assertEqual("foo", render(Identifier("foo")))

        # StringLiteral
        with self.assertRaises(NotImplementedError):
            render(StringLiteral("foo\"bar"))

        # str
        with self.assertRaises(ValueError):
            render("foo")

        # Other
        with self.assertRaises(ValueError):
            render(None)


if __name__ == '__main__':
    unittest.main()
