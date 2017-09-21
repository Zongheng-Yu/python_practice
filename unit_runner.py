#!/usr/bin/env python
from unittest import TestCase, TestSuite, TestLoader, TextTestRunner


if __name__ == '__main__':
    suite1 = TestLoader().discover('./Team 1', pattern='case_*_test.py')
    all_tests = TestSuite([suite1])
    TextTestRunner(verbosity=2).run(all_tests)
