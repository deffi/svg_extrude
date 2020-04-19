import unittest

from svg_extrude.util import filter_repetition, each_with_remaining, group_by, arg_min, identity


class UtilTest(unittest.TestCase):
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

    def test_group_by(self):
        self.assertEqual(dict(), group_by([], len))

        words = ("foo", "bar", "waldo", "fred", "qux", "hello", "a")
        self.assertEqual({
            1: ["a"],
            3: ["foo", "bar", "qux"],
            4: ["fred"],
            5: ["waldo", "hello"],
        }, group_by(words, len))

    def test_arg_min(self):
        self.assertEqual(None, arg_min([], len))

        words = "foo", "bar", "waldo", "a", "fred", "qux", "hello"
        self.assertEqual("a", arg_min(words, len))
        self.assertEqual("waldo", arg_min(words, lambda x: -len(x)))

    def test_identity(self):
        for x in [0, 1, "", "1", None, identity, UtilTest]:
            self.assertIs(x, identity(x))


if __name__ == '__main__':
    unittest.main()
