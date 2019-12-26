import unittest

from svg2stl.util import filter_repetition


class TestUtil(unittest.TestCase):
    def test_filter_repetition(self):
        input = [1, 2, 2, 3, 3, 3, 4, 3, 3, 3]

        self.assertEqual(list(filter_repetition(input)), [1, 2, 3, 4, 3])


if __name__ == '__main__':
    unittest.main()
