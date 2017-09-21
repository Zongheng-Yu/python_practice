#! /usr/bin/env python
import sys
from graph import Graph, Vertex


def mc2(graph):
    count = 0
    for each in graph.get_all_vertexes():
        if len(each.adjacencies) == 0:
            each.paint(Vertex.BLACK)
            count += 1
        elif len(each.adjacencies) == 1:
            if each.color == Vertex.WHITE:
                each.adjacencies.keys()[0].paint(Vertex.BLACK)
                count += 1
    count += mc(graph)
    return count


def mc(graph):
    arr = graph.get_all_vertexes()
    arr.sort()
    count = 0
    while len(arr) > 0:
        vertex =  arr.pop()
        if vertex.calculate_coverage() > 0:
            vertex.paint(vertex.BLACK)
            count += 1
        else:
            break

    return count


def main(input_file, output_file, alg):
    graphs = []
    with open(input_file) as fd:
        case_num = int(fd.readline().strip())
        for i in range(case_num):
            graph = Graph()
            line = fd.readline().split()
            node_num = int(line[0].strip())
            for j in range(node_num):
                graph.add_vertex(j+1)

            for j in range(1, len(line), 2):
                graph.add_edge(int(line[j].strip()), int(line[j+1].strip()), 1)
                graph.add_edge(int(line[j+1].strip()), int(line[j].strip()), 1)
            graphs.append(graph)

    result_srt_pattren = 'Case #%d:%d\n'
    result_lines = []
    for i in range(len(graphs)):
        if alg == 1:
            result = mc(graphs[i])
        elif alg == 2:
            result = mc2(graphs[i])
        result_lines.append(result_srt_pattren % (i + 1, result))

    with open(output_file, 'wb') as fd:
        fd.writelines(result_lines)


if __name__ == '__main__':
    main('bts_deployment_small_1497230644446', 'small.output', 1)
    main('bts_deployment_large_1497230652539', 'large.output', 1)
    main('bts_deployment_small_1497230644446', 'small.output_2', 2)
    main('bts_deployment_large_1497230652539', 'large.output_2', 2)