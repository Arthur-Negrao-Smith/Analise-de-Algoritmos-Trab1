from util.benchmark import benchmark
from util.data import Data, DATA_PATH


def heap_swap(data: Data, index_a: int, index_b: int) -> None:
    data.update_swaps()
    data.data[index_a], data.data[index_b] = data.data[index_b], data.data[index_a]


def heapify_recursive(dataToOrder: Data, dataSize: int, nodeIndex: int) -> None:
    largest: int = nodeIndex
    left: int = (nodeIndex << 1) + 1
    right: int = (nodeIndex << 1) + 2

    dataToOrder.update_comparisons(3)
    if left < dataSize and dataToOrder.data[left] > dataToOrder.data[largest]:
        largest = left
    if right < dataSize and dataToOrder.data[right] > dataToOrder.data[largest]:
        largest = right

    # if nodeIndex isn't the largest number
    if largest != nodeIndex:
        heap_swap(dataToOrder, nodeIndex, largest)
        heapify_recursive(dataToOrder, dataSize, largest)


@benchmark("Heap-Sort (recursive)", save_csv=f"{DATA_PATH}/heapsort_recursive.csv")
def heap_sort_recursive(dataToOrder: Data) -> Data:
    n: int = len(dataToOrder.data)
    for i in range((n >> 1) - 1, -1, -1):
        dataToOrder.update_comparisons()
        heapify_recursive(dataToOrder, n, i)

    # swap the largest number to the temporary final position
    for i in range(n - 1, 0, -1):
        dataToOrder.update_comparisons()

        heap_swap(dataToOrder, 0, i)

        # now use the heapify in the list
        heapify_recursive(dataToOrder, i, 0)

    return dataToOrder


def heapify_iterative(dataToOrder: Data, dataSize: int, nodeIndex: int) -> None:
    while True:
        largest: int = nodeIndex
        left: int = (nodeIndex << 1) + 1
        right: int = (nodeIndex << 1) + 2

        # while + 3 if conditions
        dataToOrder.update_comparisons(3)
        if left < dataSize and dataToOrder.data[left] > dataToOrder.data[largest]:
            largest = left
        if right < dataSize and dataToOrder.data[right] > dataToOrder.data[largest]:
            largest = right

        # if nodeIndex is the largest number
        if largest == nodeIndex:
            break

        heap_swap(dataToOrder, nodeIndex, largest)
        nodeIndex = largest


@benchmark("Heap-Sort (iterative)", save_csv=f"{DATA_PATH}/heapsort_iterative.csv")
def heap_sort_iterative(dataToOrder: Data) -> Data:
    n: int = len(dataToOrder.data)

    for i in range((n >> 1) - 1, -1, -1):
        dataToOrder.update_comparisons()
        heapify_iterative(dataToOrder, n, i)

    # swap the largest number to the temporary final position
    for i in range(n - 1, 0, -1):
        dataToOrder.update_comparisons()

        heap_swap(dataToOrder, 0, i)
        heapify_iterative(dataToOrder, i, 0)

    return dataToOrder
