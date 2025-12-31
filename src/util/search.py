import numpy as np


def binary_search(array: np.ndarray, target: int, left: int, right: int) -> int:
    if left == right:
        if array[left] > target:
            return left
        else:
            return left + 1

    # if the array don't have the target value
    if left > right:
        return left

    mid: int = (left + right) // 2

    if target > array[mid]:
        return binary_search(array, target, mid + 1, right)

    if target < array[mid]:
        return binary_search(array, target, left, mid - 1)

    return mid
