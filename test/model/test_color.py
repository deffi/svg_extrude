import unittest

from svg2stl.model import Color


class ColorTest(unittest.TestCase):
    def test_hsv(self):
        self.assertEqual(Color.from_hsv(0/6, 1, 1).rgb(), (1.0, 0.0, 0.0))
        self.assertEqual(Color.from_hsv(1/6, 1, 1).rgb(), (1.0, 1.0, 0.0))
        self.assertEqual(Color.from_hsv(2/6, 1, 1).rgb(), (0.0, 1.0, 0.0))
        self.assertEqual(Color.from_hsv(3/6, 1, 1).rgb(), (0.0, 1.0, 1.0))
        self.assertEqual(Color.from_hsv(4/6, 1, 1).rgb(), (0.0, 0.0, 1.0))
        self.assertEqual(Color.from_hsv(5/6, 1, 1).rgb(), (1.0, 0.0, 1.0))

    def test_to_html(self):
        self.assertEqual("000000", Color.from_rgb(0, 0,   0.000/255).to_html())
        self.assertEqual("000000", Color.from_rgb(0, 0,   0.499/255).to_html())
        self.assertEqual("000001", Color.from_rgb(0, 0,   0.501/255).to_html())
        self.assertEqual("000001", Color.from_rgb(0, 0,   1.000/255).to_html())
        self.assertEqual("000001", Color.from_rgb(0, 0,   1.499/255).to_html())
        self.assertEqual("000002", Color.from_rgb(0, 0,   1.501/255).to_html())
        self.assertEqual("0000FE", Color.from_rgb(0, 0, 254.499/255).to_html())
        self.assertEqual("0000FF", Color.from_rgb(0, 0, 254.501/255).to_html())
        self.assertEqual("0000FF", Color.from_rgb(0, 0, 255.000/255).to_html())
        self.assertEqual("ABFA11", Color.from_rgb(0.671, 0.980, 0.067).to_html())
        self.assertEqual("FFFFFF", Color.from_rgb(1, 1, 1).to_html())


if __name__ == '__main__':
    unittest.main()
