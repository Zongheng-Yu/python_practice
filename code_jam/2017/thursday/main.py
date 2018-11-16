#! /usr/bin/env python
import sys
from pythonds.graphs import PriorityQueue, Graph, Vertex
from prim import prim


def mst(matrix, s):
    for i in range(len(matrix)):
        matrix[i][i] = sys.maxint

    graph = Graph()
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            graph.addEdge(i, j, matrix[i][j])
    prim(graph, graph.getVertex(s))
    sum = 0
    for each in graph:
        sum += each.getDistance()

    return sum

def main(input_file, output_file):
    case_name = None
    matrix = []
    with open(input_file) as fd:
        case_name = fd.readline().strip()
        node_num = int(fd.readline().strip())
        matrix = [[sys.maxint for j in range(node_num)] for j in range(node_num)]
        for i in range(node_num):
            weights = fd.readline().split()
            for j in range(len(weights)):
                matrix[i][j] = int(weights[j].strip())

        exist_edge_num = int(fd.readline().strip())
        for i in range(exist_edge_num):
            node1, node2 = fd.readline().split()
            node1 = int(node1.strip()) - 1
            node2 = int(node2.strip()) - 1
            matrix[node1][node2] = matrix[node2][node1] = 0

    for each in matrix:
        print each
    sum = mst(matrix, 0)
    print sum
    with open(output_file, 'wb') as fd:
        fd.writelines([case_name + ' ' + str(sum)])
        # fd.writelines(['Case#1: %d' % sum])


if __name__ == '__main__':
    # main('small_input_3.txt', 'small.output')
    main('large_input_8.txt', 'large.output')