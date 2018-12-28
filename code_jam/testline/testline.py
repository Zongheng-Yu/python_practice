# -*- coding: utf-8 -*-
import sys


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
            user_list.append(set(map(lambda x: x-1, map(int, fd.readline().strip().split(r',')))))

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


def main():
    filename = parse_arg()
    test_line_num, user_list = parse_input_file(filename)
    search_solution([False]*test_line_num, user_list, 0)
    print(solution_number)
    sum = 0
    set1 = user_list[0]
    for set2 in user_list[1:]:
        tmp = 1
        for each in range(len(set1 & set2)):
            tmp *= (each + 1)
        sum += tmp
        sum += len(set1 - set2) * len(set2)
        sum += len(set2 - set1) * len(set1)
        set1 = set1 | set2

    print(sum)


if __name__ == '__main__':
    main()
