"""
Topological sort implementation
"""

from graph import Graph
from dfs import DFS
from unittest import TestCase, main


def topological_sort(graph):
    if not isinstance(graph, Graph):
        raise TypeError('Expect an instance of Graph')
    DFS(graph).run()
    return reversed(sorted(graph.get_all_vertexes(), key=lambda x: x.finish))


class TestTopologicalSort(TestCase):
    INPUT_GRAPH = {
        'underpants': {'pants', 'shoes'},
        'pants': {'shoes', 'belt'},
        'belt': {'jacket'},
        'shirt': {'belt', 'tie'},
        'tie': {'jacket'},
        'jacket': {},
        'socks': {'shoes'},
        'watch': {}
    }

    def test_topological_sort(self):
        graph = Graph(self.INPUT_GRAPH)
        result = topological_sort(graph)
        for each in result:
            print each, each.discover, each.finish

    def test_raise_type_error_when_invalid_para(self):
        self.assertRaises(TypeError, topological_sort, 'aaa')


if __name__ == '__main__':
    main()
