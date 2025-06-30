import json
from typing import Any
from unittest.mock import patch

import pandas as pd

from src.utils import get_information_home_page, get_events_information


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



