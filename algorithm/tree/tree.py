from collections import deque
from unittest import TestCase, main


class Tree(object):
    def __init__(self, key):
        self._key = key
        self._parent = None
        self._children = list()

    @property
    def key(self):
        return self._key

    def add_subtree(self, subtree):
        if not isinstance(subtree, Tree):
            raise TypeError('subtree should be an instance of Tree: %s' % subtree)
        self._children.append(subtree)
        subtree.parent = self

    def remove_subtree(self, subtree):
        self._children.remove(subtree)

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if not isinstance(parent, Tree):
            raise TypeError('Parent should be a instance of Tree: %s' % parent)
        self._parent = parent

    def layer_traversal(self, action=None):
        queue = deque()
        queue.append(self)
        while len(queue) > 0:
            node = queue.popleft()
            action(node)
            queue.extend(node.children)

    def search_tree(self, key):
        if self._key == key:
            return self
        else:
            for each in self._children:
                result = each.search_tree(key)
                if result is not None:
                    return result

    def has_key(self, key):
        return self.search_tree(key) is not None


class TestTree(TestCase):
    def setUp(self):
        self._tree = root = Tree('a0')
        root.add_subtree(Tree('b0'))
        root.add_subtree(Tree('b1'))
        root.add_subtree(Tree('b2'))
        root.search_tree('b0').add_subtree(Tree('c0'))
        root.search_tree('b0').add_subtree(Tree('c1'))
        root.search_tree('b0').add_subtree(Tree('c2'))
        root.search_tree('b1').add_subtree(Tree('c3'))
        root.search_tree('b1').add_subtree(Tree('c4'))
        root.search_tree('b1').add_subtree(Tree('c5'))
        root.search_tree('b2').add_subtree(Tree('c6'))
        root.search_tree('b2').add_subtree(Tree('c7'))
        root.search_tree('b2').add_subtree(Tree('c8'))
        root.search_tree('c0').add_subtree(Tree('d0'))
        root.search_tree('c0').add_subtree(Tree('d1'))
        root.search_tree('c0').add_subtree(Tree('d2'))
        root.search_tree('c0').add_subtree(Tree('d3'))

    def test_tree(self):
        all_nodes = list()
        self._tree.layer_traversal(action=lambda x: all_nodes.append(x.key))
        self.assertEqual(all_nodes, ['a0', 'b0', 'b1', 'b2', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
                                     'd0', 'd1', 'd2', 'd3'])


if __name__ == '__main__':
    main(verbosity=2)
