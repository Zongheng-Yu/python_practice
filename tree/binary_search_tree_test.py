#! /usr/bin/env python
from binary_search_tree import BinarySearchTree as BSTree
import unittest


class BSTreeTest(unittest.TestCase):
    RAW_DATA = [3, 4, 6, 2, 1, 0, 7, 9, 8, 5]

    def setUp(self):
        '''        3
                  / \
                 2   4
                /     \
               1       6
              /       / \
             0       5   7
                          \
                           9
                            \
                             8
        '''
        self.tree = BSTree()
        for each in self.RAW_DATA:
            self.tree.insert(each)

    def tearDown(self):
        pass

    def test_size(self):
        self.assertEqual(len(self.RAW_DATA), self.tree.size)

    def test_search(self):
        for each in self.RAW_DATA:
            self.assertEqual(each, self.tree.search(each).key)

    def test_insert(self):
        self.tree.insert(99)
        self.assertEqual(len(self.RAW_DATA) + 1, self.tree.size)
        with self.assertRaises(KeyError):
            self.tree.insert(99)

        self.assertEqual(len(self.RAW_DATA) + 1, self.tree.size)
        self.tree.insert(-99)
        self.assertEqual(len(self.RAW_DATA) + 2, self.tree.size)

    def test_delete(self):
        self.tree.delete(0)
        self.assertEqual(9, self.tree.size)
        self.assertEqual(1, self.tree.min())

        self.tree.delete(9)
        self.assertEqual(8, self.tree.size)
        self.assertEqual(8, self.tree.max())

        with self.assertRaises(KeyError):
            self.tree.delete(9)

        self.tree.delete(6)
        self.assertEqual(7, self.tree.size)

        results = []
        self.tree.in_order_traversal(func=lambda x: results.append(x))
        self.assertEqual([1, 2, 3, 4, 5, 7, 8], results)

        results = []
        self.tree.layer_traversal(func=lambda x: results.append(x))
        self.assertEqual([3, 2, 4, 1, 5, 7, 8], results)

        self.tree.delete(3)
        self.assertEqual(6, self.tree.size)
        results = []
        self.tree.layer_traversal(func=lambda x: results.append(x))
        self.assertEqual([2, 1, 4, 5, 7, 8], results)

    def test_max(self):
        self.assertEqual(9, self.tree.max())

    def test_min(self):
        self.assertEqual(0, self.tree.min())

    def test_in_order_traversal(self):
        results = []
        self.tree.in_order_traversal(func=lambda x: results.append(x))
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], results)

    def test_pre_order_traversal(self):
        results = []
        self.tree.pre_order_traversal(func=lambda x: results.append(x))
        self.assertEqual([3, 2, 1, 0, 4, 6, 5, 7, 9, 8], results)

    def test_post_order_traversal(self):
        results = []
        self.tree.post_order_traversal(func=lambda x: results.append(x))
        self.assertEqual([0, 1, 2, 5, 8, 9, 7, 6, 4, 3], results)

    def test_layer_traversal(self):
        results = []
        self.tree.layer_traversal(func=lambda x: results.append(x))
        self.assertEqual([3, 2, 4, 1, 6, 0, 5, 7, 9, 8], results)
