import re

from svg2fff.scad import reserved_words


class Identifier:
    @staticmethod
    def is_valid(value: str):
        # OpenSCAD does not seem to document the rules for identifiers, but
        # looking at its lexer.l, it seems that only latin letters, digits, and
        # underscores are allowed. Also, the identifier may not consist solely
        # of digits (though it may start with a digit) and may not be identical
        # to a reserved word.

        # Invalid characters or empty
        if not re.fullmatch(r'[a-zA-Z0-9_]+', value):
            return False

        # Digits only
        if re.fullmatch(r'\d*', value):
            return False

        # Reserved word
        if value in reserved_words:
            return False

        return True

    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError(f"Not a valid identifier: {value}")

        self._value = value

    @property
    def value(self):
        return self._value
