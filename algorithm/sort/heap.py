"""
Heap sort implementation.
The number of leaf node of a full binary tree is 2^n which is 1 more than the sum of all other nodes.
2^0 + 2^1 + ... + 2^n = 2^(n+1) - 1
"""
import unittest


class Heap(object):
    def __init__(self, iterable=None, key=lambda x: x):
        """
        Init a heap
        :param iterable: The iterable object to init the queue
        :param key: The function to extract key from item
        :return: None
        """
        self._arr = list()
        self._key = key
        if iterable is not None:
            for each in iterable:
                self._arr.append(each)
        self._heapify()

    def _heapify(self):
        for index in reversed(range(len(self._arr)//2)):
            self._bubble_down(index)

    def _bubble_down(self, start_pos):
        min_index = start_pos
        left = self.left_child(start_pos)
        right = self.right_child(start_pos)
        if left < len(self._arr) and self._key(self._arr[left]) < self._key(self._arr[min_index]):
            min_index = left
        if right < len(self._arr) and self._key(self._arr[right]) < self._key(self._arr[min_index]):
            min_index = right
        if min_index != start_pos:
            self._arr[min_index], self._arr[start_pos] = self._arr[start_pos], self._arr[min_index]
            self._bubble_down(min_index)

    def _bubble_up(self, pos):
        if pos > 0:
            parent = self.parent(pos)
            if self._key(self._arr[pos]) < self._key(self._arr[parent]):
                self._arr[pos], self._arr[parent] = self._arr[parent], self._arr[pos]
                self._bubble_up(parent)

    def pop(self):
        ret_val = self._arr[0]
        last = self._arr.pop()
        if len(self._arr) > 0:
            self._arr[0] = last
            self._bubble_down(0)
        return ret_val

    def push(self, item):
        self._arr.append(item)
        self._bubble_up(len(self._arr) - 1)

    def empty(self):
        return len(self._arr) == 0

    @staticmethod
    def left_child(index):
        return 2*index + 1

    @staticmethod
    def right_child(index):
        return Heap.left_child(index) + 1

    @staticmethod
    def parent(index):
        return (index - 1)//2

    def __contains__(self, item):
        return item in self._arr


class PriorityQueue(Heap):
    KEY_POS = 0
    VALUE_POS = 1

    def decrease_key(self, value, new_key):
        """
        Decreash the key of a item
        :param value: with which to find the item
        :param new_key: the new key to assign to the item
        :return: None
        """
        for i in range(len(self._arr)):
            if self._arr[i][self.VALUE_POS] is value:
                self._arr[i] = (new_key, value)
                self._bubble_up(i)
                break
        else:
            raise ValueError('value not found: %s' % value)

    def __contains__(self, value):
        for key, value2 in self._arr:
            if value2 is value:
                return True
        return False


def heap_sort(arr):
    heap = Heap(arr)
    for index in range(len(arr)):
        arr[index] = heap.pop()
    return arr


class TestHeap(unittest.TestCase):
    def test_heap(self):
        heap = Heap((4, 3, 1, 2, 5))
        self.assertEqual(heap.pop(), 1)
        heap.push(1)
        heap.push(6)
        self.assertEqual(heap.pop(), 1)
        self.assertEqual(heap.pop(), 2)
        self.assertEqual(heap.pop(), 3)
        self.assertEqual(heap.pop(), 4)
        self.assertEqual(heap.pop(), 5)
        self.assertFalse(heap.empty())
        self.assertEqual(heap.pop(), 6)
        self.assertTrue(heap.empty())

    def test_priority_queue(self):
        pq = PriorityQueue(((each, each) for each in range(5)))
        pq.decrease_key(4, -1)
        self.assertEqual((-1, 4), pq.pop())


if __name__ == '__main__':
    unittest.main(verbosity=2)
