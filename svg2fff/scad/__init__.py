# noinspection SpellCheckingInspection
reserved_words = {
    "abs", "acos", "asin", "assert", "assign", "atan", "atan2", "ceil", "child", "children", "chr",
    "circle", "color", "concat", "cos", "cross", "cube", "cylinder", "difference", "dxf_cross",
    "dxf_dim", "dxf_linear_extrude", "dxf_rotate_extrude", "each", "echo", "else", "exp", "false",
    "floor", "for", "function", "group", "hull", "if", "import", "import_dxf", "import_off",
    "import_stl", "include", "intersection", "intersection_for", "is_bool", "is_function",
    "is_list", "is_num", "is_string", "is_undef", "len", "let", "linear_extrude", "ln", "log",
    "lookup", "max", "min", "minkowski", "mirror", "module", "multmatrix", "norm", "offset", "ord",
    "parent_module", "polygon", "polyhedron", "pow", "projection", "rands", "render", "resize",
    "rotate", "rotate_extrude", "round", "scale", "search", "sign", "sin", "sphere", "sqrt",
    "square", "str", "surface", "tan", "text", "translate", "true", "undef", "union", "use",
    "version", "version_num"
}

from .identifier import Identifier
from .string_literal import StringLiteral
from .writer import Writer
from .renderer import Renderer
