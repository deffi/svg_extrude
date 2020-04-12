from typing import Optional

import tinycss2 as css
import tinycss2.ast


def extract_value(style, name: str) -> Optional[str]:
    declarations = css.parse_declaration_list(style)
    for declaration in declarations:
        if isinstance(declaration, css.ast.Declaration):
            if declaration.lower_name == name.lower():
                if declaration.value:
                    return declaration.value[0].value
    return None
