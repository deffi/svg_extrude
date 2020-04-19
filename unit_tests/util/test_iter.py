import unittest

from svg_extrude.util.iter import filter_repetition, each_with_remaining

class IterText(unittest.TestCase):
    def test_filter_repetition(self):
        # Empty
        self.assertEqual([], list(filter_repetition([])))

        # List
        self.assertEqual([1, 2, 3, 4, 3, 4, 5],
                         list(filter_repetition([1, 2, 3, 3, 3, 3, 4, 3, 4, 4, 5])))

    def test_with_remaining(self):
        # Empty
        self.assertEqual([], list(each_with_remaining([])))

        # List
        self.assertEqual([(11, [22, 44, 33]), (22, [44, 33]), (44, [33]), (33, [])],
                         list(each_with_remaining([11, 22, 44, 33])))

        # String
        self.assertEqual([("f", "red"), ("r", "ed"), ("e", "d"), ("d", "")],
                         list(each_with_remaining("fred")))


if __name__ == '__main__':
    unittest.main()
