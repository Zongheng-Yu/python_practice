"""
strongly connected components
"""

from graph import Graph
from dfs import DFS


def strongly_connected_components(graph):
    if not isinstance(graph, Graph):
        raise TypeError('Expect an insrance of a graph, given: %s' % graph)
    DFS(graph).run()
    graph_t = graph.get_transposed_graph()
    decrease_order_list = sorted(graph.get_all_vertexes(), key=lambda x: x.finish, reverse=True)
    dfs_t = DFS(graph_t).run([graph_t.get_vertex(vertex.key) for vertex in decrease_order_list])
    return dfs_t.get_dfs_forest()

