from typing import Sequence, Generator


def each_with_remaining(items: Sequence):
    """For each items, yields a tuple with (a) that item, and (b) a slice of the
    original sequence containing all items after that item."""
    for index in range(len(items)):
        yield items[index], items[index+1:]


def filter_repetition(items: Sequence) -> Generator:
    if items:
        i = items[0]
        yield i

        for item in items[1:]:
            if item != i:
                i = item
                yield i
