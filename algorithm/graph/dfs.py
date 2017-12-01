"""
depth first search
"""

from unittest import TestCase, main

from graph import Graph
from algorithm.tree.tree import Tree


class DFS(object):
    """
    depth first search implementation
    """
    WHITE = 0
    GRAY = 1
    BLACK = 2

    def __init__(self, graph):
        if not isinstance(graph, Graph):
            raise TypeError('Invalid argument')
        self._graph = graph
        self._time = 0
        self._dfs_forest = set()

    def run(self, vertex_order=None):
        """
        run dfs on graph
        :param vertex_order: an iterable object, algorithm will traverse vertexes in given order
        :return: None
        """
        if vertex_order is None:
            vertex_order = self._graph.get_all_vertexes()

        for vertex in self._graph.get_all_vertexes():
            vertex.color = self.WHITE
            vertex.discover = 0
            vertex.finish = 0
            vertex.pre = None

        self._time = 0
        for vertex in vertex_order:
            if vertex.color == self.WHITE:
                self._dfs_forest.add(self._dfs_visit(vertex))

    def _dfs_visit(self, vertex):
        self._time += 1
        vertex.color = self.GRAY
        vertex.discover = self._time
        dfs_tree = Tree(vertex)
        for adj in vertex.adjacencies:
            if adj.color == self.WHITE:
                adj.pre = vertex
                dfs_tree.add_subtree(self._dfs_visit(adj))
        vertex.color = self.BLACK
        self._time += 1
        vertex.finish = self._time
        return dfs_tree

    def get_dfs_forest(self):
        return self._dfs_forest


class TestDfs(TestCase):
    def test_raise_type_error_when_invalid_para(self):
        self.assertRaises(TypeError, DFS, 'aaaa')


if __name__ == '__main__':
    main()
