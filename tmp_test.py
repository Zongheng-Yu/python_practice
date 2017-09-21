#!/usr/bin/env python
import re


if __name__ == '__main__':
    str = '10001111'
    str2 = ''
    for i in range(8):
        str2 += str[7-i]
    print str2
    pure_data = '10001111'*36
    byte_dats = ['%02X' % int(pure_data[i*8:i*8+8][::-1], 2) for i in range(36)]
    print byte_dats


