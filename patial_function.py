#! /usr/bin/env python

from operator import add
from functools import partial


def main_test():
    add2 = partial(add, 2)
    print add2(5)
    base2 = partial(int, base=2)
    print base2("1111111111111111")


if __name__ == '__main__':
    main_test()