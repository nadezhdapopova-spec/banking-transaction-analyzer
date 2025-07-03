import json
from datetime import datetime, timedelta
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest
from dateutil.relativedelta import relativedelta
from pandas import Timestamp

from src.reports import get_date_information, get_filtered_transactions, get_spending_by_category


@patch("src.reports.get_filtered_transactions")
@patch("src.reports.get_date_information")
def test_get_spending_by_category(mock_get_date_information: Any, mock_filter_transactions: Any) -> None:
    date_str = "2023-11-01 12:00:00"
    category = "Связь"
    transactions = pd.DataFrame({
        "Дата операции": ["2023-11-01 12:00:00", "2023-10-30 12:00:00"],
        "Сумма": [1000, 2000],
        "Категория": ["Дом и ремонт", "Связь"],
        "Кэшбэк": [0, 20],
        "MCC": [5200, 7379]
    })

    mock_get_date_information.return_value = (
        pd.Timestamp("2023-09-01 12:00:00"),
        pd.Timestamp("2023-11-02 12:00:00")
    )

    mock_filter_transactions.return_value = transactions
    expected_result = transactions.to_dict(orient="records")
    expected_result_json = json.dumps(expected_result, ensure_ascii=False, indent=4)

    result = get_spending_by_category(transactions, category, date_str)

    assert result == expected_result_json


@patch("src.reports.get_filtered_transactions")
@patch("src.reports.get_date_information")
def test_get_spending_by_category_invalid(mock_get_date_information: Any, mock_filter_transactions: Any) -> None:
    date_str = "2023-11-01 12:00:00"
    category = "Связь"

    mock_get_date_information.return_value = (
        pd.Timestamp("2023-09-01 12:00:00"),
        pd.Timestamp("2023-11-02 12:00:00")
    )

    mock_filter_transactions.side_effect = KeyError()

    transactions = pd.DataFrame({
        "Дата операции": ["2023-11-01 12:00:00", "2023-10-30 12:00:00"],
        "Сумма": [1000, 2000],
        "Кэшбэк": [0, 20],
        "MCC": [5200, 7379]
    })

    with pytest.raises(KeyError):
        get_spending_by_category(transactions, category, date_str)


def test_get_date_information_with_date() -> None:
    date = "2021-10-30 22:39:04"

    result = get_date_information(date)

    expected = (
        (datetime(2021, 8, 1, 22, 39, 4),
         datetime(2021, 10, 31, 22, 39, 4))
    )

    assert result == expected


def test_get_date_information_without_date() -> None:
    date = None

    result = get_date_information(date)

    expected = (
        (datetime.now().replace(day=1) - relativedelta(months=2),
         datetime.now() + timedelta(days=1))
    )

    assert result == expected


def test_get_date_information_invalid() -> None:
    with pytest.raises(ValueError):
        get_date_information("2023-12-31T02:26:18.671407")


def test_get_filtered_transactions(filtered_transactions: pd.DataFrame) -> None:
    start_date = datetime(2023, 1, 1, 22, 39, 4)
    end_date = datetime(2023, 3, 15, 22, 39, 4)
    category = "Детские товары"

    result = get_filtered_transactions(filtered_transactions, category, start_date, end_date)

    expected = [
        {"Дата операции": Timestamp('2023-02-04 00:00:00'),
         "Номер карты": "*7197",
         "Сумма операции": -400.0,
         "Кэшбэк": 0,
         "Сумма операции с округлением": 400,
         "Категория": "Детские товары",
         "Описание": "Детский Мир"}
    ]

    assert result.to_dict(orient="records") == expected


def test_get_filtered_transactions_invalid(filtered_transactions_invalid: pd.DataFrame) -> None:
    start_date = datetime(2023, 1, 1, 22, 39, 4)
    end_date = datetime(2023, 3, 15, 22, 39, 4)
    category = "Детские товары"

    with pytest.raises(KeyError):
        get_filtered_transactions(filtered_transactions_invalid, category, start_date, end_date)
