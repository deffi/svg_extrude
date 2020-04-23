from itertools import count

from svg_extrude.util import FactoryDict


class Namespace:
    def __init__(self, sanitize_identifier, reserved):
        self._map = FactoryDict(self.build)
        self._sanitize_identifier = sanitize_identifier
        self._reserved = reserved

    def get(self, name: str) -> str:
        return self._map[name]

    def build(self, name: str) -> str:
        def candidates():
            identifier = self._sanitize_identifier(name)
            yield identifier
            for i in count(1):
                yield f"{identifier}_{i}"

        existing = set(self._map.values())
        for candidate in candidates():
            if candidate not in self._reserved and candidate not in existing:
                return candidate
