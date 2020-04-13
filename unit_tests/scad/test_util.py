import unittest

from svg2fff.model import Point
from svg2fff.scad.util import render


class TestUtil(unittest.TestCase):
    def test_render(self):
        self.assertEqual("42", render(42))
        self.assertEqual("42.0", render(42.0))

        self.assertEqual("[1, 2, 33]", render([1, 2, 33]))
        self.assertEqual("[1, 2, 33]", render((1, 2, 33)))

        mm = 1e-3
        p1 = Point(11 * mm, 12 * mm)
        p2 = Point(21 * mm, 22 * mm)
        self.assertEqual("[11.0, 12.0]", render(p1))
        self.assertEqual("[21.0, 22.0]", render(p2))
        self.assertEqual("[[11.0, 12.0], [21.0, 22.0]]", render([p1, p2]))

        with self.assertRaises(ValueError):
            render("foo")


if __name__ == '__main__':
    unittest.main()
