#!/usr/bin/env python
from graph import Graph, Vertex


class BFS(object):
    def __init__(self, graph):
        if isinstance(graph, Graph):
            self._graph = graph
        else:
            self._graph = Graph(graph)

    def run(self, src):
        if isinstance(src, Vertex):
            vertex = src
        else:
            vertex = self._graph.get_vertex(src)






