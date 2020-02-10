from collections import defaultdict

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
    if not candidates:
        return None

    closest = candidates[0]
    closest_dist = distance(closest, value)

    for candidate in candidates[1:]:
        dist = distance(candidate, value)
        if dist < closest_dist:
            closest = candidate
            closest_dist = dist

    return closest
