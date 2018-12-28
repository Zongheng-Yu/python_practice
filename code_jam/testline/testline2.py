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
        test_line_num, user_num = map(int, fd.readline().strip().split(r','))
        user_list = list()
        for i in range(user_num):
            user_list.append(list(map(lambda x: x-1, map(int, fd.readline().strip().split(r',')))))

    return test_line_num, user_list


solution_number = 0


def search_solution(test_line_occupation, user_list, depth):
    if depth >= len(user_list):
        global solution_number
        solution_number += 1
        return

    for each in user_list[depth]:
        if not test_line_occupation[each]:
            test_line_occupation[each] = True
            search_solution(test_line_occupation, user_list, depth+1)
            test_line_occupation[each] = False


def task_generator(test_line_occupation, user_list):
    user_list.sort(key=len, reverse=True)
    for each in user_list[0]:
        if not test_line_occupation[each]:
            test_line_occupation[each] = True
            for line in user_list[1]:
                if not test_line_occupation[line]:
                    test_line_occupation[line] = True
                    yield (copy.deepcopy(test_line_occupation), copy.deepcopy(user_list), 2)
                    test_line_occupation[line] = False
            test_line_occupation[each] = False


def sub_process(test_line_occupation, user_list, depth):
    global solution_number
    solution_number = 0
    search_solution(test_line_occupation, user_list, depth)
    return solution_number


def main():
    filename = parse_arg()
    test_line_num, user_list = parse_input_file(filename)
    with Pool() as p:
        print(sum(p.starmap(sub_process, task_generator([False]*test_line_num, user_list))))


if __name__ == '__main__':
    main()
