class Node:
    def __init__(self, key: int, value: str) -> None:
        self.key = key
        self.value = value
        self._left_node = None
        self._right_node = None

    def add_node(self, node):
        if node.value < self.value:
            if self._left_node is None:
                self._left_node = node
            else:
                self._left_node.add_node(node)
        else:
            if self._right_node is None:
                self._right_node = node
            else:
                self._right_node.add_node(node)

    def get_key_of(self, value: str) -> int:
        if self.value == value:
            return self.key
        left_key = -1
        right_key = -1
        if self._left_node is not None:
            left_key = self._left_node.get_key_of(value)
        if self._right_node is not None:
            right_key = self._right_node.get_key_of(value)
        return left_key if left_key > right_key else right_key

    def to_string(self):
        string = str(self.key) + " : " + str(self.value) + "\n"
        if self._left_node is not None:
            string += self._left_node.to_string()
        if self._right_node is not None:
            string += self._right_node.to_string()
        return string


class BinarySearchTree:
    def __init__(self) -> None:
        self._root = None
        self._node_count = 0

    def add(self, value: str) -> int:
        new_node = Node(self._node_count, value)
        if self._root is None:
            self._root = new_node
        else:
            self._root.add_node(new_node)
        self._node_count += 1
        return new_node.key

    def get_key_of(self, value: str) -> int:
        if self._root is not None:
            if self._root.value == value:
                return self._root.key
            return self._root.get_key_of(value)
        return -1

    def to_string(self):
        if self._root is not None:
            return self._root.to_string()
        return ""
