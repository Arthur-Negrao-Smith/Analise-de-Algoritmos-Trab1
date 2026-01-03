from util.data import DATA_PATH, Data
from util.benchmark import benchmark

import numpy as np


class AVLNode:
    def __init__(self, data: np.int64) -> None:
        self.data: np.int64 = data
        self.left: AVLNode | None = None
        self.right: AVLNode | None = None
        self.height: int = 1
        self.frequency: int = 1


class AVLTree:
    def __init__(self) -> None:
        self._root: AVLNode | None = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        if self._root is None:
            return "[]"

        return str(self.getSortedData())

    @benchmark("AVL Tree", save_csv=f"{DATA_PATH}/avl_tree.csv")
    def insertData(self, dataToOrder: Data) -> Data:
        for data in dataToOrder.data:
            tmp_node: AVLNode = AVLNode(data)
            self.insertNode(tmp_node, dataToOrder)

        dataToOrder.data = self.getSortedData()
        return dataToOrder

    def insertNode(self, node: AVLNode, dataToBenchmark: Data | None = None) -> None:
        if dataToBenchmark is None:
            dataToBenchmark = Data()

        self._size += 1

        dataToBenchmark.update_comparisons()
        if self._root is None:
            self._root = node
            return

        current: AVLNode = self.root
        stack: list[AVLNode] = []

        while True:
            dataToBenchmark.update_comparisons(2)
            if node.data == current.data:
                current.frequency += 1
                return

            stack.append(current)

            dataToBenchmark.update_comparisons()
            if node.data < current.data:
                dataToBenchmark.update_comparisons()
                if current.left is None:
                    current.left = node
                    break
                current = current.left

            elif node.data > current.data:
                dataToBenchmark.update_comparisons(2)
                if current.right is None:
                    current.right = node
                    break
                current = current.right

        while stack:

            parent: AVLNode = stack.pop()

            self._updateHeight(parent)

            balance: int = self._getBalance(parent)

            new_local_root: AVLNode = parent

            dataToBenchmark.update_comparisons(2)
            # right rotate
            if balance > 1:
                dataToBenchmark.update_comparisons()
                if self._getBalance(parent.left) >= 0:
                    new_local_root = self._rightRotate(parent)
                    dataToBenchmark.update_swaps()
                else:
                    # double rotation
                    parent.left = self._leftRotate(parent.left)  # type: ignore
                    new_local_root = self._rightRotate(parent)
                    dataToBenchmark.update_swaps(2)

            # left rotate
            elif balance < -1:
                dataToBenchmark.update_comparisons(2)
                if self._getBalance(parent.right) <= 0:
                    new_local_root = self._leftRotate(parent)
                    dataToBenchmark.update_swaps()
                else:
                    # double rotation
                    parent.right = self._rightRotate(parent.right)  # type: ignore
                    new_local_root = self._leftRotate(parent)
                    dataToBenchmark.update_swaps(2)

            dataToBenchmark.update_comparisons()
            # if any rotation occurred
            if parent != new_local_root:

                dataToBenchmark.update_comparisons()
                dataToBenchmark.update_swaps()
                # if the stack is empty
                if not stack:
                    self._root = new_local_root

                # reconect the grandparent
                else:
                    dataToBenchmark.update_comparisons()
                    grandparent: AVLNode = stack[-1]
                    if grandparent.left is parent:
                        grandparent.left = new_local_root
                    else:
                        grandparent.right = new_local_root

    def _getHeight(self, node: AVLNode | None) -> int:
        if node is None:
            return 0

        return node.height

    def _updateHeight(self, node: AVLNode) -> None:
        node.height = 1 + max(self._getHeight(node.left), self._getHeight(node.right))

    def _getBalance(self, node: AVLNode | None) -> int:
        if node is None:
            return 0
        return self._getHeight(node.left) - self._getHeight(node.right)

    def _leftRotate(self, node: AVLNode) -> AVLNode:
        new_root: AVLNode | None = node.right
        if new_root is None:
            raise RuntimeError("It is impossible to do a left rotate with a None node")

        node.right = new_root.left
        new_root.left = node

        self._updateHeight(node)
        self._updateHeight(new_root)

        return new_root

    def _rightRotate(self, node: AVLNode) -> AVLNode:
        new_root: AVLNode | None = node.left
        if new_root is None:
            raise RuntimeError("It is impossible to do a right rotate with a None node")

        node.left = new_root.right
        new_root.right = node

        self._updateHeight(node)
        self._updateHeight(new_root)

        return new_root

    def getSortedData(self) -> np.ndarray:
        # prealloc to avoid list reallocs
        result: np.ndarray = np.empty((self._size,), np.int64)

        stack: list[AVLNode] = []
        current: AVLNode | None = self.root

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

    @property
    def root(self) -> AVLNode:
        if self._root is None:
            raise RuntimeError("The tree don't have a root")

        return self._root
