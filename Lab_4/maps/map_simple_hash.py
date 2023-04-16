class MapSimpleHash:

    def __init__(self, length):
        self.length = length
        self.map = [Slot() for _ in range(length)]

    def hash_function(self, val):
        return val % self.length

    def put(self, key, val):
        index = self.hash_function(val)
        self.map[index] = Slot(key, val)

    def get(self, val):
        index = self.hash_function(val)
        return self.map[index].get_key()


class Slot:

    def __init__(self, key=None, val=None):
        self.val = val  # Значение числа
        self.key = key  # Номер в изначальной последовательности

    def get_key(self):
        return self.key
