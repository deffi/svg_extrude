from typing import Optional

import tinycss2 as css

from svg2fff.model import Color

# TODO code duplication

def extract_fill_rule(svg_path) -> Optional[str]:
    """opacity:1;vector-effect:none;fill:#000cff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.66145831;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"""
    style = svg_path.style
    declarations = css.parse_declaration_list(style)
    for declaration in declarations:
        if isinstance(declaration, css.ast.Declaration):
            if declaration.lower_name == "fill-rule":
                if declaration.value:
                    return declaration.value[0].value
    return None


def extract_color(svg_object) -> Optional[Color]:
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
