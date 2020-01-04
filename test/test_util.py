import unittest

from svg2stl.util import filter_repetition, with_remaining


class TestUtil(unittest.TestCase):
    def test_filter_repetition(self):
        values = [1, 2, 2, 3, 3, 3, 4, 3, 3, 3]

        self.assertEqual(list(filter_repetition(values)), [1, 2, 3, 4, 3])

    def test_with_remaining(self):
        self.assertEqual(list(with_remaining([])), [])
        self.assertEqual(list(with_remaining([1, 2, 3, 4])), [
            (1, [2, 3, 4]),
            (2, [3, 4]),
            (3, [4]),
            (4, []),
        ])


if __name__ == '__main__':
    unittest.main()
