"""
Unit test of graph algorithm
"""

from unittest import main, TestCase
from graph import Graph, Vertex, CycleError


class TestGraph(TestCase):
    INPUT_GRAPH = {
         'a': {'b': 2, 'c': 1, 'd': 3},
         'b': {'c': 2},
         'c': {'d': 3},
         'd': {}
    }
    INPUT_NO_WEIGHT_GRAPH = {
         'a': {'b', 'c', 'd'},
         'b': {'c'},
         'c': {'d'},
         'd': {}
    }
    INPUT_VERTEX_NUM = 4
    INPUT_EDGE_NUM = 5

    def test_init_graph_with_dict(self):
        graph = Graph(self.INPUT_GRAPH)
        self.assertEqual(len(graph.get_all_vertexes()), self.INPUT_VERTEX_NUM)
        self.assertEqual(len(graph.get_all_edges()), self.INPUT_EDGE_NUM)
        self.assertEqual({'a', 'b', 'c', 'd'}, set(graph.get_all_keys()))
        self.assertTrue(isinstance(graph.get_vertex('a'), Vertex))
        self.assertTrue(isinstance(graph.get_vertex('b'), Vertex))
        self.assertTrue(isinstance(graph.get_vertex('c'), Vertex))
        self.assertTrue(isinstance(graph.get_vertex('d'), Vertex))
        self.assertEqual(graph.get_edge('a', 'b').weight, 2)
        self.assertEqual(graph.get_edge('a', 'c').weight, 1)
        self.assertEqual(graph.get_edge('a', 'd').weight, 3)
        self.assertEqual(graph.get_edge('b', 'c').weight, 2)
        self.assertEqual(graph.get_edge('c', 'd').weight, 3)

    def test_init_graph_without_weight(self):
        graph = Graph(self.INPUT_NO_WEIGHT_GRAPH)
        self.assertEqual(len(graph.get_all_vertexes()), self.INPUT_VERTEX_NUM)
        self.assertEqual(len(graph.get_all_edges()), self.INPUT_EDGE_NUM)
        self.assertEqual({'a', 'b', 'c', 'd'}, set(graph.get_all_keys()))
        self.assertTrue(isinstance(graph.get_vertex('a'), Vertex))
        self.assertTrue(isinstance(graph.get_vertex('b'), Vertex))
        self.assertTrue(isinstance(graph.get_vertex('c'), Vertex))
        self.assertTrue(isinstance(graph.get_vertex('d'), Vertex))
        self.assertIsNone(graph.get_edge('a', 'b').weight)
        self.assertIsNone(graph.get_edge('a', 'c').weight)
        self.assertIsNone(graph.get_edge('a', 'd').weight)
        self.assertIsNone(graph.get_edge('b', 'c').weight)
        self.assertIsNone(graph.get_edge('c', 'd').weight)

    def test_init_graph_with_invalid_param(self):
        self.assertRaises(TypeError, Graph, 'invalid param')
        self.assertRaises(TypeError, Graph, {'a': 'b'})

    def test_add_vertex_and_edge(self):
        graph = Graph(self.INPUT_GRAPH)
        graph.add_vertex('e')
        self.assertTrue(isinstance(graph.get_vertex('e'), Vertex))
        self.assertEqual(len(graph.get_all_vertexes()), self.INPUT_VERTEX_NUM + 1)
        graph.add_edge('d', 'e', 5)
        self.assertEqual(len(graph.get_all_edges()), self.INPUT_EDGE_NUM + 1)
        self.assertEqual(graph.get_edge('d', 'e').weight, 5)

    def test_duplicate_vertex_cannot_be_added(self):
        graph = Graph()
        graph.add_vertex('a')
        self.assertRaises(KeyError, graph.add_vertex, 'a')

    def test_duplicate_edge_cannot_be_added(self):
        graph = Graph()
        graph.add_edge('a', 'b', 1)
        self.assertRaises(KeyError, graph.add_edge, 'a', 'b', 2)

    def test_assign_weight_to_edge(self):
        graph = Graph()
        graph.add_edge('a', 'b', 1)
        graph.get_edge('a', 'b').weight = 2
        self.assertEqual(graph.get_edge('a', 'b').weight, 2)

    def test_transpose(self):
        graph = Graph(self.INPUT_GRAPH).get_transposed_graph()
        self.assertEqual(len(graph.get_all_vertexes()), self.INPUT_VERTEX_NUM)
        self.assertEqual(len(graph.get_all_edges()), self.INPUT_EDGE_NUM)
        self.assertEqual({'a', 'b', 'c', 'd'}, set(graph.get_all_keys()))
        self.assertTrue(isinstance(graph.get_vertex('a'), Vertex))
        self.assertTrue(isinstance(graph.get_vertex('b'), Vertex))
        self.assertTrue(isinstance(graph.get_vertex('c'), Vertex))
        self.assertTrue(isinstance(graph.get_vertex('d'), Vertex))
        self.assertEqual(graph.get_edge('b', 'a').weight, 2)
        self.assertEqual(graph.get_edge('c', 'a').weight, 1)
        self.assertEqual(graph.get_edge('d', 'a').weight, 3)
        self.assertEqual(graph.get_edge('c', 'b').weight, 2)
        self.assertEqual(graph.get_edge('d', 'c').weight, 3)

    def test_bfs(self):
        input_graph = {
             'a': {'b', 'c', 'd'},
             'b': {'c'},
             'c': {'d'},
             'd': {'e', 'a'},
             'e': {},
             'f': {}
        }
        graph = Graph(input_graph)
        graph.run_bfs('a')
        self.assertEqual([vertex.key for vertex in graph.get_path('a')], ['a'])
        self.assertEqual([vertex.key for vertex in graph.get_path('b')], ['a', 'b'])
        self.assertEqual([vertex.key for vertex in graph.get_path('c')], ['a', 'c'])
        self.assertEqual([vertex.key for vertex in graph.get_path('d')], ['a', 'd'])
        self.assertEqual([vertex.key for vertex in graph.get_path('e')], ['a', 'd', 'e'])
        self.assertEqual([vertex.key for vertex in graph.get_path('f')], ['f'])
        graph.run_bfs('b')
        self.assertEqual([vertex.key for vertex in graph.get_path('a')], ['b', 'c', 'd', 'a'])
        self.assertEqual([vertex.key for vertex in graph.get_path('b')], ['b'])
        self.assertEqual([vertex.key for vertex in graph.get_path('c')], ['b', 'c'])
        self.assertEqual([vertex.key for vertex in graph.get_path('d')], ['b', 'c', 'd'])
        self.assertEqual([vertex.key for vertex in graph.get_path('e')], ['b', 'c', 'd', 'e'])
        self.assertEqual([vertex.key for vertex in graph.get_path('f')], ['f'])
        graph.run_bfs('c')
        self.assertEqual([vertex.key for vertex in graph.get_path('a')], ['c', 'd', 'a'])
        self.assertEqual([vertex.key for vertex in graph.get_path('b')], ['c', 'd', 'a', 'b'])
        self.assertEqual([vertex.key for vertex in graph.get_path('c')], ['c'])
        self.assertEqual([vertex.key for vertex in graph.get_path('d')], ['c', 'd'])
        self.assertEqual([vertex.key for vertex in graph.get_path('e')], ['c', 'd', 'e'])
        self.assertEqual([vertex.key for vertex in graph.get_path('f')], ['f'])
        graph.run_bfs('d')
        self.assertEqual([vertex.key for vertex in graph.get_path('a')], ['d', 'a'])
        self.assertEqual([vertex.key for vertex in graph.get_path('b')], ['d', 'a', 'b'])
        self.assertEqual([vertex.key for vertex in graph.get_path('c')], ['d', 'a', 'c'])
        self.assertEqual([vertex.key for vertex in graph.get_path('d')], ['d'])
        self.assertEqual([vertex.key for vertex in graph.get_path('e')], ['d', 'e'])
        self.assertEqual([vertex.key for vertex in graph.get_path('f')], ['f'])
        graph.run_bfs('f')
        self.assertEqual([vertex.key for vertex in graph.get_path('a')], ['a'])
        self.assertEqual([vertex.key for vertex in graph.get_path('b')], ['b'])
        self.assertEqual([vertex.key for vertex in graph.get_path('c')], ['c'])
        self.assertEqual([vertex.key for vertex in graph.get_path('d')], ['d'])
        self.assertEqual([vertex.key for vertex in graph.get_path('e')], ['e'])
        self.assertEqual([vertex.key for vertex in graph.get_path('f')], ['f'])

    def test_dfs(self):
        input_graph = {
             'a': {'b', 'c', 'd'},
             'b': {'c'},
             'c': {'d'},
             'd': {'e', 'a'},
             'e': {},
             'f': {}
        }
        graph = Graph(input_graph)
        graph.run_dfs(vertex_order=(graph.get_vertex(each) for each in ('a', 'b', 'c', 'd', 'e', 'f')))
        self.assertEqual(graph.get_vertex('a').discover, 0)
        self.assertEqual(graph.get_vertex('a').finish, 9)
        self.assertEqual(graph.get_vertex('f').discover, 10)
        self.assertEqual(graph.get_vertex('f').finish, 11)
        forst = graph.get_dfs_forest()
        self.assertEqual(len(forst), 2)
        for each in forst:
            all_keys = set()
            each.layer_traversal(action=lambda x: all_keys.add(x.key.key))
            if each.key.key == 'f':
                self.assertEqual(all_keys, {'f'})
            else:
                self.assertEqual(each.key.key, 'a')
                self.assertEqual(all_keys, {'a', 'b', 'c', 'd', 'e'})

    def test_topological_sort(self):
        input_graph = {
            'underpants': {'pants', 'shoes'},
            'pants': {'shoes', 'belt'},
            'belt': {'jacket'},
            'shirt': {'belt', 'tie'},
            'tie': {'jacket'},
            'jacket': {},
            'socks': {'shoes'},
            'watch': {}
        }
        graph = Graph(input_graph)
        sorted_keys = [each.key for each in graph.topological_sort()]
        self.assertLess(sorted_keys.index('underpants'), sorted_keys.index('pants'))
        self.assertLess(sorted_keys.index('underpants'), sorted_keys.index('shoes'))
        self.assertLess(sorted_keys.index('pants'), sorted_keys.index('shoes'))
        self.assertLess(sorted_keys.index('pants'), sorted_keys.index('belt'))
        self.assertLess(sorted_keys.index('belt'), sorted_keys.index('jacket'))
        self.assertLess(sorted_keys.index('shirt'), sorted_keys.index('belt'))
        self.assertLess(sorted_keys.index('shirt'), sorted_keys.index('pants'))
        self.assertLess(sorted_keys.index('tie'), sorted_keys.index('jacket'))
        self.assertLess(sorted_keys.index('socks'), sorted_keys.index('shoes'))

    def test_bellman_ford(self):
        # """
        #  ___________________3________________
        # /                                    \
        # a-- -3 -->b-- 2 -->c-- 3 -->d-- 2 -->e
        # """
        input_graph = {
            'a': {'a': 0, 'b': -3, 'e': 3},
            'b': {'b': 0, 'c': 2},
            'c': {'c': 0, 'd': 3},
            'd': {'d': 0, 'e': 2},
            'e': {'e': 0}}

        graph = Graph(input_graph)
        graph.sssp_bellman_ford('a')
        self.assertEqual(graph.get_vertex('a').distance, 0)
        self.assertEqual([each.key for each in graph.get_path('a')], ['a'])
        self.assertEqual(graph.get_vertex('b').distance, -3)
        self.assertEqual([each.key for each in graph.get_path('b')], ['a', 'b'])
        self.assertEqual(graph.get_vertex('c').distance, -1)
        self.assertEqual([each.key for each in graph.get_path('c')], ['a', 'b', 'c'])
        self.assertEqual(graph.get_vertex('d').distance, 2)
        self.assertEqual([each.key for each in graph.get_path('d')], ['a', 'b', 'c', 'd'])
        self.assertEqual(graph.get_vertex('e').distance, 3)
        self.assertEqual([each.key for each in graph.get_path('e')], ['a', 'e'])
        graph.sssp_bellman_ford('c')
        self.assertEqual(graph.get_vertex('a').distance, Vertex.UNREACHABLE)
        self.assertEqual(graph.get_vertex('b').distance, Vertex.UNREACHABLE)
        self.assertEqual(graph.get_vertex('c').distance, 0)
        self.assertEqual([each.key for each in graph.get_path('c')], ['c'])
        self.assertEqual(graph.get_vertex('d').distance, 3)
        self.assertEqual([each.key for each in graph.get_path('d')], ['c', 'd'])
        self.assertEqual(graph.get_vertex('e').distance, 5)
        self.assertEqual([each.key for each in graph.get_path('e')], ['c', 'd', 'e'])

    def test_raise_error_when_negative_weight_circle(self):
        # """
        #  ___________________3________________
        #  /         ___-5____________         \
        # /         /                  \       \
        # a-- -3 -->b-- 2 --->c-- 3 -->d-- 2 -->e
        # """
        input_graph = {
                'a': {'b': -3, 'e': 3},
                'b': {'c': 2},
                'c': {'d': 3},
                'd': {'e': 2, 'b': -6},
                'e': {}
            }
        self.assertRaises(CycleError, Graph(input_graph).sssp_bellman_ford, 'a')


if __name__ == '__main__':
    main(verbosity=2)
