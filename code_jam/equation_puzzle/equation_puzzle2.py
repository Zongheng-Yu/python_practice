# -*- coding: utf-8 -*-
import sys
import re
import copy
from multiprocessing import Pool


NUMBER_COUNT = 10


def parse_arg():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        raise Exception("Please provide the input filename")


def parse_input_file(filename):
    with open(filename) as fd:
        raw_string = fd.readline()

    char_map = dict()
    result = re.match(r'^\s*(\w+)\s*\*\s*(\w+)\s*=\s*(\w+)\s*$', raw_string)
    if result:
        left = result.groups()[0]
        right = result.groups()[1]
        result = result.groups()[2]
    else:
        raise Exception('Wrong format: ' + raw_string)

    for char in left + right + result:
        if char not in char_map:
            char_map[char] = CharItem(char)
    char_map[left[0]].is_leading = True
    char_map[right[0]].is_leading = True
    char_map[result[0]].is_leading = True
    return list(char_map.values()), Equation(left, right, result, raw_string)


class CharItem(object):
    def __init__(self, char, value=-1, is_leading=False):
        self.char = char
        self.value = value
        self.is_leading = is_leading


class Equation(object):
    def __init__(self, left, right, result, raw_string):
        self.left = left
        self.right = right
        self.result = result
        self._raw_string = raw_string
        self._solutions = list()

    def test_equation(self, char_items):
        left = self._to_int(self.left, char_items)
        right = self._to_int(self.right, char_items)
        result = self._to_int(self.result, char_items)
        if left * right == result:
            solution = self._raw_string
            for item in char_items:
                solution = solution.replace(item.char, str(item.value))
            self._solutions.append(solution)

    @staticmethod
    def _to_int(string, char_items):
        num = 0
        for char in string:
            for item in char_items:
                if char == item.char:
                    num = num*10 + item.value
        return num

    @property
    def solutions(self):
        return self._solutions


def search_result(char_items, number_occupation, depth, equation):
    if depth == len(char_items):
        equation.test_equation(char_items)
        return

    if

    for i in range(NUMBER_COUNT):
        if not(number_occupation[i] or (char_items[depth].is_leading and i == 0)):
            number_occupation[i] = True
            char_items[depth].value = i
            search_result(char_items, number_occupation, depth+1, equation)
            number_occupation[i] = False


def task(char_items, number_occupation, depth, equation):
    search_result(char_items, number_occupation, depth, equation)
    return equation.solutions


def task_generator(char_items, equation):
    number_occupation = [False] * NUMBER_COUNT
    for i in range(NUMBER_COUNT):
        if not (char_items[0].is_leading and i == 0):
            number_occupation[i] = True
            char_items[0].value = i
            yield (copy.deepcopy(char_items), copy.deepcopy(number_occupation), 1, copy.deepcopy(equation))
            number_occupation[i] = False


def main():
    filename = parse_arg()
    char_items, equation = parse_input_file(filename)
    with Pool() as p:
        result = p.starmap(task, task_generator(char_items, equation))
    for solutions in result:
        for each in solutions:
            print(each)


if __name__ == '__main__':
    main()
