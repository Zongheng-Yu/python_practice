# -*- coding: utf-8 -*-
import sys
from multiprocessing import Pool


def parse_arg():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        raise Exception("Please provide the input filename")


def parse_input_file(filename):
    with open(filename) as fd:
        names = list()
        for each_line in fd:
            names.append(each_line.strip())

    return names


def similarity(str1, str2):

    d = [[0]*(len(str2)+1) for i in range(len(str1)+1)]
    for i in range(1, len(str1) + 1):
        d[i][0] = i

    for i in range(1, len(str2) + 1):
        d[0][i] = i

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i-1] == str2[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(d[i][j-1], d[i-1][j], d[i-1][j-1]) + 1

    return d[len(str1)][len(str2)]


def parse_dataset():
    with open("dataset.txt") as fd:
        name_map = dict()
        for each_line in fd:
            name, gender = each_line.strip().split(r',')
            name_map[name] = gender
    return name_map


def subprocess(name, name_map):
    min_d = 1000
    gender = 'male'
    for refer in name_map:
        d = similarity(name, refer)
        if d < min_d:
            min_d = d
            gender = name_map[refer]

    return name, gender


def task_generator(names, name_map):
    for name in names:
        yield (name, name_map)


def main():
    filename = parse_arg()
    names = parse_input_file(filename)
    name_map = parse_dataset()
    with Pool() as p:
        result = p.starmap(subprocess, task_generator(names, name_map))
    for each in result:
        print(each[0] + ',' + each[1])


if __name__ == '__main__':
    main()
