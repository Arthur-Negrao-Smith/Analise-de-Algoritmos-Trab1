from enum import Enum
import numpy as np


class Order(Enum):
    ORDENED = 0
    REVERSED = 1
    RANDOM = 2
    MANY_REPETITIONS = 3


class Data:
    """
    Class to generate artificial data
    """

    def __init__(self) -> None:
        self._data: np.ndarray | None = None

    def create_data(self, size: int, order: Order) -> None:
        if size < 1:
            raise RuntimeError("Size of data must be greater than 0")

        match order:
            case Order.ORDENED:
                self._data = np.arange(0, size, step=1)
            case Order.REVERSED:
                self._data = np.arange(size - 1, -1, step=-1)
            case Order.RANDOM:
                self._data = np.random.randint(size - 1, size=(size))
            case Order.MANY_REPETITIONS:
                if size <= 100:
                    raise RuntimeError(
                        f"The size is very small. Use a size greater than 100: {size}"
                    )
                self._data = np.random.randint(low=0, high=size // 100, size=size - 1)
            case _:
                raise RuntimeError("Undefined order")

    @property
    def data(self) -> np.ndarray:
        if self._data is None:
            raise RuntimeError("Data wasn't initialized")

        return self._data

    @data.setter
    def data(self, newData: np.ndarray):
        self._data = newData
