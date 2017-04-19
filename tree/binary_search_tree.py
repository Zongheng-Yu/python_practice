#! /usr/bin/env python


def in_order_traversal(root, func):
    if root.has_left():
        in_order_traversal(root.left, func)

    func(root.key)

    if root.has_right():
        in_order_traversal(root.right, func)


def pre_order_traversal(root, func):
    func(root.key)
    if root.has_left():
        pre_order_traversal(root.left, func)

    if root.has_right():
        pre_order_traversal(root.right, func)


def post_order_traversal(root, func):
    if root.has_left():
        post_order_traversal(root.left, func)

    if root.has_right():
        post_order_traversal(root.right, func)

    func(root.key)


def layer_traversal(root, func):
    nodes = [root]
    while len(nodes) > 0:
        node = nodes.pop(0)
        func(node.key)
        if node.has_left():
            nodes.append(node.left)
        if node.has_right():
            nodes.append(node.right)


def insert(root, new_node):
    if root.key > new_node.key:
        if root.has_left():
            insert(root.left, new_node)
        else:
            root.left = new_node
            new_node.parent = root
    elif root.key < new_node.key:
        if root.has_right():
            insert(root.right, new_node)
        else:
            root.right = new_node
            new_node.parent = root
    else:
        raise KeyError('key conflict')


def search(root, key):
    if root is None:
        return None
    if root.key > key:
        return search(root.left, key)
    elif root.key < key:
        return search(root.right, key)
    else:
        return root


def find_max(root):
    if root.has_right():
        return find_max(root.right)
    else:
        return root


def find_min(root):
    if root.has_left():
        return find_min(root.left)
    else:
        return root


def replace_node_with_only_child(node, chiid):
    if node.is_left():
        node.parent.left = chiid
    elif node.is_right():
        node.parent.right = chiid

    if chiid:
        chiid.parent = node.parent

    return chiid


def delete(node):
    if node.has_left() and node.has_right():
        max_node = find_max(node.left)
        max_node.key, node.key = node.key, max_node.key
        delete(max_node)
        return node
    elif node.has_right():
        return replace_node_with_only_child(node, node.right)
    elif node.has_left():
        return replace_node_with_only_child(node, node.left)
    else:
        return replace_node_with_only_child(node, None)


class TreeNode(object):
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None

    def has_left(self):
        return True if self.left else False

    def has_right(self):
        return True if self.right else False

    def has_parent(self):
        return True if self.parent else False

    def is_left(self):
        return True if self.has_parent() and self.parent.left is self else False

    def is_right(self):
        return True if self.has_parent() and self.parent.right is self else False


class BinarySearchTree(object):
    def __init__(self):
        self._root = None
        self._size = 0

    @property
    def size(self):
        return self._size

    def insert(self, key):
        new_node = TreeNode(key)
        if self._root is None:
            self._root = new_node
        else:
            insert(self._root, new_node)

        self._size += 1

    def search(self, key):
        return search(self._root, key)

    def delete(self, key):
        node = self.search(key)
        if node is None:
            raise KeyError('no such key: ' + str(key))

        if node.has_parent():
            delete(node)
        else:
            self._root = delete(node)

        self._size -= 1

    def max(self):
        if self._size > 0:
            return find_max(self._root).key
        else:
            raise ValueError('Empty tree')

    def min(self):
        if self._size > 0:
            return find_min(self._root).key
        else:
            raise ValueError('Empty tree')

    def in_order_traversal(self, func):
        in_order_traversal(self._root, func)

    def pre_order_traversal(self, func):
        pre_order_traversal(self._root, func)

    def post_order_traversal(self, func):
        post_order_traversal(self._root, func)

    def layer_traversal(self, func):
        layer_traversal(self._root, func)
