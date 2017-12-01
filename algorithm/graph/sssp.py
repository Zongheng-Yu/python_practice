#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Bellman-Ford核心算法
# 对于一个包含n个顶点，m条边的图, 计算源点到任意点的最短距离
# 循环n-1轮，每轮对m条边进行一次松弛操作

# 定理：
# 在一个含有n个顶点的图中，任意两点之间的最短路径最多包含n-1条边
# 最短路径肯定是一个不包含回路的简单路径（回路包括正权回路与负权回路）
# 1. 如果最短路径中包含正权回路，则去掉这个回路，一定可以得到更短的路径
# 2. 如果最短路径中包含负权回路，则每多走一次这个回路，路径更短，则不存在最短路径
# 因此最短路径肯定是一个不包含回路的简单路径，即最多包含n-1条边，所以进行n-1次松弛即可

"""
Single source short path implementation
"""

from graph import Graph, Vertex
from unittest import TestCase, main


class CycleError(Exception):
    pass


def relax(edge):
    if edge.src.distance + edge.weight < edge.dst.distance:
        edge.dst.distance = edge.src.distance + edge.weight
        edge.dst.pre = edge.src


class BellmanFord(object):
    UNREACHABLE = float('inf')

    def __init__(self, graph):
        if not isinstance(graph, Graph):
            raise TypeError('Expect an instance of Graph, given: %s' % graph)
        self._graph = graph

    def run(self, src):
        src_vertex = self._graph.get_vertex(src)
        for vertex in self._graph.get_all_vertexes():
            vertex.distance = self.UNREACHABLE
            vertex.pre = None

        src_vertex.distance = 0
        for i in range(len(self._graph.get_all_vertexes()) - 1):
            for edge in self._graph.get_all_edges():
                relax(edge)

        for edge in self._graph.get_all_edges():
            if edge.src.distance + edge.weight < edge.dst.distance:
                raise CycleError('Negative weight cycle in graph')

        return self

    def _get_path(self, vertex, output):
        if vertex.pre:
            self._get_path(vertex.pre, output)
        output.append(vertex.key)

    def get_path(self, vertex):
        if not isinstance(vertex, Vertex):
            vertex = self._graph.get_vertex(vertex)
        result = []
        self._get_path(vertex, result)
        return result

    def get_distance(self, vertex):
        if not isinstance(vertex, Vertex):
            vertex = self._graph.get_vertex(vertex)
        return vertex.distance


class TestBellmanFord(TestCase):
    def test_bellman_ford(self):
        # """
        #  ___________________3________________
        # /                                    \
        # a-- -3 -->b-- 2 -->c-- 3 -->d-- 2 -->e
        # """
        G = {'a': {'a': 0, 'b': -3, 'e': 3},
             'b': {'b': 0, 'c': 2},
             'c': {'c': 0, 'd': 3},
             'd': {'d': 0, 'e': 2},
             'e': {'e': 0}}

        bf = BellmanFord(Graph(G))
        bf.run('a')
        self.assertEqual(bf.get_distance('a'), 0)
        self.assertEqual(bf.get_path('a'), ['a'])
        self.assertEqual(bf.get_distance('b'), -3)
        self.assertEqual(bf.get_path('b'), ['a', 'b'])
        self.assertEqual(bf.get_distance('c'), -1)
        self.assertEqual(bf.get_path('c'), ['a', 'b', 'c'])
        self.assertEqual(bf.get_distance('d'), 2)
        self.assertEqual(bf.get_path('d'), ['a', 'b', 'c', 'd'])
        self.assertEqual(bf.get_distance('e'), 3)
        self.assertEqual(bf.get_path('e'), ['a', 'e'])
        bf.run('c')
        self.assertEqual(bf.get_distance('a'), BellmanFord.UNREACHABLE)
        self.assertEqual(bf.get_distance('b'), BellmanFord.UNREACHABLE)
        self.assertEqual(bf.get_distance('c'), 0)
        self.assertEqual(bf.get_path('c'), ['c'])
        self.assertEqual(bf.get_distance('d'), 3)
        self.assertEqual(bf.get_path('d'), ['c', 'd'])
        self.assertEqual(bf.get_distance('e'), 5)
        self.assertEqual(bf.get_path('e'), ['c', 'd', 'e'])

    def test_raise_error_when_negative_weight_circle(self):
        # """
        #  ___________________3________________
        #  /         ___-5____________         \
        # /         /                  \       \
        # a-- -3 -->b-- 2 --->c-- 3 -->d-- 2 -->e
        # """
        G = {
                'a': {'b': -3, 'e': 3},
                'b': {'c': 2},
                'c': {'d': 3},
                'd': {'e': 2, 'b': -6},
                'e': {}
            }
        self.assertRaises(CycleError, BellmanFord(Graph(G)).run, 'a')

if __name__ == '__main__':
    main(verbosity=2)
