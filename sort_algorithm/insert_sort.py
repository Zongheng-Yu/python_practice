def insert_sort(arr):
    for i in range(1, len(arr)):
        for j in range(i):
            if arr[j] > arr[i]:
                tmp = arr[i]
                for k in range(i, j, -1):
                    arr[k] = arr[k-1]
                arr[j] = tmp
                break
    return arr


if __name__ == '__main__':
    print range(3, 1, -1)