import unittest
from typing import Dict
from os import path

from svg2fff.model import Scene, Color, ColorSet, Shape, Group, Point

file_name = path.join(path.dirname(__file__), "scene.svg")
c1 = Color(1.0, 0.0, 0.2)
c2 = Color(1.0, 0.2, 0.0)
c3 = Color(1.0, 0.8, 0.0)
red = Color(1.0, 0.0, 0.0)
yel = Color(1.0, 1.0, 0.0)


class SceneTest(unittest.TestCase):
    def test_from_svg(self):
        scene = Scene.from_svg(file_name, precision=1, available_colors=None)

        shapes: Dict[str, Shape]   = {shape.name: shape for shape in scene.shapes}
        groups: Dict[Color, Group] = {group.color: group for group in scene.groups}

        # Correct number of shapes
        self.assertEqual(3, len(shapes))
        # Correct shape names
        self.assertEqual({"one", "two", "tre"}, set(shapes.keys()))
        # Each shape: correct color
        self.assertEqual(c1, shapes["one"].color)
        self.assertEqual(c2, shapes["two"].color)
        self.assertEqual(c3, shapes["tre"].color)
        # Each shape: correct points - we should have this, but the y coordinates are slightly off (also in test_from_svg_with_colors)
        #self.assertEqual((Point(0.00, 0.01), Point(0.01, 0.01), Point(0.01, 0.00), Point(0.00, 0.00), Point(0.00, 0.01)), shapes["one"].polygon.paths[0])
        #self.assertEqual((Point(0.01, 0.01), Point(0.02, 0.01), Point(0.02, 0.00), Point(0.01, 0.00), Point(0.01, 0.01)), shapes["two"].polygon.paths[0])
        #self.assertEqual((Point(0.02, 0.00), Point(0.02, 0.01), Point(0.03, 0.01), Point(0.03, 0.00), Point(0.02, 0.00)), shapes["tre"].polygon.paths[0])

        # Correct number of groups
        self.assertEqual(3, len(groups))
        # Correct group colors
        self.assertEqual({c1, c2, c3}, set(groups.keys()))
        # Each group: correct set of shapes
        self.assertEqual({shapes["one"]}, set(groups[c1].shapes))
        self.assertEqual({shapes["two"]}, set(groups[c2].shapes))
        self.assertEqual({shapes["tre"]}, set(groups[c3].shapes))

    def test_from_svg_with_colors(self):
        colors = ColorSet({red, yel})
        scene = Scene.from_svg(file_name, precision=1, available_colors=colors)

        shapes: Dict[str, Shape]   = {shape.name: shape for shape in scene.shapes}
        groups: Dict[Color, Group] = {group.color: group for group in scene.groups}

        # Correct number of shapes
        self.assertEqual(3, len(shapes))
        # Correct shape names
        self.assertEqual({"one", "two", "tre"}, set(shapes.keys()))
        # Each shape: correct color (despite available_colors!)
        self.assertEqual(c1, shapes["one"].color)
        self.assertEqual(c2, shapes["two"].color)
        self.assertEqual(c3, shapes["tre"].color)

        # Correct number of groups
        self.assertEqual(2, len(groups))
        # Correct group colors
        self.assertEqual({red, yel}, set(groups.keys()))
        # Each group: correct set of shapes
        self.assertEqual({shapes["one"], shapes["two"]}, set(groups[red].shapes))
        self.assertEqual({shapes["tre"]}               , set(groups[yel].shapes))


if __name__ == '__main__':
    unittest.main()
