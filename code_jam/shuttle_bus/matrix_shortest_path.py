# -*- coding: utf-8 -*-
import sys


def parse_arg():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        raise Exception("Please provide the input filename")


def parse_input_file(filename):
    with open(filename) as fd:
        column_num, row_num = map(int, fd.readline().strip().split(r','))
        matrix = list()
        for i in range(row_num):
            matrix.append(list(map(int, fd.readline().strip().split(r','))))

    return column_num, row_num, matrix


def search_longest_path(column_num, row_num, matrix):
    for i in range(1, row_num):
        matrix[i][0] += matrix[i-1][0]

    for i in range(1, column_num):
        matrix[0][i] += matrix[0][i-1]

    for i in range(1, row_num):
        for j in range(1, column_num):
            matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1]) + matrix[i][j]

    return matrix[row_num-1][column_num-1]


def main():
    filename = parse_arg()
    print(search_longest_path(*parse_input_file(filename)))


if __name__ == '__main__':
    main()
