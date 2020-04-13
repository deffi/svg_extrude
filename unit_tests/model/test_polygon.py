import unittest

from svg2fff.model import Point, Polygon


class PolygonTest(unittest.TestCase):
    def test_index_paths(self):
        p = [Point(i, i) for i in range(10)]

        paths = (
            (p[0], p[2], p[4], p[8], p[0]),
            (p[5], p[3], p[4])
        )

        points, index_paths = Polygon(paths).index_paths()
        self.assertEqual([p[0], p[2], p[4], p[8], p[5], p[3]], points)
        self.assertEqual([[0, 1, 2, 3, 0], [4, 5, 2]], index_paths)


if __name__ == '__main__':
    unittest.main()
