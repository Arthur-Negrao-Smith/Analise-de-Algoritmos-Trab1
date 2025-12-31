from util.data import Data


def binary_search(data: Data, target: int, left: int, right: int) -> int:
    data.update_comparisons()
    if left == right:
        data.update_comparisons()

        if data.data[left] > target:
            return left
        else:
            return left + 1

    data.update_comparisons()
    # if the array don't have the target value
    if left > right:
        return left

    mid: int = (left + right) // 2

    data.update_comparisons()
    if target > data.data[mid]:
        return binary_search(data, target, mid + 1, right)

    data.update_comparisons()
    if target < data.data[mid]:
        return binary_search(data, target, left, mid - 1)

    return mid
