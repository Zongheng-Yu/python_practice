import json
import re
import sys


def solution(input_list):
    max_position = 0
    input_list_length = len(input_list)
    for i in range(input_list_length):
        if i > max_position:
            return False
        else:
            if i + input_list[i] > input_list_length:
                return True
            elif i + input_list[i] > max_position:
                max_position = i + input_list[i]


if __name__ == '__main__':
    print(solution([2, 3, 1, 1, 4]))
    print(solution([3, 2, 1, 0, 4]))
