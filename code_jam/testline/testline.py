# -*- coding: utf-8 -*-
import sys
import copy
from multiprocessing import Pool


def parse_arg():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        raise Exception("Please provide the input filename")


def parse_input_file(filename):
    with open(filename) as fd:
        test_line_num, user_num = fd.readline().strip().split(r',')
        test_line_num = int(test_line_num)
        user_num = int(user_num)
        user_list = list()
        for i in range(user_num):
            user_list.append(list(map(int, fd.readline().strip().split(r','))))

    return test_line_num, user_list


def test_solution(solution, user_list):
    for i in range(len(solution)):
        if solution[i] not in user_list[i]:
            return False
    return True


def search_solution(test_line_num, user_list):
    pass

def main():
    filename = parse_arg()
    test_line_num, user_list = parse_input_file(filename)
    solution = [0] * len(user_list)
    for each in range(test_line_num):
        if

if __name__ == '__main__':
    main()
