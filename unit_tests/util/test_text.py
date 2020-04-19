import unittest

from svg_extrude.util.text import count


class TextTest(unittest.TestCase):
    def test_coung(self):
        self.assertEqual("0 widgets", count(0, "widget", "widgets"))
        self.assertEqual("1 widget" , count(1, "widget", "widgets"))
        self.assertEqual("2 widgets", count(2, "widget", "widgets"))


if __name__ == '__main__':
    unittest.main()
