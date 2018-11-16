def _quick_sort(arr):
    if len(arr) <= 1:
        return arr
    key = arr[0]
    left = []
    right = []
    for i in range(1, len(arr)):
        if arr[i] <= key:
            left.append(arr[i])
        else:
            right.append(arr[i])
    left = quick_sort(left)
    right = quick_sort(right)
    return left + [key] + right


def quick_sort(ary):
    return qsort(ary,0,len(ary)-1)
    return _quick_sort(ary)


def qsort(ary, left, right):
    if left >= right: return ary
    key = ary[left]
    lp = left + 1
    rp = right
    while lp < rp:
        while ary[rp] >= key and lp < rp:
            rp -= 1
        while ary[lp] <= key and lp < rp:
            lp += 1
        ary[lp],ary[rp] = ary[rp],ary[lp]
    ary[left],ary[lp] = ary[lp],ary[left]
    qsort(ary,left,lp-1)
    qsort(ary,rp+1,right)
    return ary