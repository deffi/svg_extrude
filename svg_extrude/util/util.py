from collections import defaultdict
from typing import Iterable


def group_by(items: Iterable, key_function) -> dict:
    """Returns a dict where the keys are determined by calling key_function with
    an item and the values are lists of items that resulted in that key."""
    result = defaultdict(list)
    for item in items:
        result[key_function(item)].append(item)
    return result


def arg_min(candidates: Iterable, target=lambda x: x):
    # """Returns the value from candidates where the target function returns the
    # lowest value. The target function is called once for each candidate."""

    minimum_candidate = None
    minimum_tgt = None

    for candidate in candidates:
        tgt = target(candidate)
        if minimum_tgt is None or tgt < minimum_tgt:
            minimum_candidate = candidate
            minimum_tgt = tgt

    return minimum_candidate


def identity(x):
    return x
