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
