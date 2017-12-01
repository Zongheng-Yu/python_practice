#! /usr/bin/env python
"""
Basic definition of graph
"""
from collections import deque


class Vertex(object):
    WHITE = 0
    GRAY = 1
    BLACK = 2
    INVALID_DISTANCE = float('inf')

    def __init__(self, key):
        self._key = key
        self._adjacencies = {}

    def add_adj(self, adj, weight):
        """
        Add a adjacency
        :param adj: destination vertex
        :param weight: the weight of the edge
        :return: None
        """
        if not isinstance(adj, Vertex):
            raise TypeError('Expent an instance of Vertex, Given: %s' % adj)

        if adj in self._adjacencies:
            raise KeyError('%s already have adjacency: %s' % (self, adj))

        self._adjacencies[adj] = weight

    def set_weight(self, adj, weight):
        if adj not in self._adjacencies:
            raise KeyError('Adjacency not exist: %s' % adj)

        self._adjacencies[adj] = weight

    @property
    def key(self):
        return self._key

    @property
    def adjacencies(self):
        return self._adjacencies.keys()

    def get_edges(self):
        edges = []
        for dst in self._adjacencies:
                edges.append(Edge(self, dst, self._adjacencies[dst]))

        return edges

    def get_weight(self, dst):
        if dst in self._adjacencies:
            return self._adjacencies[dst]
        raise ValueError('Edge not found: %s---->%s' % (str(self), str(dst)))

    def __str__(self):
        return str(self._key)


class Edge(object):
    def __init__(self, source, destination, weight=None):
        self.src = source
        self.dst = destination
        self._weight = weight

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self.src.set_weight(self.dst, weight)

    def __str__(self):
        return '%s--%d-->%s' % (str(self.src), self.weight, str(self.dst))


class Graph(object):
    def __init__(self, graph_description=None):
        """
        Init graph with a dict structure. eg.
         {
             'a':{'b':2, 'c':1, 'd':3},
             'b':{'c':2},
             'c':{'d':3},
             'd':{}
         }
        """
        # dict of key:vertex pair
        self._graph = {}
        if graph_description is None:
            return

        if not isinstance(graph_description, dict):
            raise TypeError('Expect a dict, Given: %s' % graph_description)

        for origin in graph_description:
            if origin not in self._graph:
                self.add_vertex(origin)
            # with weight given
            if isinstance(graph_description[origin], dict):
                for destination in graph_description[origin]:
                    self.add_edge(origin, destination, graph_description[origin][destination])
            # without weight
            elif isinstance(graph_description[origin], set):
                for destination in graph_description[origin]:
                    self.add_edge(origin, destination, None)
            else:
                raise TypeError('Expect a dict or set, Given: %s' % graph_description[origin])

    def add_vertex(self, key):
        if key in self._graph:
            raise KeyError('key already exists: %s' % key)
        self._graph[key] = vertex = Vertex(key)
        return vertex

    def add_edge(self, src, dst, weight):
        if src not in self._graph:
            self.add_vertex(src)

        if dst not in self._graph:
            self.add_vertex(dst)

        self.get_vertex(src).add_adj(self.get_vertex(dst), weight)

    def get_vertex(self, key):
        if key in self._graph:
            return self._graph[key]
        raise KeyError('No such vertex in graph: %s' % key)

    def get_all_vertexes(self):
        return self._graph.values()

    def get_all_keys(self):
        return self._graph.keys()

    def get_edge(self, src, dst):
        if src in self._graph and dst in self._graph:
            return Edge(self.get_vertex(src), self.get_vertex(dst), self.get_weight(src, dst))
        raise ValueError('Edge not found: %s---->%s' % (src, dst))

    def get_weight(self, src, dst):
        return self.get_vertex(src).get_weight(self.get_vertex(dst))

    def set_weight(self, src, dst, weight):
        return self.get_vertex(src).set_weight(dst, weight)

    def get_all_edges(self):
        edges = []
        for vertex in self._graph.values():
            edges += vertex.get_edges()

        return edges

    def get_transposed_graph(self):
        gt = Graph()
        for vertex in self.get_all_vertexes():
            gt.add_vertex(vertex.key)

        for edge in self.get_all_edges():
            gt.add_edge(edge.dst.key, edge.src.key, edge.weight)

        return gt

    def _init_bfs(self):
        for vertex in self.get_all_vertexes():
            vertex.color = Vertex.WHITE
            vertex.distance = Vertex.INVALID_DISTANCE
            vertex.pre = None

    def run_bfs(self, src):
        """
        Run Breadth first search on graph
        :param src: the source vertex to run BFS
        :return:
        """
        src_vertex = self.get_vertex(src)
        self._init_bfs()
        src_vertex.color = Vertex.GRAY
        src_vertex.distance = 0
        queue = deque()
        queue.append(src_vertex)
        while len(queue) > 0:
            vertex = queue.popleft()
            for adj in vertex.adjacencies:
                if adj.color == Vertex.WHITE:
                    queue.append(adj)
                    adj.pre = vertex
                    adj.color = Vertex.GRAY
                    adj.distance = vertex.distance + 1

    def _get_path(self, vertex, out_list):
        if vertex.pre is not None:
            self._get_path(vertex.pre, out_list)
        out_list.append(vertex)

    def get_path(self, key):
        vertex = self.get_vertex(key)
        out_list = list()
        self._get_path(vertex, out_list)
        return out_list


if __name__ == '__main__':
    pass
