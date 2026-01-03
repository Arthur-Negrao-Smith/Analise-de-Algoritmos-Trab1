from util.data import DATA_PATH, Data
from util.benchmark import benchmark

import numpy as np


class BinaryNode:
    def __init__(self, data: int) -> None:
        self.data: int = data
        self.left: BinaryNode | None = None
        self.right: BinaryNode | None = None
        self.frequency: int = 1


class BinaryTree:
    def __init__(self) -> None:
        self._root: BinaryNode | None = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        if self._root is None:
            return "[]"

        return str(self.getSortedData())

    @benchmark("Binary Tree", save_csv=f"{DATA_PATH}/binary_tree.csv")
    def insertData(self, dataToOrder: Data) -> Data:
        for data in dataToOrder.data:
            tmp_node: BinaryNode = BinaryNode(data)
            self.insertNode(tmp_node)

        dataToOrder.data = self.getSortedData()
        return dataToOrder

    def insertNode(self, node: BinaryNode) -> None:
        self._size += 1

        if self._root is None:
            self._root = node
            return

        current: BinaryNode = self.root

        while True:
            if node.data == current.data:
                current.frequency += 1
                return

            if node.data < current.data:
                if current.left is None:
                    current.left = node
                    return
                current = current.left

            if node.data > current.data:
                if current.right is None:
                    current.right = node
                    return
                current = current.right

    @property
    def root(self) -> BinaryNode:
        if self._root is None:
            raise RuntimeError("The tree don't have a root")

        return self._root

    def getSortedData(self) -> np.ndarray:
        # prealloc to avoid list reallocs
        result: np.ndarray = np.empty((self._size,), np.int64)

        stack: list[BinaryNode] = []
        current: BinaryNode | None = self.root

        result_index: int = 0
        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()

                if current.frequency == 1:
                    result[result_index] = current.data
                    result_index += 1

                else:
                    # optmization with slice
                    result[result_index : result_index + current.frequency] = [
                        current.data
                    ] * current.frequency

                    result_index += current.frequency

                current = current.right

        return result
