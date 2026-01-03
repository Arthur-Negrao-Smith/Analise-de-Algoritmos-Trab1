from time import time
from typing import Self
import pandas as pd
from pathlib import Path

from util.data import Data

BENCHDATA_INDEXES: list[str] = ["Order", "Data Size", "Swaps", "Comparisons", "Time"]


def benchmark(
    algorithm_name: str, print_result: bool = True, save_csv: str | None = None
):

    def decorator(func):

        def wrapper(*args):
            start: float = time()
            data: Data = func(*args)
            finish: float = time() - start

            if print_result:
                print("-" * 50)
                print(f"Algorithm: {algorithm_name}")
                print(f"Data size: {len(data.data)}")
                print(f"Data ordering: {data.get_order().name}")
                print(f"Time: {finish}s")
                print("-" * 50)

            # to save the results
            if save_csv is not None:
                swaps, comparisons = data.get_swaps_comparisons()

                file_not_exists: bool = not Path(save_csv).exists()

                with open(save_csv, "a") as file:

                    # add a header
                    if file_not_exists:
                        file.write(",".join(BENCHDATA_INDEXES) + "\n")

                    file.write(
                        f"{data.get_order().name},{len(data.data)},{swaps},{comparisons},{finish}\n"
                    )

            return finish

        return wrapper

    return decorator


class BenchData:
    def __init__(self) -> None:
        self.df: pd.DataFrame = pd.DataFrame(
            {"Order": [], "Data Size": [], "Swaps": [], "Comparisons": [], "Time": []}
        )

    def __getattribute__(self, name: str) -> pd.Series | pd.DataFrame:
        return self.df[name]

    def read_csv(self, pathToData: str) -> Self:
        self.df.read_csv(
            pathToData,
        )
        return self
