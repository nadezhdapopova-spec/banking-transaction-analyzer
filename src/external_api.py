import json
import os

import requests
from dotenv import load_dotenv

from config import ROOT_DIR
from src.logging_config import external_api_logger


def get_currency_rates() -> list[dict]:
    """Получает данные о курсе заданных валют к рублю."""
    file_name = os.path.join(ROOT_DIR, "user_settings.json")
    try:
        external_api_logger.info(f"Чтение json-файла {file_name}.")
        with open(file_name) as f:
            data = json.load(f)

        valid_for_conversion = data["user_currencies"]

        load_dotenv()
        api_key = os.getenv('API_KEY_twelvedata')

        currency_rates = []
        cur_to = "RUB"
        external_api_logger.info("Запрос к API https://api.twelvedata.com/exchange_rate")
        for cur in valid_for_conversion:
            url = f"https://api.twelvedata.com/exchange_rate?symbol={cur}/{cur_to}&apikey={api_key}&source = docs"
            response = requests.get(url).json()

            result = round(float(response["rate"]), 2)

            currency_rate = dict()
            currency_rate["currency"] = cur
            currency_rate["rate"] = result
            currency_rates.append(currency_rate)

        external_api_logger.info("Получены данные с API https://api.twelvedata.com/exchange_rate")
        return currency_rates

    except FileNotFoundError as e:
        external_api_logger.error(f"Json-файл {file_name} не найден.")
        raise FileNotFoundError(f"Ошибка чтения файла: {e}.")

    except requests.exceptions.RequestException as e:
        external_api_logger.warning(f"Ошибка запроса к API https://api.twelvedata.com/exchange_rate: {e}.")
        print("Ошибка запроса к API:", e)
        return []


def get_stock_prices() -> list[dict]:
    """Получает данные о cтоимости заданных акций из S&P500 в рублях."""
    file_name = os.path.join(ROOT_DIR, "user_settings.json")
    try:
        external_api_logger.info(f"Чтение json-файла {file_name}.")
        with open(file_name) as f:
            data = json.load(f)

        valid_stocks = data["user_stocks"]

        load_dotenv()
        api_key = os.getenv('API_KEY_twelvedata')

        stock_prices = []
        external_api_logger.info("Запрос к API https://api.twelvedata.com/price")
        for stock in valid_stocks:
            url = f"https://api.twelvedata.com/price?symbol={stock}&apikey={api_key}&source=docs"
            response = requests.get(url).json()

            stock_price = dict()
            stock_price["stock"] = stock
            stock_price.update(response)
            stock_price["price"] = round(float(stock_price["price"]), 2)
            stock_prices.append(stock_price)

        external_api_logger.info("Получены данные с API https://api.twelvedata.com/price")
        return stock_prices

    except FileNotFoundError as e:
        external_api_logger.error(f"Json-файл {file_name} не найден.")
        raise FileNotFoundError(f"Ошибка чтения файла: {e}.")

    except requests.exceptions.RequestException as e:
        external_api_logger.warning(f"Ошибка запроса к API https://api.twelvedata.com/price: {e}.")
        print("Ошибка запроса к API:", e)
        return []
