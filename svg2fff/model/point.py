from collections import namedtuple


class Point(namedtuple("Point", ("x", "y"))):
    """Coordinates are in meters (SI base unit)"""
