import unittest

from svg_extrude.util import group_by
from svg_extrude.util.iter import filter_repetition, each_with_remaining


class TestUtil(unittest.TestCase):
    def test_filter_repetition(self):
        values = [1, 2, 2, 3, 3, 3, 4, 3, 3, 3]

        self.assertEqual(list(filter_repetition(values)), [1, 2, 3, 4, 3])

    def test_with_remaining(self):
        self.assertEqual(list(each_with_remaining([])), [])
        self.assertEqual(list(each_with_remaining([1, 2, 3, 4])), [
            (1, [2, 3, 4]),
            (2, [3, 4]),
            (3, [4]),
            (4, []),
        ])

    def test_group_by(self):
        self.assertEqual(group_by([1, 2, 3, 4, 5, 6, 10, 11, 12, 13], lambda x: x % 3),
                         {
                             0: [3, 6, 12],
                             1: [1, 4, 10, 13],
                             2: [2, 5, 11],
                         })


if __name__ == '__main__':
    unittest.main()
