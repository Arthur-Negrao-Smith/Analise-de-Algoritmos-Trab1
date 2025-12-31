from time import time


def benchmark(
    algorithm_name: str, print_result: bool = True, save_file: str | None = None
):

    def decorator(func):

        def wrapper(*args):
            start: float = time()
            func(*args)
            finish: float = time() - start

            if print_result:
                print(f"Total time of {algorithm_name}: {finish}s")

            # to save the results
            if save_file is not None:
                with open(save_file, "a") as file:
                    file.write(str(finish) + "\n")

            return finish

        return wrapper

    return decorator
