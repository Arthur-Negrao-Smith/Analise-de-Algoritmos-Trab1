from util.search import binary_search
from util.data import Data
from util.benchmark import benchmark


@benchmark("Insertion Sort (linear search)")
def insertion_sort_with_linear_search(dataToOrder: Data) -> Data:

    for i in range(1, len(dataToOrder.data)):
        key: int = dataToOrder.data[i]

        j = i - 1  # last index inserted
        while j >= 0 and key < dataToOrder.data[j]:
            dataToOrder.data[j + 1] = dataToOrder.data[j]
            j -= 1

        # j will less than real index
        dataToOrder.data[j + 1] = key

    return dataToOrder


@benchmark("Insertion Sort (binary search)")
def insertion_sort_with_binary_searh(dataToOrder: Data) -> Data:
    for i in range(1, len(dataToOrder.data)):
        key: int = dataToOrder.data[i]

        j = binary_search(dataToOrder.data, key, 0, i - 1)

        if j < i:
            # shift all array 1 position to right (without copy data)
            dataToOrder.data[j + 1 : i + 1] = dataToOrder.data[j:i]

            # insert the key in the current position
            dataToOrder.data[j] = key

    return dataToOrder
