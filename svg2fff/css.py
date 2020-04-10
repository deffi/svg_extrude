from typing import Optional

import tinycss2 as css

from svg2fff.model import Color


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
