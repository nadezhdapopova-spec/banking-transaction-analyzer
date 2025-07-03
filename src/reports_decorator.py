import os.path
from functools import wraps
from typing import Any, Callable, Optional

from config import ROOT_DIR


def report(filename: Optional[str] = None) -> Any:
    """Декоратор для записи репорта работы функции в файл."""
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            path = filename or os.path.join(ROOT_DIR, "data", "report.txt")
            with open(path, "w", encoding="utf-8") as file:
                try:
                    result = func(*args, **kwargs)
                    log = (f"Function {func.__name__} ok" +
                           f"\nFunction {func.__name__} called with args:\n {args} \nand kwargs: {kwargs}. " +
                           f"\nResult: {result}")
                    file.write(log)
                    return result

                except Exception as e:
                    log = f"{func.__name__} error: {e} Inputs: {args}, {kwargs}\n\n"
                    file.write(log)
                    raise e

        return inner
    return wrapper
