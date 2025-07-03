import json
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.services import (
    get_profitable_cashback_categories,
    get_transactions_list,
    make_simple_search,
    search_for_transfers_to_individuals
)


@patch("src.services.read_transactions_excel")
def test_get_transactions_list(mock_read_excel: Any) -> None:
    fake_df = pd.DataFrame({
        "Дата операции": ["01.01.2021 12:00:00", "02.01.2021 14:30:00"],
        "Сумма": [1000, 2000]
    })

    mock_read_excel.return_value = fake_df

    result = get_transactions_list()

    expected = [
        {"Дата операции": "01.01.2021 12:00:00", "Сумма": 1000},
        {"Дата операции": "02.01.2021 14:30:00", "Сумма": 2000}
    ]

    assert result == expected
    mock_read_excel.assert_called_once()


@patch("src.services.read_transactions_excel")
def test_get_transactions_list_invalid(mock_read_excel: Any) -> None:
    mock_read_excel.side_effect = AttributeError()
    with pytest.raises(AttributeError):
        get_transactions_list()


def test_get_profitable_cashback_categories(filtered_transactions_list: list[dict]) -> None:
    result = get_profitable_cashback_categories(filtered_transactions_list, 2, 2023)

    expected_result = {
        "Дом и ремонт": 100,
        "Наличные": 20,
        "Детские товары": 0,
        "Аптеки": 0,
        "Переводы": 0,
        "Пополнения": 0,
        "Связь": 0,
        "Супермаркеты": 0
    }

    expected_result_json = json.dumps(expected_result, ensure_ascii=False, indent=4)

    assert result == expected_result_json


def test_get_profitable_cashback_categories_invalid(filtered_transactions_invalid_list: list[dict]) -> None:
    with pytest.raises(KeyError):
        get_profitable_cashback_categories(filtered_transactions_invalid_list, 2, 2023)


@patch("src.services.get_transactions_list")
def test_make_simple_search(mock_get_list: Any, filtered_transactions_list: list[dict]) -> None:
    mock_get_list.return_value = filtered_transactions_list

    result = make_simple_search("Тинькофф")

    expected = [{
        "Дата операции": "2023-02-02 00:00:00",
        "Номер карты": "*7197",
        "Сумма операции": -2000,
        "Кэшбэк": 20,
        "Сумма операции с округлением": 2000,
        "Категория": "Наличные",
        "Описание": "Снятие в банкомате Тинькофф"
    }]

    actual_result = json.loads(result)

    assert actual_result == expected


def test_search_for_transfers_to_individuals(filtered_transactions_list: list[dict]) -> None:
    result = search_for_transfers_to_individuals(filtered_transactions_list)

    expected_result = [
        {
            "Дата операции": "2023-02-02 00:00:00",
            "Номер карты": "*4556",
            "Сумма операции": 1000.0,
            "Кэшбэк": 0,
            "Сумма операции с округлением": 1000,
            "Категория": "Переводы",
            "Описание": "Дмитрий Р."
        },
        {
            "Дата операции": "2023-02-04 00:00:00",
            "Номер карты": "*4556",
            "Сумма операции": -300.0,
            "Кэшбэк": 0,
            "Сумма операции с округлением": 300,
            "Категория": "Переводы",
            "Описание": "Андрей Х."
        }
    ]

    expected_result_json = json.dumps(expected_result, ensure_ascii=False, indent=4)

    assert result == expected_result_json


def test_search_for_transfers_to_individuals_invalid(filtered_transactions_invalid_list: list[dict]) -> None:
    with pytest.raises(KeyError):
        search_for_transfers_to_individuals(filtered_transactions_invalid_list)
