import json
import os

import requests
from dotenv import load_dotenv

from config import ROOT_DIR


def get_currency_rates() -> list[dict]:
    """Получает данные о курсе заданных валют к рублю."""
    file_name = os.path.join(ROOT_DIR, "user_settings.json")
    with open(file_name) as f:
        data = json.load(f)

    valid_for_conversion = data["user_currencies"]

    currency_rates = []
    for currency in valid_for_conversion:
        currency_rate = {}
        cur_to = "RUB"
        cur_from = currency
        amount = 1
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={cur_to}&from={cur_from}&amount={amount}"

        load_dotenv()
        api_key = os.getenv('API_KEY_apilayer')
        headers = {
            "apikey": api_key
        }

        response = requests.get(url, headers=headers).json()

        result = round(response["result"], 2)

        currency_rate["currency"] = currency
        currency_rate["rate"] = result
        currency_rates.append(currency_rate)

    return currency_rates


def get_stock_prices() -> list[dict]:
    """Получает данные о cтоимости заданных акций из S&P500 в рублях."""
    file_name = os.path.join(ROOT_DIR, "user_settings.json")
    with open(file_name) as f:
        data = json.load(f)

    valid_stocks = data["user_stocks"]

    stock_prices = []
    for stock in valid_stocks:
        stock_price = {}
        load_dotenv()
        api_key = os.getenv('API_KEY_twelvedata')
        url = f"https://api.twelvedata.com/price?symbol={stock}&apikey={api_key}&source=docs"

        response = requests.get(url).json()

        stock_price["stock"] = stock
        stock_price.update(response)
        # stock_price["price"] = round(float(stock_price["price"]), 2)
        stock_prices.append(stock_price)

    return stock_prices
