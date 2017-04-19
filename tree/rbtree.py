#! /usr/bin/env python
from binary_search_tree import BinarySearchTree, TreeNode


class RBNode(TreeNode):
    RED = 1
    BLACK = 0

    def __init__(self, key):
        super(RBNode, self).__init__(key)
        self.color = self.RED


class RBTree(BinarySearchTree):
    def __init__(self):
        super(RBTree, self).__init__()

    def insert(self, new_node):
        pass

    def search(self, key):
        pass

    def delete(self, key):
        pass


if __name__ == '__main__':
    pass
