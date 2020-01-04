import tinycss2 as css

from svg2stl.model import Color


def extract_color(svg_object):
    style = svg_object.style
    declarations = css.parse_declaration_list(style)
    for declaration in declarations:
        if isinstance(declaration, css.ast.Declaration):
            if declaration.lower_name == "fill":
                if declaration.value:
                    value = declaration.value[0]
                    if isinstance(value, css.ast.HashToken):
                        return Color.from_html(value.value)
    return None
