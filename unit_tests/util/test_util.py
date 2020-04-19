import unittest

from svg_extrude.util import group_by, arg_min, identity


class UtilTest(unittest.TestCase):

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
