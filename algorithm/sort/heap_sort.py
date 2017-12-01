"""
Heap sort implementation.
The number of leaf node of a full binary tree is 2^n which is 1 more than the sum of all other nodes.
2^0 + 2^1 + ... + 2^n = 2^(n+1) - 1
"""


def left_child(index):
    return 2*index + 1


def right_child(index):
    return left_child(index) + 1


def max_heap(arr, index, heap_size):
    max_index = index
    left = left_child(index)
    right = right_child(index)
    if left < heap_size and arr[left] > arr[max_index]:
        max_index = left
    if right < heap_size and arr[right] > arr[max_index]:
        max_index = right
    if max_index != index:
        arr[max_index], arr[index] = arr[index], arr[max_index]
        max_heap(arr, max_index, heap_size)


def heap_sort(arr):
    for index in range(len(arr)//2 - 1, -1, -1):
        max_heap(arr, index, len(arr))

    for index in range(len(arr)):
        heap_size = len(arr) - index - 1
        arr[0], arr[heap_size] = arr[heap_size], arr[0]
        max_heap(arr, 0, heap_size)

    return arr
