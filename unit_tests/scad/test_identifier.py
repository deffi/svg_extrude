import unittest

from svg2fff.scad import Identifier

class IdentifierTest(unittest.TestCase):
    def test_is_valid(self):
        # Valid
        self.assertEqual(True, Identifier.is_valid("foo"))
        self.assertEqual(True, Identifier.is_valid("foo_1"))
        self.assertEqual(True, Identifier.is_valid("1_foo"))

        # Empty
        self.assertEqual(False, Identifier.is_valid(""))

        # Invalid characters
        self.assertEqual(False, Identifier.is_valid("foo bar"))
        self.assertEqual(False, Identifier.is_valid("foo-bar"))
        self.assertEqual(False, Identifier.is_valid("foo.bar"))

        # Reserved word
        self.assertEqual(False, Identifier.is_valid("if"))
        self.assertEqual(False, Identifier.is_valid("module"))
        self.assertEqual(False, Identifier.is_valid("translate"))
        self.assertEqual(False, Identifier.is_valid("cube"))

        # Digits only
        self.assertEqual(False, Identifier.is_valid("123"))


if __name__ == '__main__':
    unittest.main()
