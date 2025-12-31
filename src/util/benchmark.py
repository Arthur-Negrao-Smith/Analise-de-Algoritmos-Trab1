from time import time
from typing import Self
import pandas as pd

from util.data import Data


def benchmark(
    algorithm_name: str, print_result: bool = True, save_csv: str | None = None
):

    def decorator(func):

        def wrapper(*args):
            start: float = time()
            data: Data = func(*args)
            finish: float = time() - start

            if print_result:
                print(f"Total time of {algorithm_name}: {finish}s")

            # to save the results
            if save_csv is not None:
                swaps, comparisons = data.get_swaps_comparisons()
                with open(save_csv, "a") as file:
                    file.write(
                        f"{data.get_order().name},{len(data.data)},{swaps},{comparisons},{finish}\n"
                    )

            return finish

        return wrapper

    return decorator


class BenchData:
    def __init__(self) -> None:
        self.df: pd.DataFrame = pd.DataFrame()

    def __getattribute__(self, name: str) -> pd.Series | pd.DataFrame:
        return self.df[name]

    def read_csv(self, pathToData: str) -> Self:
        self.df.read_csv(
            pathToData,
            header=None,
            names=["Order", "Data Size", "Swaps", "Comparisons", "Time"],
        )
        return self
