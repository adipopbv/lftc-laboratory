class Node:
    def __init__(self, value: str) -> None:
        self.value = value
        self._left_node = None
        self._right_node = None

    def add_node(self, node):
        """
        Adds a node to the left or right based on the value

        :param node: the node to be added
        :return: nothing
        """
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


class BinarySearchTree:
    def __init__(self) -> None:
        self._root = None

    def add(self, value: str) -> None:
        """
        Adds a node to the tree

        :param value: the value to be added
        :return: nothing
        """
        if self._root is None:
            self._root = Node(value)
        else:
            self._root.add_node(Node(value))