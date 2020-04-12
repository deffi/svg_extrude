from typing import Iterable, Generator, Sequence
from collections import defaultdict


def filter_repetition(items: Sequence) -> Generator:
    if items:
        i = items[0]
        yield i

        for item in items[1:]:
            if item != i:
                i = item
                yield i


def with_remaining(items: Sequence):
    """For each items, yields a tuple with (a) that item, and (b) a slice of the
    original sequence containing all items after that item."""
    for index in range(len(items)):
        yield items[index], items[index+1:]


def groupby(items: Iterable, key_function) -> dict:
    """Returns a dict where the keys are determined by calling key_function with
    an item and the values are lists of items that resulted in that key."""
    result = defaultdict(list)
    for item in items:
        result[key_function(item)].append(item)
    return result


def closest(candidates: Iterable, value, distance=lambda x, y: abs(x-y)):
    """Returns the value from candidates that is closest to value, according to
    the specified distance function. The distance function should be commutative
    and is called once for each candidate."""
    closest_candidate = None
    closest_dist = None

    for candidate in candidates:
        dist = distance(candidate, value)
        if closest_dist is None or dist < closest_dist:
            closest_candidate = candidate
            closest_dist = dist

    return closest_candidate
