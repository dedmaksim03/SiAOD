class Deque:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def add_left(self, item):
        self.items.insert(0, item)

    def add_right(self, item):
        self.items.append(item)

    def remove_right(self):
        return self.items.pop()

    def remove_left(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)
