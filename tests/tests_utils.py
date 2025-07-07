import json
from datetime import datetime
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import (
    filter_transactions,
    get_card_spent_cashback,
    get_date_obj_information,
    get_events_information,
    get_greeting,
    get_information_home_page,
    get_top_categories_expenses,
    get_top_categories_income,
    get_top_five_transactions,
    get_total_expenses,
    get_total_income,
    get_transfers_and_cash_expenses
)


@patch("src.utils.get_top_five_transactions")
@patch("src.utils.get_card_spent_cashback")
@patch("src.utils.filter_transactions")
@patch("src.utils.get_greeting", return_value="Добрый день")
@patch("src.utils.get_date_obj_information")
def test_get_information_home_page(mock_get_date_obj_information: Any,
                                   mock_get_greeting: Any,
                                   mock_filter_transactions: Any,
                                   mock_get_card_spent_cashback: Any,
                                   mock_get_top_five_transactions: Any) -> None:
    date_str = "2023-11-01 12:00:00"
    transactions = pd.DataFrame({
        "Дата операции": ["2023-11-01", "2023-11-02"],
        "Сумма": [1000, 2000]
    })
    currency_rates = [{"currency": "USD", "rate": 90.5}]
    stock_prices = [{"stock": "AAPL", "price": 150.0}]

    mock_get_date_obj_information.return_value = (
        pd.Timestamp("2023-11-01"),
        pd.Timestamp("2023-11-01"),
        pd.Timestamp("2023-11-02")
    )
    mock_filter_transactions.return_value = transactions
    mock_get_card_spent_cashback.return_value = [
        {"spent": 5000},
        {"cashback": 100}
    ]
    mock_get_top_five_transactions.return_value = [
        {"date": "2021-12-30", "amount": 1000},
        {"date": "2021-12-29", "amount": 2000}
    ]

    result = get_information_home_page(date_str, transactions, currency_rates, stock_prices)
    result_json = json.loads(result)

    assert result_json["greeting"] == "Добрый день"
    assert result_json["cards"] == [{"spent": 5000}, {"cashback": 100}]
    assert result_json["top_transactions"][0]["amount"] == 1000
    assert result_json["currency_rates"] == [{"currency": "USD", "rate": 90.5}]
    assert result_json["stock_prices"] == [{"stock": "AAPL", "price": 150.0}]


@patch("src.utils.get_top_categories_income")
@patch("src.utils.get_total_income")
@patch("src.utils.get_transfers_and_cash_expenses")
@patch("src.utils.get_top_categories_expenses")
@patch("src.utils.get_total_expenses")
@patch("src.utils.filter_transactions")
@patch("src.utils.get_date_obj_information")
def test_get_events_information(mock_get_date_obj_information: Any,
                                mock_filter_transactions: Any,
                                mock_get_total_expenses: Any,
                                mock_get_top_categories_expenses: Any,
                                mock_get_transfers_and_cash_expenses: Any,
                                mock_get_total_income: Any,
                                mock_get_top_categories_income: Any
                                ) -> None:
    date_str = "2023-11-01 12:00:00"
    transactions = pd.DataFrame({
        "Дата операции": ["2023-11-01", "2023-11-02"],
        "Сумма": [1000, 2000]
    })
    currency_rates = [{"currency": "USD", "rate": 90.5}]
    stock_prices = [{"stock": "AAPL", "price": 150.0}]
    data_range = "M"

    mock_get_date_obj_information.return_value = (
        pd.Timestamp("2023-11-01"),
        pd.Timestamp("2023-11-01"),
        pd.Timestamp("2023-11-02")
    )
    mock_filter_transactions.return_value = transactions
    mock_get_total_expenses.return_value = {"total_amount": 55000}
    mock_get_top_categories_expenses.return_value = [
        {"category": "Переводы", "amount": 11000},
        {"category": "Такси", "amount": 5000}
    ]
    mock_get_transfers_and_cash_expenses.return_value = [
        {"category": "Переводы", "amount": 11000},
        {"category": "Наличные", "amount": 1000}
    ]
    mock_get_total_income.return_value = {"total_amount": 155000}
    mock_get_top_categories_income.return_value = [
        {"category": "Пополнения", "amount": 11000},
        {"category": "Другое", "amount": 2000}
    ]

    result = get_events_information(date_str, transactions, currency_rates, stock_prices, data_range)
    result_json = json.loads(result)

    assert result_json["expenses"] == {
        "total_amount": 55000,
        "main": [
            {"category": "Переводы", "amount": 11000},
            {"category": "Такси", "amount": 5000}
        ],
        "transfers_and_cash": [
            {"category": "Переводы", "amount": 11000},
            {"category": "Наличные", "amount": 1000}
        ]
    }
    assert result_json["income"] == {
        "total_amount": 155000,
        "main": [
            {"category": "Пополнения", "amount": 11000},
            {"category": "Другое", "amount": 2000}
        ]
    }
    assert result_json["currency_rates"] == [{"currency": "USD", "rate": 90.5}]
    assert result_json["stock_prices"] == [{"stock": "AAPL", "price": 150.0}]


def test_get_date_obj_information_week() -> None:
    date_obj, start_date, end_date = get_date_obj_information("2025-06-13 02:26:18", "W")

    assert date_obj == datetime(2025, 6, 13, 2, 26, 18)
    assert start_date == datetime(2025, 6, 9, 2, 26, 18)
    assert end_date == datetime(2025, 6, 14, 2, 26, 18)


def test_get_date_obj_information_month() -> None:
    date_obj, start_date, end_date = get_date_obj_information("2023-05-25 00:00:00", "M")

    assert date_obj == datetime(2023, 5, 25, 0, 0, 0)
    assert start_date == datetime(2023, 5, 1, 0, 0, 0)
    assert end_date == datetime(2023, 5, 26, 0, 0, 0)


def test_get_date_obj_information_year() -> None:
    date_obj, start_date, end_date = get_date_obj_information("1900-04-01 02:26:18", "Y")

    assert date_obj == datetime(1900, 4, 1, 2, 26, 18)
    assert start_date == datetime(1900, 1, 1, 2, 26, 18)
    assert end_date == datetime(1900, 4, 2, 2, 26, 18)


def test_get_date_obj_information_lower() -> None:
    date_obj, start_date, end_date = get_date_obj_information("2000-02-29 02:26:18", "m")

    assert date_obj == datetime(2000, 2, 29, 2, 26, 18)
    assert start_date == datetime(2000, 2, 29, 2, 26, 18)
    assert end_date == datetime(2000, 3, 1, 2, 26, 18)


def test_get_date_obj_information_invalid() -> None:
    with pytest.raises(ValueError):
        get_date_obj_information("2023-12-31T02:26:18.671407", "M")


@pytest.mark.parametrize("date, expected", [
    ((2023, 1, 1, 8, 0), "Доброе утро"),
    ((2023, 1, 1, 12, 15), "Добрый день"),
    ((2023, 1, 1, 18, 0), "Добрый вечер"),
    ((2023, 1, 2, 0, 0), "Доброй ночи"),
])
def test_get_greeting(date: tuple[int, int, int, int, int], expected: str) -> None:
    date_obj = datetime(*date)
    assert get_greeting(date_obj) == expected


def test_filter_transactions_start_date() -> None:
    transactions = pd.DataFrame({
        "Дата операции": pd.to_datetime(["02.02.2023 00:00:00", "02.03.2023 00:00:00"], format="%d.%m.%Y %H:%M:%S"),
        "Сумма": [1000, 2000],
        "Кэшбэк": [0, 0]
    })

    start_date = datetime(2023, 2, 1, 2, 26, 18)
    end_date = datetime(2023, 2, 20, 2, 26, 18)
    date_obj = datetime(2023, 2, 19, 2, 26, 18)

    result = filter_transactions(transactions, start_date, end_date, date_obj)
    expected = [{
        "Дата операции": pd.Timestamp("2023-02-02 00:00:00"),
        "Сумма": 1000,
        "Кэшбэк": 0
    }]

    assert result.to_dict(orient="records") == expected


def test_filter_transactions() -> None:
    transactions = pd.DataFrame({
        "Дата операции": pd.to_datetime(["02.02.2023 00:00:00", "01.01.2023 00:00:00"], format="%d.%m.%Y %H:%M:%S"),
        "Сумма": [1000, 2000],
        "Кэшбэк": [0, 0]
    })

    start_date = datetime(2023, 2, 19, 2, 26, 18)
    end_date = datetime(2023, 2, 20, 2, 26, 18)
    date_obj = datetime(2023, 2, 19, 2, 26, 18)

    result = filter_transactions(transactions, start_date, end_date, date_obj)
    expected = [
        {"Дата операции": pd.Timestamp("2023-02-02 00:00:00"),
         "Сумма": 1000,
         "Кэшбэк": 0},
        {"Дата операции": pd.Timestamp("2023-01-01 00:00:00"),
         "Сумма": 2000,
         "Кэшбэк": 0}
    ]

    assert result.to_dict(orient="records") == expected


def test_filter_transactions_invalid() -> None:
    transactions = pd.DataFrame({
        "Сумма": [1000, 2000],
        "Кэшбэк": [0, 0]
    })

    start_date = datetime(2023, 2, 19, 2, 26, 18)
    end_date = datetime(2023, 2, 20, 2, 26, 18)
    date_obj = datetime(2023, 2, 19, 2, 26, 18)

    with pytest.raises(KeyError, match="Дата операции"):
        filter_transactions(transactions, start_date, end_date, date_obj)


def test_get_card_spent_cashback(filtered_transactions: pd.DataFrame) -> None:
    result = get_card_spent_cashback(filtered_transactions)

    expected = [
        {"last_digits": "4556", "total_spent": 10100.5, "cashback": 100},
        {"last_digits": "7197", "total_spent": 3650.0, "cashback": 20}
    ]

    assert result == expected


def test_get_card_spent_cashback_invalid(filtered_transactions_invalid: pd.DataFrame) -> None:
    with pytest.raises(KeyError, match="Номер карты"):
        get_card_spent_cashback(filtered_transactions_invalid)


def test_get_top_five_transactions(filtered_transactions: pd.DataFrame) -> None:
    result = get_top_five_transactions(filtered_transactions)

    expected = [
        {"date": "05.02.2023", "amount": 10000, "category": "Дом и ремонт", "description": "МаксидоМ"},
        {"date": "02.02.2023", "amount": 2000, "category": "Наличные", "description": "Снятие в банкомате Тинькофф"},
        {"date": "02.02.2023", "amount": 1000, "category": "Переводы", "description": "Дмитрий Р."},
        {"date": "03.02.2023", "amount": 1000, "category": "Аптеки", "description": "Аптека Вита"},
        {"date": "03.02.2023", "amount": 800.5, "category": "Супермаркеты", "description": "Магнит"}
    ]

    assert result == expected


def test_get_top_five_transactions_invalid(filtered_transactions_invalid: pd.DataFrame) -> None:
    with pytest.raises(KeyError, match="Сумма операции с округлением"):
        get_top_five_transactions(filtered_transactions_invalid)


def test_get_total_expenses(filtered_transactions: pd.DataFrame) -> None:
    result = get_total_expenses(filtered_transactions)

    expected = {"total_amount": 14850}

    assert result == expected


def test_get_total_expenses_invalid(filtered_transactions_invalid: pd.DataFrame) -> None:
    with pytest.raises(KeyError, match="Сумма операции"):
        get_total_expenses(filtered_transactions_invalid)


def test_get_total_income(filtered_transactions: pd.DataFrame) -> None:
    result = get_total_income(filtered_transactions)

    expected = {"total_amount": 1100}

    assert result == expected


def test_get_total_income_invalid(filtered_transactions_invalid: pd.DataFrame) -> None:
    with pytest.raises(KeyError, match="Сумма операции"):
        get_total_income(filtered_transactions_invalid)


def test_get_top_categories_expenses(filtered_transactions: pd.DataFrame) -> None:
    result = get_top_categories_expenses(filtered_transactions)

    expected = [
        {"category": "Дом и ремонт", "amount": 10000},
        {"category": "Наличные", "amount": 2000},
        {"category": "Аптеки", "amount": 1000},
        {"category": "Супермаркеты", "amount": 800},
        {"category": "Детские товары", "amount": 400},
        {"category": "Связь", "amount": 350},
        {"category": "Остальное", "amount": 0}
    ]

    assert result == expected


def test_get_top_categories_expenses_invalid(filtered_transactions_invalid: pd.DataFrame) -> None:
    with pytest.raises(KeyError, match="Категория"):
        get_top_categories_expenses(filtered_transactions_invalid)


def test_get_top_categories_income(filtered_transactions: pd.DataFrame) -> None:
    result = get_top_categories_income(filtered_transactions)

    expected = [
         {"category": "Переводы", "amount": 1000},
         {"category": "Пополнения", "amount": 100}
    ]

    assert result == expected


def test_get_top_categories_income_invalid(filtered_transactions_invalid: pd.DataFrame) -> None:
    with pytest.raises(KeyError, match="Сумма операции"):
        get_top_categories_income(filtered_transactions_invalid)


def test_get_transfers_and_cash_expenses(filtered_transactions: pd.DataFrame) -> None:
    result = get_transfers_and_cash_expenses(filtered_transactions)

    expected = [
        {"category": "Наличные", "amount": 2000},
        {"category": "Переводы", "amount": 300}
    ]

    assert result == expected


def test_get_transfers_and_cash_expenses_invalid(filtered_transactions_invalid: pd.DataFrame) -> None:
    with pytest.raises(KeyError, match="Категория"):
        get_transfers_and_cash_expenses(filtered_transactions_invalid)
