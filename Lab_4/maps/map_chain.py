class MapChain:

    def __init__(self, length):
        self.length = length
        self.map = [SlotChain() for _ in range(length)]

    def hash_function(self, val):
        return val % self.length

    def put(self, key, val):
        index = self.hash_function(val)
        if self.map[index].get_key() is None:
            self.map[index] = SlotChain(key, val)
        else:
            self.map[index].put_next_number(key, val)

    def get(self, val):
        index = self.hash_function(val)
        if self.map[index].get_val() == val:
            return self.map[index].get_key()
        else:
            return self.map[index].get_next_number(val)


class SlotChain:

    def __init__(self, key=None, val=None, next_number=None):
        self.val = val  # Значение числа
        self.key = key  # Номер в изначальной последовательности
        self.next_number = next_number

    def put_next_number(self, key, val):
        if self.next_number is None:
            self.next_number = SlotChain(key, val)
        else:
            self.next_number.put_next_number(key, val)

    def get_next_number(self, val):
        if val == self.val:
            return self.key
        elif self.next_number is None:
            return None
        else:
            return self.next_number.get_next_number(val)

    def get_key(self):
        return self.key

    def get_val(self):
        return self.val

    def get_next_number_object(self):
        return self.next_number
