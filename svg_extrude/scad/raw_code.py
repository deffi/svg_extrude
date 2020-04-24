class RawCode:
    def __init__(self, code: str):
        self._code: str = code

    @property
    def code(self):
        return self._code
