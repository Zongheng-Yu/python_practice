#! /usr/bin/env python

from operator import add
from functools import partial
from unittest import main, TestCase


def test_sum(sum, num1=0, num2=0):
    return sum == num1 + num2


class TestPartial(TestCase):
    def test_partial(self):
        add2 = partial(add, 2)
        self.assertEqual(add2(1), 3)
        base2 = partial(int, base=2)
        self.assertEqual(base2('1111111111111111'), 65535)
        test_sum4 = partial(test_sum, num1=1, num2=3)
        self.assertTrue(test_sum4(4))
        test_sum3 = partial(test_sum, num2=3)
        self.assertTrue(test_sum3(3))
        test_sum1 = partial(test_sum, num1=1)
        self.assertTrue(test_sum1(1))


if __name__ == '__main__':
    main()