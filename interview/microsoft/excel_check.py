import json
import re
import sys


class Cell:
    WHITE = 0
    GRAY = 1
    BLACK = 2

    def __init__(self, key, refers):
        self.key = key
        self.refers = refers
        self.color = self.WHITE


def parse(string):
    keys = re.findall(r'([A-Z]{2}\d{2})', string)
    if keys:
        print(keys)
        return keys[0], Cell(keys[0], keys[1:])


def has_circle_by_dfs(graph, cell):
    cell.color = cell.GRAY
    for each in cell.refers:
        if each in graph.keys():
            if graph[each].color == Cell.GRAY or has_circle_by_dfs(graph, graph[each]):
                return True

    cell.color = cell.BLACK
    return False


def solution(strings):
    graph = dict()
    for string in strings:
        key, value = parse(string)
        graph[key] = value
        print(key, value.refers)

    for each in graph.values():
        if each.color == each.WHITE and has_circle_by_dfs(graph, each):
            return False

    return True


def main():
    print(solution(["AA00 = 10", "AA01 = AA00 + AB00", "AB00 = 15"]))
    print(solution(["AA00 = 10", "AA01 = 20 + AB00", "AB00 = (AA00 + AA01) * 15"]))


if __name__ == '__main__':
    main()
