# -*- coding: utf-8 -*-
import sys
from collections import deque
import copy
from multiprocessing import Pool


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


class Solution(object):
    def __init__(self, items):
        self.item_map = dict()
        for item in items:
            self.item_map[item.index] = item
        self.max_value = 0
        self.result = set()
        self.tmp_result = set()

    def get_all_features(self):
        return list(filter(lambda item: item.value > 0, self.item_map.values()))

    def add_dependency(self, item):
        queue = deque()
        queue.append(item)
        while len(queue) > 0:
            item = queue.popleft()
            for each in item.dependency_list:
                item = self.item_map[each]
                if item not in self.tmp_result:
                    self.tmp_result.add(item)
                    queue.append(item)

    def update(self, features, feature_map):
        self.tmp_result = set()
        for index in range(len(features)):
            if feature_map[index]:
                self.tmp_result.add(features[index])
                self.add_dependency(features[index])
        tmp_value = self.calculate_tmp_result()
        if tmp_value > self.max_value:
            self.max_value = tmp_value
            self.result = self.tmp_result
        elif tmp_value == self.max_value:
            if len(self.result) > len(self.tmp_result):
                self.result = self.tmp_result

    def calculate_tmp_result(self):
        return sum(map(lambda item: item.value, self.tmp_result))


def search_solution(features, feature_map, depth, solution):
    if depth == len(features):
        solution.update(features, feature_map)
        return
    feature_map[depth] = False
    search_solution(features, feature_map, depth+1, solution)
    feature_map[depth] = True
    search_solution(features, feature_map, depth+1, solution)


# def task_generator(features, feature_map, depth, solution):
#
#     feature_map[depth] = False
#     yield(copy.deepcopy(features), copy.deepcopy(feature_map), depth+1, copy.deepcopy(solution))
#     feature_map[depth] = True
#     yield(copy.deepcopy(features), copy.deepcopy(feature_map), depth+1, copy.deepcopy(solution))
#
#
# def task(features, feature_map, depth, solution):
#     search_solution(features, feature_map, depth, solution)
#     return solution


def main():
    items = parse_input_file(parse_arg())
    solution = Solution(items)
    features = solution.get_all_features()
    search_solution(features, [False]*len(features), 0, solution)
    # with Pool() as p:
    #     solutions = p.starmap(task, task_generator(features, [False]*len(features), 0, solution))

    # print(solutions)
    # sorted(solutions, key=lambda x: x.max_value, reverse=True)
    # solution = solutions[0]
    # for each in solutions[1:]:
    #     if each.max_value == solution.max_value and len(each.result) < len(solution.result):
    #         solution = each

    print(solution.max_value)
    for each in sorted(map(lambda x: x.index, solution.result)):
        print(each)


if __name__ == '__main__':
    main()
