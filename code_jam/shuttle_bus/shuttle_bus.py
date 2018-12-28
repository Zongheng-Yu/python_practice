# -*- coding: utf-8 -*-
import sys


def parse_arg():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        raise Exception("Please provide the input filename")


def parse_input_file(filename):
    with open(filename) as fd:
        column_num, row_num = map(int, fd.readline().strip().split(r','))
        matrix = list()
        for i in range(row_num):
            matrix.append(list(map(int, fd.readline().strip().split(r','))))

    return column_num, row_num, matrix


class Vertex(object):
    WHITE = 0
    GRAY = 1
    BLACK = 2
    UNREACHABLE = float('inf')

    def __init__(self, key):
        self._key = key
        self._adjacencies = {}

    def add_adj(self, adj, weight):
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

    def relax(self):
        if self.src.distance + self.weight < self.dst.distance:
            self.dst.distance = self.src.distance + self.weight
            self.dst.pre = self.src


class Graph(object):
    def __init__(self):
        self._graph = {}

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

        self.get_vertex(src).add_neighbor(self.get_vertex(dst), weight)

    def get_vertex(self, key):
        if key in self._graph:
            return self._graph[key]
        raise KeyError('No such vertex in graph: %s' % key)

    def get_all_vertexes(self):
        return list(self._graph.values())

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

    def sssp_bellman_ford(self, src):
        src_vertex = self.get_vertex(src)
        for vertex in self.get_all_vertexes():
            vertex.distance = Vertex.UNREACHABLE
            vertex.pre = None

        src_vertex.distance = 0
        for i in range(len(self.get_all_vertexes()) - 1):
            for edge in self.get_all_edges():
                edge.relax()

    def get_transposed_graph(self):
        gt = Graph()
        for vertex in self.get_all_vertexes():
            gt.add_vertex(vertex.key)

        for edge in self.get_all_edges():
            gt.add_edge(edge.dst.key, edge.src.key, edge.weight)

        return gt


def output_max_number(column_num, row_num, matrix):
    graph = Graph()
    for i in range(row_num):
        for j in range(column_num):
            if j + 1 < column_num:
                graph.add_edge(str(i)+str(j), str(i)+str(j+1), -matrix[i][j])
            if i + 1 < row_num:
                graph.add_edge(str(i)+str(j), str(i+1)+str(j), -matrix[i][j])

    graph.sssp_bellman_ford('00')
    print(-graph.get_vertex(str(row_num - 1)+str(column_num - 1)).distance)


def main():
    filename = parse_arg()
    output_max_number(*parse_input_file(filename))


if __name__ == '__main__':
    main()
