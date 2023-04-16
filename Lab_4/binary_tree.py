class BinarySearchTree:
    """
    Отвечает за организацию дерева в целом: хранит корень, осуществляет вставку новых узлов
    """

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __setitem__(self, k, v):
        self.put(k, v)

    def put(self, key, val=None):
        if self.root:
            self._put(key, self.root, val)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self, key, current_node, val=None):
        if key < current_node.key:
            if current_node.has_left_child():
                self._put(key, current_node.leftChild, val)
            else:
                current_node.leftChild = TreeNode(key, val, parent=current_node)
        else:
            if current_node.has_right_child():
                self._put(key, current_node.rightChild, val)
            else:
                current_node.rightChild = TreeNode(key, val, parent=current_node)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False

    def delete(self, key):
        if self.size > 1:
            node_to_remove = self._get(key, self.root)
            if node_to_remove:
                self.remove(node_to_remove)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self, key):
        self.delete(key)

    def remove(self, currentNode):
        if currentNode.is_leaf():  # Если нет потомков
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.has_both_children():  # Если оба потомка
            succ = currentNode.find_successor()
            succ.splice_out()
            currentNode.key = succ.key
            currentNode.payload = succ.payload

        else:  # Если один потомок
            if currentNode.has_left_child():
                if currentNode.is_left_child():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.is_right_child():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replace_node_data(currentNode.leftChild.key,
                                                  currentNode.leftChild.payload,
                                                  currentNode.leftChild.leftChild,
                                                  currentNode.leftChild.rightChild)
            else:
                if currentNode.is_left_child():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.is_right_child():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replace_node_data(currentNode.rightChild.key,
                                                  currentNode.rightChild.payload,
                                                  currentNode.rightChild.leftChild,
                                                  currentNode.rightChild.rightChild)


def __delitem__(self, key):
    self.delete(key)


class TreeNode:
    """
    Отвечает за конкретный узел: может быть инициализирован, хранит ссылки на предков и потомков
    """

    def __init__(self, key, val=None, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def has_left_child(self):
        return self.leftChild

    def has_right_child(self):
        return self.rightChild

    def is_left_child(self):
        return self.parent and self.parent.leftChild == self

    def is_right_child(self):
        return self.parent and self.parent.rightChild == self

    def is_root(self):
        return not self.parent

    def is_leaf(self):
        return not (self.rightChild or self.leftChild)

    def has_any_children(self):
        return self.rightChild or self.leftChild

    def has_both_children(self):
        return self.rightChild and self.leftChild

    def replace_node_data(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.has_left_child():
            self.leftChild.parent = self
        if self.has_right_child():
            self.rightChild.parent = self

    def find_successor(self):  # Возвращает потомка данного узла
        succ = None
        if self.has_right_child():
            succ = self.rightChild.find_min()
        else:
            if self.parent:
                if self.is_left_child():
                    succ = self.parent
                else:
                    # Если узел - правый потомок своего родителя и сам правого потомка не имеет,
                    # то его преемником будет преемник родителя (исключая сам этот узел).
                    self.parent.rightChild = None
                    succ = self.parent.find_successor()
                    self.parent.rightChild = self
        return succ

    def find_min(self):  # Находит минимальный элемент после себя (самый левый элемент в дереве)
        current = self
        while current.has_left_child():
            current = current.leftChild
        return current

    def splice_out(self):  # Удаление узла (более точечное, чем delete)
        if self.is_leaf():
            if self.is_left_child():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.has_any_children():
            if self.has_left_child():
                if self.is_left_child():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.is_left_child():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent
