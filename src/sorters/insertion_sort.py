from util.search import binary_search
from util.data import Data, DATA_PATH
from util.benchmark import benchmark


@benchmark(
    "Insertion Sort (linear search)",
    save_csv=f"{DATA_PATH}/insertion_sort(linear_search).csv",
)
def insertion_sort_with_linear_search(dataToOrder: Data) -> Data:

    for i in range(1, len(dataToOrder.data)):
        key: int = dataToOrder.data[i]

        j = i - 1  # last index inserted
        while j >= 0 and key < dataToOrder.data[j]:
            dataToOrder.data[j + 1] = dataToOrder.data[j]
            j -= 1

            dataToOrder.update_comparisons(2)
            dataToOrder.update_swaps(1)

        # j will less than real index
        dataToOrder.data[j + 1] = key
        dataToOrder.update_swaps()

    return dataToOrder


@benchmark(
    "Insertion Sort (binary search)",
    save_csv=f"{DATA_PATH}/insertion_sort(binary_search).csv",
)
def insertion_sort_with_binary_searh(dataToOrder: Data) -> Data:
    for i in range(1, len(dataToOrder.data)):
        key: int = dataToOrder.data[i]

        j = binary_search(dataToOrder, key, 0, i - 1)

        if j < i:
            # shift all array 1 position to right (without copy data)
            dataToOrder.data[j + 1 : i + 1] = dataToOrder.data[j:i]

            # insert the key in the current position
            dataToOrder.data[j] = key

            dataToOrder.update_swaps(i - j)
            dataToOrder.update_comparisons()

    return dataToOrder
