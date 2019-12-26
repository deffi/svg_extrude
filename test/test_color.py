import unittest

from svg2stl import Color

class TestScadObject(unittest.TestCase):
    def test_hsv(self):
        self.assertEqual(Color.from_hsv(0, 1, 1).rgb(), (1.0, 0.0, 0.0))


if __name__ == '__main__':
    unittest.main()
