#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
列表解析
[expr for iter_var in iterable if cond_expr]
生成器表达式:
(expr for iter_var in iterable if cond_expr)
"""


def cols(): # example of simple generator
    yield 56
    yield 2
    yield 1


class FindLongestLineInFile(object):
    @staticmethod
    def traditional_way(file_name):
        longest = 0
        with open(file_name, 'rb') as fd:
            for line in fd:
                length = len(line.strip())
                if length > longest:
                    longest = length

        return longest

    @staticmethod
    def list_comps(file_name):
        with open(file_name, 'rb') as fd:
            return max([len(line.strip()) for line in fd])

    @staticmethod
    def generator(file_name):
        with open(file_name, 'rb') as fd:
            return max(len(line.strip()) for line in fd)

if __name__ == '__main__':
    print FindLongestLineInFile.traditional_way("example.log")
    print FindLongestLineInFile.list_comps("example.log")
    print FindLongestLineInFile.generator("example.log")
    for each in cols():
        print each

    print
    a = cols()
    print a
    print a.next()
    print a.next()
    print a.next()
    print a.next()
