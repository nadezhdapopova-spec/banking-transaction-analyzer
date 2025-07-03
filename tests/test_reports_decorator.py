import os

import pytest

from config import ROOT_DIR
from src.reports_decorator import report

@report(filename=os.path.join(ROOT_DIR, r"data/test_exec.txt"))
def normal_exec_file(name: str) -> str:
    return "Hello " + name


@report(filename=os.path.join(ROOT_DIR, r"data/test_exec.txt"))
def exception_exec_file(error: str) -> str:
    raise Exception("Ошибка: " + error + ".")


def remove_test_file(path: str) -> None:
    """Удаляет тестовый файл для записи логов"""
    if os.path.exists(path):
        os.remove(path)


def read_test_file(path: str) -> list:
    """Возвращает записаннные в файл строки в виде списка кортежей"""
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def test_report_decorator_filename() -> None:
    """Проверка декоратора: запись в файл при успешном выполнении функции"""
    filepath = os.path.join(ROOT_DIR, r"data/test_exec.txt")
    remove_test_file(filepath)

    result = normal_exec_file("Alice")
    assert result == "Hello Alice"

    file_content = read_test_file(filepath)

    assert file_content[0] == "Function normal_exec_file ok\n"
    assert file_content[1] == "Function normal_exec_file called with args:\n"
    assert file_content[2] == " ('Alice',) \n"
    assert file_content[3] == "and kwargs: {}. \n", "Result: Hello Alice"


def test_log_file_decorator_exception() -> None:
    """Проверка декоратора: запись в файл при возбуждении исключения"""
    filepath = os.path.join(ROOT_DIR, r"data/test_exec.txt")
    remove_test_file(filepath)

    with pytest.raises(Exception):
        exception_exec_file("Неверное значение")

    file_content = read_test_file(filepath)
    assert (file_content[0] == "exception_exec_file error: Ошибка: " +
                               "Неверное значение. Inputs: ('Неверное значение',), {}\n")
