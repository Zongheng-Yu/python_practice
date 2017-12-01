#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
列表解析
[expr for iter_var in iterable if cond_expr]
生成器表达式:
(expr for iter_var in iterable if cond_expr)
"""
from unittest import TestCase, main


def sample_yield(): # example of simple generator
    yield 0
    yield 1
    yield 2


def nested_yield():
    for each in sample_yield():
        yield each
    yield 3


def recurse_yield(depth=0):
    if depth > 0:
        for each in recurse_yield(depth - 1):
            yield each
    yield depth


class TestYield(TestCase):
    def test_generator_expression(self):
        ge = (each for each in range(5))
        self.assertEqual(ge.next(), 0)
        self.assertEqual(ge.next(), 1)
        self.assertEqual(ge.next(), 2)
        self.assertEqual(ge.next(), 3)
        self.assertEqual(ge.next(), 4)
        self.assertRaises(StopIteration, ge.next)

    def test_sample_yield(self):
        ge = sample_yield()
        self.assertEqual(ge.next(), 0)
        self.assertEqual(ge.next(), 1)
        self.assertEqual(ge.next(), 2)
        self.assertRaises(StopIteration, ge.next)

    def test_nestd_yield(self):
        ge = nested_yield()
        self.assertEqual(ge.next(), 0)
        self.assertEqual(ge.next(), 1)
        self.assertEqual(ge.next(), 2)
        self.assertEqual(ge.next(), 3)
        self.assertRaises(StopIteration, ge.next)

    def test_recurse_yield(self):
        ge = recurse_yield(5)
        self.assertEqual(ge.next(), 0)
        self.assertEqual(ge.next(), 1)
        self.assertEqual(ge.next(), 2)
        self.assertEqual(ge.next(), 3)
        self.assertEqual(ge.next(), 4)
        self.assertEqual(ge.next(), 5)
        self.assertRaises(StopIteration, ge.next)


if __name__ == '__main__':
    main(verbosity=2)
