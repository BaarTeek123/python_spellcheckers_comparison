import time
from functools import wraps
from time import perf_counter


def repeat(number_of_times):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(number_of_times):
                func(*args, **kwargs)

        return wrapper

    return decorate



def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return result, abs(start-end)
    return wrapper


def retry(num_retries, exception_to_check, sleep_time=0):
    """Decorator that retries the execution of a function if it raises a specific exception."""
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, num_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exception_to_check as ex:
                    print(f"{func.__name__} raised {ex.__class__.__name__}. Retrying...")
                    if i < num_retries:
                        time.sleep(sleep_time)
            raise ex
        return wrapper
    return decorate




def log_info(logger):
    def log_info(function):
        """Decorator that logs basic informations about functions."""

        def wrapper(*args, **kwargs):
            logger.debug(f"----- {function.__name__}: start -----")
            if function.__doc__ is not None:
                logger.info(f"\n{function.__doc__}\n")
            start = perf_counter()
            output = function(*args, **kwargs)

            logger.debug(f"----- {function.__name__}: finished in {perf_counter() - start:.2f} seconds)-----")
            return output

        return wrapper

    return log_info