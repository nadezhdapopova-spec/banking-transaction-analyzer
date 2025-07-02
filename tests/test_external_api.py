from typing import Any
from unittest.mock import Mock, mock_open, patch

import pytest
import requests

from src.external_api import get_currency_rates, get_stock_prices


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv", return_value="fake_api_key")
@patch("src.external_api.json.load")
@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
def test_get_currency_rates(mock_open_file: Any,
                            mock_json_load: Any,
                            mock_getenv: Any,
                            mock_requests_get: Any) -> None:
    mock_json_load.return_value = {
        "user_currencies": ["USD", "EUR"]
    }

    mock_getenv.return_value = "fake_api_key"
    mock_requests_get.side_effect = [
        Mock(json=Mock(return_value={"rate": "89.1234"})),
        Mock(json=Mock(return_value={"rate": "97.5678"}))
    ]

    result = get_currency_rates()

    expected = [
        {"currency": "USD", "rate": 89.12},
        {"currency": "EUR", "rate": 97.57}
    ]

    assert result == expected


@patch("builtins.open", side_effect=FileNotFoundError("Ошибка чтения файла"))
def test_get_currency_rates_file_not_found(mock_open_file: Any) -> None:
    with pytest.raises(FileNotFoundError):
        get_currency_rates()

    mock_open_file.assert_called_once()


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv", return_value="fake_api_key")
@patch("src.external_api.json.load")
@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
def test_get_currency_rates_request_exception(mock_open_file: Any,
                                              mock_json_load: Any,
                                              mock_getenv: Any,
                                              mock_requests_get: Any) -> None:
    mock_json_load.return_value = {
        "user_currencies": ["USD", "EUR"]
    }

    mock_requests_get.side_effect = requests.exceptions.RequestException("Ошибка сети")

    result = get_currency_rates()

    assert result == []


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv", return_value="fake_api_key")
@patch("src.external_api.json.load")
@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
def test_get_stock_prices(mock_open_file: Any,
                          mock_json_load: Any,
                          mock_getenv: Any,
                          mock_requests_get: Any) -> None:
    mock_json_load.return_value = {
        "user_stocks": ["AAPL", "AMZN"]
    }

    mock_getenv.return_value = "fake_api_key"
    mock_requests_get.side_effect = [
        Mock(json=Mock(return_value={"price": "189.1234"})),
        Mock(json=Mock(return_value={"price": "197.5678"}))
    ]

    result = get_stock_prices()

    expected = [
        {"stock": "AAPL", "price": 189.12},
        {"stock": "AMZN", "price": 197.57}
    ]

    assert result == expected


@patch("builtins.open", side_effect=FileNotFoundError("Ошибка чтения файла"))
def test_get_stock_prices_file_not_found(mock_open_file: Any) -> None:
    with pytest.raises(FileNotFoundError):
        get_stock_prices()

    mock_open_file.assert_called_once()


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv", return_value="fake_api_key")
@patch("src.external_api.json.load")
@patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks": ["AAPL", "MSFT"]}')
def test_get_stock_prices_request_exception(mock_open_file: Any,
                                            mock_json_load: Any,
                                            mock_getenv: Any,
                                            mock_requests_get: Any) -> None:
    mock_json_load.return_value = {
        "user_stocks": ["AAPL", "MSFT"]
    }

    mock_requests_get.side_effect = requests.exceptions.RequestException("Ошибка сети")

    result = get_stock_prices()

    assert result == []
