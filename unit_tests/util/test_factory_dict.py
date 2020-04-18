import unittest

from svg_extrude.util import FactoryDict


class FactoryDictTest(unittest.TestCase):
    def test_factory_dict(self):
        def square(x):
            return x ** 2

        fd = FactoryDict(square)

        # It is a dict
        self.assertEqual({}, fd)
        fd[1] = 2
        fd[2] = 3
        self.assertEqual(2, len(fd))
        self.assertEqual({1, 2}, set(fd))
        self.assertEqual(2, fd[1])
        self.assertEqual(3, fd.get(2, "nope"))

        self.assertNotIn(3, fd)
        self.assertEqual("nope", fd.get(3, "nope"))
        # Calling get did not invoke the factory
        self.assertNotIn(3, fd)

        self.assertEqual(9, fd[3])
        # Now we have key 3
        self.assertIn(3, fd)
        # And we can get it
        self.assertEqual(9, fd.get(3, "nope"))


if __name__ == '__main__':
    unittest.main()
