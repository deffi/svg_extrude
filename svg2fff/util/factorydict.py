from collections import defaultdict

class factorydict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            value = self.default_factory(key)
            self[key] = value
            return value
