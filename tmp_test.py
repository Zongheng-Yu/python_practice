#!/usr/bin/env python
import re
from collections import OrderedDict
from struct import pack


class A(object):
    def __init__(self):
        pass

    def __eq__(self, other):
        pass


def modify(a):
    a = 1


if __name__ == '__main__':
    a = A()
    print a
    modify(a)
    print a
    a = pack("!III", 1, 2, 3)
    print type(a)
    print len(a)
    print str(a)
    for each in a:
        print a

