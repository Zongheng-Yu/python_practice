# -*- coding: utf-8 -*-
import sys
from collections import deque


class Vertex(object):
    WHITE = 0
    GRAY = 1
    BLACK = 2
    UNREACHABLE = float('inf')

    def __init__(self, key):
        self._key = key
        self._neighbors = {}

    def add_neighbor(self, neighbor, weight):
        if not isinstance(neighbor, Vertex):
            raise TypeError('Expent an instance of Vertex, Given: %s' % neighbor)

        if neighbor in self._neighbors:
            raise KeyError('%s already have neighbor: %s' % (self, neighbor))

        self._neighbors[neighbor] = Edge(self, neighbor, weight)

    def set_weight(self, neighbor, weight):
        if neighbor not in self._neighbors:
            raise KeyError('Adjacency not exist: %s' % neighbor)
        self._neighbors[neighbor].weight = weight

    @property
    def key(self):
        return self._key

    @property
    def neighbors(self):
        return self._neighbors.keys()

    def get_edges(self):
        return self._neighbors.values()

    def get_edge(self, neighbor):
        return self._neighbors[neighbor]

    def get_weight(self, dst):
        if dst in self._neighbors:
            return self._neighbors[dst].weight
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
        return self._graph[key]

    def get_all_vertexes(self):
        return self._graph.values()

    def get_all_keys(self):
        return self._graph.keys()

    def get_edge(self, src, dst):
        return self.get_vertex(src).get_edge(self.get_vertex(dst))

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
            vertex.distance = Vertex.UNREACHABLE
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
            for neighbor in vertex.neighbors:
                if neighbor.color == Vertex.WHITE:
                    queue.append(neighbor)
                    neighbor.pre = vertex
                    neighbor.color = Vertex.GRAY
                    neighbor.distance = vertex.distance + 1


def get_residual_capacity(src, dst):
    if dst in src.neighbors:
        edge = src.get_edge(dst)
        return edge.weight - edge.flow
    elif src in dst.neighbors:
        return dst.get_edge(src).flow
    else:
        return 0


def _push(src, dst):
    delta = min(get_residual_capacity(src, dst), src.excess)
    if dst in src.neighbors():
        edge = src.get_edge(dst)
        edge.flow += delta
    else:
        # push flow back to the global source direction
        edge = dst.get_edge(src)
        edge.flow -= delta

    src.excess -= delta
    dst.excess += delta


def _relabel(vertex):
    vertex.height = min(map(lambda x: x.height, vertex.neighbors)) + 1


def _try_push_for_vertex(vertex):
    for neighbor in vertex.neighbors:
        edge = vertex.get_edge(neighbor)
        if vertex.height == neighbor.height + 1 and edge.flow < edge.weight:
            _push(vertex, neighbor)
            return True
    return False


def _try_push(graph):
    for vertex in graph.get_all_vertexes():
        if vertex.excess > 0:
            if _try_push_for_vertex(vertex):
                return True
    return False


def _try_relable_for_vertex(graph, vertex):
    for vertex2 in graph.get_all_vertexes():
        if not (get_residual_capacity(vertex, vertex2) > 0 and vertex.height <= vertex2.height):
            return False
    _relabel(vertex)
    return True


def _try_relable(graph):
    for vertex in graph.get_all_vertexes():
        if vertex.excess > 0:
            if _try_relable_for_vertex(graph, vertex):
                return True

    return False


def _init_preflow(graph, src):
    for vertex in graph.get_all_vertexes():
        vertex.height = 0
        vertex.excess = 0

    for edge in graph.get_all_edges():
        edge.flow = 0

    src.height = len(graph.get_all_vertexes())

    for neighbor in src.neighbors:
        edge = src.get_edge(neighbor)
        edge.flow = edge.weight
        neighbor.excess = edge.weight
        src.excess -= edge.weight


def generic_push_relable(graph, s):
    _init_preflow(graph, s)
    while _try_push(graph) or _try_relable(graph):
        pass



def parse_arg():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        raise Exception("Please provide the input filename")


def parse_input_file(filename):
    with open(filename) as fd:
        item_num = int(fd.readline().strip())
        items = list()
        for i in range(item_num):
            line = list(map(int, fd.readline().strip().split()))
            item = Item(i+1, line[0], line[1:])
            items.append(item)
    return items


def get_residual_graph(graph):
    residual_graph = Graph()
    for edge in graph.get_all_edges():
        if edge.flow > 0:
            residual_graph.add_edge(edge.dst.key, edge.src.key, edge.flow)

        if edge.weight - edge.flow > 0:
            residual_graph.add_edge(edge.src.key, edge.dst.key, edge.weight - edge.flow)

    return residual_graph


INFINIT = 1000


class Item(object):
    def __init__(self, index, value, dependency_list):
        self.index = index
        self.value = value
        self.dependency_list = dependency_list

    def __str__(self):
        return str(self.value) + ": " + str(self.dependency_list)


def get_item_from_index(items, index):
    for each in items:
        if each.index == index:
            return each


def search_solution(items):
    graph = Graph()
    src_key = 'src'
    sink_key = 'sink'
    for each in items[1:]:
        if each.value < 0:
            graph.add_edge(src_key, each, -each.value)
        else:
            graph.add_edge(each, sink_key, each.value)
        for dependency in each.dependency_list:
            graph.add_edge(get_item_from_index(items, dependency), each, INFINIT)

    generic_push_relable(graph, graph.get_vertex(src_key))
    residual_graph = get_residual_graph(graph)
    residual_graph.run_bfs(src_key)
    result = list()
    for vertex in residual_graph.get_all_vertexes():
        if vertex.color == Vertex.WHITE and vertex.key != sink_key:
            result.append(vertex.key)


def main():
    search_solution(parse_input_file(parse_arg()))


if __name__ == '__main__':
    main()
