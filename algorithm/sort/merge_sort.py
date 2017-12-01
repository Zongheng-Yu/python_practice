def _merge(left, right):
    l, r = 0, 0
    result = []
    while l < len(left) and r < len(right):
        if left[l] < right[r]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1

    result += left[l:]
    result += right[r:]
    return result


def merge_sort(arr):
    if len(arr) == 1:
        return arr
    left = arr[0:len(arr)//2]
    right = arr[len(arr)//2:]
    left = merge_sort(left)
    right = merge_sort(right)
    return _merge(left, right)


def merge_sort_memory_friendly(arr, start, len):
    if len == 1:
        return
    merge_sort_memory_friendly(arr, start, len//2)
    merge_sort_memory_friendly(arr, start + len//2, len - len//2)
    cmp_start = start
    for i in range(start + len//2, start + len):
        for j in range(cmp_start, i):
            if arr[j] > arr[i]:
                tmp = arr[i]
                for k in range(i, j, -1):
                    arr[k] = arr[k-1]
                arr[j] = tmp
                cmp_start = j + 1
                break

    return arr

