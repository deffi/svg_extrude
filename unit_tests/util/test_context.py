import unittest
from contextlib import contextmanager

from svg_extrude.util.context import conditional_context


class ContextTest(unittest.TestCase):
    def test_conditional_context(self):
        @contextmanager
        def wrapped(x):
            yield [x]

        a = 1
        with wrapped(a) as b:
            self.assertEqual([1], b)

            with wrapped(b) as c:
                self.assertEqual([1], b)
                self.assertEqual([[1]], c)

            with conditional_context(True, wrapped(b), "something") as c:
                self.assertEqual([1], b)
                self.assertEqual([[1]], c)

            with conditional_context(False, wrapped(b), "something") as c:
                self.assertEqual([1], b)
                self.assertEqual("something", c)


if __name__ == '__main__':
    unittest.main()
