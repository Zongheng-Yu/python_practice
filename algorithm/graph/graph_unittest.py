"""
Unit test of graph algorithm
"""


from unittest import main, TestCase
from graph import Graph, Vertex


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


if __name__ == '__main__':
    main(verbosity=2)
