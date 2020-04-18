import unittest

from svg_extrude.util import Namespace


class NamespaceTest(unittest.TestCase):
    def test_build(self):
        # Build won't modify the known names

        ns = Namespace(str.lower, reserved=["nope", "NOWAY"])

        # Sane names are returned as is
        self.assertEqual("foo", ns.build("foo"))
        self.assertEqual("bar", ns.build("bar"))

        # Non-sane names are sanitized
        self.assertEqual("foo", ns.build("Foo"))
        self.assertEqual("foo", ns.build("FOO"))

        # Appended digits are fine
        self.assertEqual("foo_1", ns.build("foo_1"))
        self.assertEqual("bar_1", ns.build("bar_1"))

        # Reserved words (after sanitizing) are modified
        self.assertEqual("nope_1", ns.build("nope"))
        self.assertEqual("nope_1", ns.build("NOPE"))

        # As said, only if it is a reserved word after sanitizing
        self.assertEqual("noway", ns.build("NOWAY"))

        # Nothing stored
        self.assertEqual(0, len(ns._map))

    def test_get(self):
        # Build will modify the known names

        ns = Namespace(sanitize_identifier=str.lower, reserved=["nope", "NOWAY"])

        # Sane names are returned as is
        self.assertEqual("foo", ns.get("foo"))
        self.assertEqual("bar", ns.get("bar"))

        # Non-sane names are sanitized
        self.assertEqual("qux", ns.get("Qux"))

        # Wait, we've already seen this one before!
        self.assertEqual("foo_1", ns.get("Foo"))
        self.assertEqual("foo_2", ns.get("FOO"))
        self.assertEqual("qux_1", ns.get("QUX"))

        # But we can re-get the same values
        self.assertEqual("foo", ns.get("foo"))
        self.assertEqual("qux", ns.get("Qux"))
        self.assertEqual("foo_1", ns.get("Foo"))
        self.assertEqual("qux_1", ns.get("QUX"))

        # Appended digits are fine
        self.assertEqual("zap_1", ns.get("zap_1"))
        # Others will fill the gap
        self.assertEqual("zap", ns.get("Zap"))
        # But now that one is gone. Also, there is a "zap", and it's not
        # ns.get("zap").
        self.assertEqual("zap_2", ns.get("zap"))

        # If we've already seen this name, the basic name is not modified: we
        # get foo_1_1, not foo_2
        self.assertEqual("foo_1_1", ns.get("foo_1"))

        # Reserved words (after sanitizing) are modified
        self.assertEqual("nope_1", ns.get("nope"))
        self.assertEqual("nope_2", ns.get("NOPE"))

        # As said, only if it is a reserved word after sanitizing
        self.assertEqual("noway", ns.get("NOWAY"))


if __name__ == '__main__':
    unittest.main()
