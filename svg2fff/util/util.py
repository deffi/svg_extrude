from collections import defaultdict

# TODO type hints

def filter_repetition(items):
    if items:
        i = items[0]
        yield i

        for item in items[1:]:
            if item != i:
                i = item
                yield i


def with_remaining(items):
    for index in range(len(items)):
        yield items[index], items[index+1:]


def groupby(items, key):
    result = defaultdict(list)
    for item in items:
        result[key(item)].append(item)
    return result


# TODO default distance function
def closest(candidates, value, distance):
    closest = None
    closest_dist = None

    for candidate in candidates:
        dist = distance(candidate, value)
        if closest_dist is None or dist < closest_dist:
            closest = candidate
            closest_dist = dist

    return closest
