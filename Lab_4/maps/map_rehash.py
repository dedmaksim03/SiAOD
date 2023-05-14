class MapReHash:

    def __init__(self, length):
        for i in range(1, 10):
            if length <= 2**i:
                self.length = 2**i
                break
        self.map = [Slot() for _ in range(self.length)]

    def __len__(self):
        return self.length

    def generator_random(self, operations):  # Генератор псевдослучайной последовательности
        r = 1
        pi = 0
        for i in range(operations):
            r = 5 * r
            r = r % (4 * self.length)
            pi = int(r / 4)
        return pi

    def hash_function(self, val):
        return val % self.length

    def rehash_function(self, val, depth):  # Функция рехэширования
        return (self.hash_function(val) + self.generator_random(depth)) % self.length

    def put(self, key, val):
        index = self.hash_function(val)
        if self.map[index].get_key() is None:
            self.map[index] = Slot(key, val)
        else:
            i = 1
            while self.map[index].get_key() is not None:
                index = self.rehash_function(val, i)
                i += 1
            self.map[index] = Slot(key, val)

    def get(self, val, with_delete=False):
        index = self.hash_function(val)
        if self.map[index].get_val() == val:
            for_return = self.map[index].get_key()
            if with_delete:
                self.map[index] = Slot()
            return for_return
        else:
            i = 1
            while self.map[index].get_val() != val:
                index = self.rehash_function(val, i)
                i += 1
                if i == self.length:
                    return None
            for_return = self.map[index].get_key()
            if with_delete:
                self.map[index] = Slot()
            return for_return



class Slot:

    def __init__(self, key=None, val=None):
        self.val = val  # Значение числа
        self.key = key  # Номер в изначальной последовательности

    def get_key(self):
        return self.key

    def get_val(self):
        return self.val
