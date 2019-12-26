import unittest

from svg2stl.model import Color


class TestColo(unittest.TestCase):
    def test_hsv(self):
        self.assertEqual(Color.from_hsv(0/6, 1, 1).rgb(), (1.0, 0.0, 0.0))
        self.assertEqual(Color.from_hsv(1/6, 1, 1).rgb(), (1.0, 1.0, 0.0))
        self.assertEqual(Color.from_hsv(2/6, 1, 1).rgb(), (0.0, 1.0, 0.0))
        self.assertEqual(Color.from_hsv(3/6, 1, 1).rgb(), (0.0, 1.0, 1.0))
        self.assertEqual(Color.from_hsv(4/6, 1, 1).rgb(), (0.0, 0.0, 1.0))
        self.assertEqual(Color.from_hsv(5/6, 1, 1).rgb(), (1.0, 0.0, 1.0))


if __name__ == '__main__':
    unittest.main()
