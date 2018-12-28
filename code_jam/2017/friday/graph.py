#! /usr/bin/env python
"""
Basic definition of graph
"""


class Vertex(object):
    WHITE = 0
    BLACK = 1
    GREY = 2

    def __init__(self, key):
        self.key = key
        self.adjacencies = {}
        self.color = self.WHITE

    def add_adj(self, dst, weight):
        self.adjacencies[dst] = weight

    def remove_adj(self, dst):
        self.adjacencies.pop(dst)

    def get_edges(self):
        edges = []
        for dst in self.adjacencies:
                edges.append(Edge(self, dst, self.adjacencies[dst]))

        return edges

    def get_weight(self, dst):
        if dst in self.adjacencies:
            return self.adjacencies[dst]
        raise ValueError('Edge not found: %s---->%s' % (str(self), str(dst)))

    def __str__(self):
        return str(self.key)

    def calculate_coverage(self):
        count = 0
        if self.color == self.WHITE:
            count += 1

        for each in self.adjacencies:
            if each.color == self.WHITE:
                count += 1

        return count

    def find_a_white_adj(self):
        for each in self.adjacencies:
            if each.color == self.WHITE:
                return each

    def __cmp__(self, other):
        return self.calculate_coverage() - other.calculate_coverage()

    def paint(self, color):
        self.color = color
        if color == self.BLACK:
            for each in self.adjacencies:
                if each.color == self.WHITE:
                    each.paint(self.GREY)


class Edge(object):
    def __init__(self, source, destination, weight=None):
        self.src = source
        self.dst = destination
        self.weight = weight

    def __str__(self):
        return '%s--%d-->%s' % (str(self.src), self.weight, str(self.dst))


class Graph(object):
    def __init__(self, graph=None):
        """
        Init graph with a dict structure. eg.
         {
             'a':{'b':2, 'c':1, 'd':3},
             'b':{'c':2},
             'c':{'d':3},
             'd':{}
         }
        """
        self._graph = {}
        if graph:
            for key in graph:
                if key not in self._graph:
                    self.add_vertex(key)
                for dst in graph[key]:
                    self.add_edge(key, dst, graph[key][dst])

    def add_vertex(self, key):
        if key in self._graph:
            raise KeyError('key already exists: %s' % key)
        self._graph[key] = vertex = Vertex(key)
        return vertex

    def get_vertex(self, key):
        if key in self._graph:
            return self._graph[key]
        raise KeyError('No such vertex in graph: %s' % key)

    def get_all_vertexes(self):
        return self._graph.values()

    def get_all_keys(self):
        return self._graph.keys()

    def add_edge(self, src, dst, weight):
        if src not in self._graph:
            self.add_vertex(src)

        if dst not in self._graph:
            self.add_vertex(dst)

        self.get_vertex(src).add_neighbor(self.get_vertex(dst), weight)

    def get_weight(self, src, dst):
        return self.get_vertex(src).get_weight(self.get_vertex(dst))

    def get_edge(self, src, dst):
        if src in self._graph and dst in self._graph:
            return Edge(self.get_vertex(src), self.get_vertex(dst), self.get_weight(src, dst))
        raise ValueError('Edge not found: %s---->%s' % (src, dst))

    def get_all_edges(self):
        edges = []
        for vertex in self._graph.values():
            edges += vertex.get_edges()

        return edges

    def remove_edge(self, k1, k2):
        self.get_vertex(k1).remove_adj(self.get_vertex(k2))

    def remove_vertex(self, k1):
        self._graph.pop(k1)


