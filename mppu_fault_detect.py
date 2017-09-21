#! /usr/bin/env python

import re
import os
from time import sleep


def get_all_mppus():
    mppus = []
    result = os.system('ilclifunit -v |grep -i dspm |grep WO-EX')
    pattern = re.compile('(MPPU-\d)')
    for each in result:
        each = each.strip()
        result = pattern.search(each)
        if result:
            mppu = result.groups()[0]
            mppus.append(mppu)
    return mppus


def mppu_guard(mppu):
    print mppu
    result = os.system('ssh %s ps -ef |grep -i udv0.out' % mppu)
    print result
    result


def main():
    all_mppus = get_all_mppus()
    while True:
        for mppu in all_mppus:
            os.system('ssh mppu-0 ps -ef |grep -i udv0.out')
            sleep(1)


if __name__ == '__main__':
    main()
