#! /usr/bin/env python
from unittest import TestCase, TestSuite, TestLoader, TextTestRunner
from bubble_sort import bubble_sort
from insert_sort import insert_sort
from selection_sort import selection_sort
from merge_sort import merge_sort, merge_sort_memory_friendly
from quick_sort import quick_sort
from heap_sort import heap_sort


class TestSortingMethods(TestCase):
    RAW_DATA = []
    REF_DATA = [0, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9]

    def setUp(self):
        self.RAW_DATA = [3, 4, 6, 2, 1, 0, 7, 9, 8, 5, 5]

    def test_bubble_sort(self):
        self.assertEqual(bubble_sort(self.RAW_DATA), self.REF_DATA)

    def test_insert_sort(self):
        self.assertEqual(insert_sort(self.RAW_DATA), self.REF_DATA)

    def test_selection_sort(self):
        self.assertEqual(selection_sort(self.RAW_DATA), self.REF_DATA)

    def test_merge_sort(self):
        self.assertEqual(merge_sort(self.RAW_DATA), self.REF_DATA)

    def test_merge_sort_memory_friendly(self):
        self.assertEqual(merge_sort_memory_friendly(self.RAW_DATA, 0, len(self.RAW_DATA)), self.REF_DATA)

    def test_quick_sort(self):
        self.assertEqual(quick_sort(self.RAW_DATA), self.REF_DATA)

    def test_heap_sort(self):
        self.assertEqual(heap_sort(self.RAW_DATA), self.REF_DATA)


if __name__ == '__main__':
    suite1 = TestLoader().loadTestsFromTestCase(TestSortingMethods)
    all_tests = TestSuite([suite1])
    TextTestRunner(verbosity=2).run(all_tests)
