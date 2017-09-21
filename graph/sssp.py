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


from graph import Graph

"""
 ___________________3________________
/                                    \
a-- -3 -->b-- 2 -->c-- 3 -->d-- 2 -->e
"""
G = {'a': {'a': 0, 'b': -3, 'e': 3},
     'b': {'b': 0, 'c': 2},
     'c': {'c': 0, 'd': 3},
     'd': {'d': 0, 'e': 2},
     'e': {'e': 0}}


class CycleError(Exception):
    pass


def relax(edge):
    if edge.src.distance + edge.weight < edge.dst.distance:
        edge.dst.distance = edge.src.distance + edge.weight
        edge.dst.pre = edge.src


def Bellman_Ford(graph_raw, src, infinite=999):
    graph = Graph(graph_raw)
    for vertex in graph.get_all_vertexes():
        vertex.distance = infinite
    graph.get_vertex(src).distance = 0
    graph.get_vertex(src).pre = None

    for i in range(len(graph.get_all_vertexes()) - 1):
        for edge in graph.get_all_edges():
            relax(edge)

    for edge in graph.get_all_edges():
        if edge.src.distance + edge.weight < edge.dst.distance:
            raise CycleError('Negative weight cycle in graph')

    return graph


def print_path(vertex):
    if vertex.pre:
        print_path(vertex.pre)

    print ' %s(%d) ' % (str(vertex), vertex.distance),


def main():
    v0 = 'a'
    graph = Bellman_Ford(G, v0)
    for vertex in graph.get_all_vertexes():
            print_path(vertex)
            print


if __name__ == '__main__':
    main()
