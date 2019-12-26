def filter_repetition(items):
    if items:
        i = items[0]
        yield i

        for item in items[1:]:
            if item != i:
                i = item
                yield i

def render_lines(target, prefix, indent):
    indented_lines = (prefix + indent * depth + line for line, depth in target)
    return "\n".join(indented_lines)
