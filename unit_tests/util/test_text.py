import unittest

from svg_extrude.util.text import pluralize


class TextTest(unittest.TestCase):
    def test_pluralize(self):
        self.assertEqual("0 widgets", pluralize(0, "widget", "widgets"))
        self.assertEqual("1 widget",  pluralize(1, "widget", "widgets"))
        self.assertEqual("2 widgets", pluralize(2, "widget", "widgets"))


if __name__ == '__main__':
    unittest.main()
