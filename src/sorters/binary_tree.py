from util.data import Data
from util.benchmark import benchmark


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

        return "[ " + self._recursive_visit(self.root) + "]"

    @benchmark("Binary Tree")
    def insertData(self, dataToOrder: Data) -> None:
        for data in dataToOrder.data:
            tmp_node: BinaryNode = BinaryNode(data)
            self.insertNode(tmp_node)

    def insertNode(self, node: BinaryNode) -> None:
        self._size += 1

        if self._root is None:
            self._root = node
            return

        self._root = self._recursiveInsertNode(self._root, node)

    def _recursiveInsertNode(
        self, root: BinaryNode | None, node: BinaryNode
    ) -> BinaryNode | None:
        if root is None:
            return node

        if node.data == root.data:
            root.frequency += 1
            return root

        if node.data < root.data:
            root.left = self._recursiveInsertNode(root.left, node)
            return root

        if node.data > root.data:
            root.right = self._recursiveInsertNode(root.right, node)
            return root

    def _recursive_visit(self, root: BinaryNode | None) -> str:
        if root is None:
            return ""

        data: str = self._recursive_visit(root.left)
        if root.frequency == 1:
            data += str(root.data) + " "
        else:
            for _ in range(root.frequency):
                data += str(root.data) + " "

        data += self._recursive_visit(root.right)

        return data

    @property
    def root(self) -> BinaryNode:
        if self._root is None:
            raise RuntimeError("The tree don't have a root")

        return self._root
