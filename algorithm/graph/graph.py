#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# 图算法

from collections import deque

from algorithm.tree.tree import Tree


class CycleError(Exception):
    pass


class Vertex(object):
    WHITE = 0
    GRAY = 1
    BLACK = 2
    UNREACHABLE = float('inf')

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

    def relax(self):
        if self.src.distance + self.weight < self.dst.distance:
            self.dst.distance = self.src.distance + self.weight
            self.dst.pre = self.src


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

    def _init_dfs(self):
        self._time = -1
        self._dfs_forest = set()
        for vertex in self.get_all_vertexes():
            vertex.color = Vertex.WHITE
            vertex.discover = 0
            vertex.finish = 0
            vertex.pre = None

    def run_dfs(self, vertex_order=None):
        """
        run dfs on graph
        :param vertex_order: an iterable object, algorithm will traverse vertexes in given order
        :return: None
        """
        if vertex_order is None:
            vertex_order = self.get_all_vertexes()
        self._init_dfs()
        for vertex in vertex_order:
            if vertex.color == Vertex.WHITE:
                self._dfs_forest.add(self._dfs_visit(vertex))

    def _dfs_visit(self, vertex):
        self._time += 1
        vertex.color = Vertex.GRAY
        vertex.discover = self._time
        dfs_tree = Tree(vertex)
        for adj in vertex.adjacencies:
            if adj.color == Vertex.WHITE:
                adj.pre = vertex
                dfs_tree.add_subtree(self._dfs_visit(adj))
        vertex.color = Vertex.BLACK
        self._time += 1
        vertex.finish = self._time
        return dfs_tree

    def get_dfs_forest(self):
        return self._dfs_forest

    def topological_sort(self):
        self.run_dfs()
        return sorted(self.get_all_vertexes(), key=lambda x: x.finish, reverse=True)

    def strongly_connected_components(self):
        sorted_vertexes = self.topological_sort()
        graph_t = self.get_transposed_graph()
        graph_t.run_dfs([graph_t.get_vertex(vertex.key) for vertex in sorted_vertexes])
        return graph_t.get_dfs_forest()

    def mst_kruskal(self):
        pass

    def sssp_bellman_ford(self, src):
        """
        Single source shortest path
        :param src: the key of the source vertex
        :return: None
        """
        # 对于一个包含n个顶点，m条边的图, 计算源点到任意点的最短距离
        # 循环n-1轮，每轮对m条边进行一次松弛操作
        # 定理：
        # 在一个含有n个顶点的图中，任意两点之间的最短路径最多包含n-1条边
        # 最短路径肯定是一个不包含回路的简单路径（回路包括正权回路与负权回路）
        # 1. 如果最短路径中包含正权回路，则去掉这个回路，一定可以得到更短的路径
        # 2. 如果最短路径中包含负权回路，则每多走一次这个回路，路径更短，则不存在最短路径
        # 因此最短路径肯定是一个不包含回路的简单路径，即最多包含n-1条边，所以进行n-1次松弛即可
        src_vertex = self.get_vertex(src)
        for vertex in self.get_all_vertexes():
            vertex.distance = Vertex.UNREACHABLE
            vertex.pre = None

        src_vertex.distance = 0
        for i in range(len(self.get_all_vertexes()) - 1):
            for edge in self.get_all_edges():
                edge.relax()

        for edge in self.get_all_edges():
            if edge.src.distance + edge.weight < edge.dst.distance:
                raise CycleError('Negative weight cycle in graph')


if __name__ == '__main__':
    pass
