import json
import os.path
from datetime import datetime, timedelta

import pandas as pd

from config import ROOT_DIR
from src.external_api import get_currency_rates, get_stock_prices
from src.read_xlsx import read_transactions_excel


def get_information_from_json(date_str: str) -> str:
    """Создает json-строку"""
    date_obj, day, month, year = get_date_obj(date_str)
    greeting = get_greeting(date_obj)

    filepath = os.path.join(ROOT_DIR, "data", "operations.xlsx")
    transactions_df = read_transactions_excel(filepath)
    transactions_df = filter_transactions(transactions_df, day, month, year)

    cards_information = get_card_spent_cashback(transactions_df)

    top_five_transactions = get_top_five_transactions(transactions_df)

    currency_rates = get_currency_rates()

    stock_prices = get_stock_prices()

    result_dict = {
        "greeting": greeting,
        "cards": cards_information,
        "top_transactions": top_five_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    parsed_result = json.dumps(str(result_dict), indent=4, ensure_ascii=False)

    return parsed_result


def get_date_obj(date_str: str) -> tuple:
    """Возвращает объект datetime из заданной даты"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    return date_obj, int(date_obj.day), int(date_obj.month), int(date_obj.year)


def get_greeting(date_obj: datetime) -> str:
    """Возвращает приветствие в зависимости от текущего времени"""
    if 6 <= date_obj.hour < 12:
        return "Доброе утро"
    elif 12 <= date_obj.hour < 18:
        return "Добрый день"
    elif 18 <= date_obj.hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def filter_transactions(transactions_df, day, month, year) -> pd.DataFrame:
    """Функция для считывания финансовых операций из XLSX-файлов"""

    filtered_transactions = transactions_df[(transactions_df["Дата операции"].dt.day <= day) &
                                            (transactions_df["Дата операции"].dt.month == month) &
                                            (transactions_df["Дата операции"].dt.year == year)]

    return filtered_transactions


def get_card_spent_cashback(transactions_df: pd.DataFrame) -> list[dict]:
    """Возвращает общую сумму расходов, кешбэк по каждой карте"""
    result = transactions_df.groupby("Номер карты").agg({"Сумма операции": "sum", "Кэшбэк": "sum"})

    result_dict = result.to_dict(orient="index")

    cards_info = []
    for key, value in result_dict.items():
        card_info = dict()
        card_info["last_digits"] = str(key)[-4:]
        card_info["total_spent"] = round(value["Сумма операции"], 2)
        card_info["cashback"] = value["Кэшбэк"]
        cards_info.append(card_info)

    return cards_info


def get_top_five_transactions(transactions_df: pd.DataFrame) -> list[dict]:
    """Возвращает топ-5 транзакций по сумме платежа"""
    top_transactions = transactions_df.sort_values("Сумма операции с округлением", ascending=False).head(5)

    top_transactions_dict = top_transactions.to_dict(orient="index")

    top_five_transactions = []
    for key, value in top_transactions_dict.items():
        top_transact = dict()
        top_transact["date"] = value["Дата операции"].strftime("%d.%m.%Y")
        top_transact["amount"] = value["Сумма операции"]
        top_transact["category"] = value["Категория"]
        top_transact["description"] = value["Описание"]
        top_five_transactions.append(top_transact)

    return top_five_transactions


# def get_events_information(date_str: str, data_range: str = "M") -> str:
#     get_dates(date_str, data_range)
#
#     # return parsed_result
#
#
# def get_dates(date_str: str, data_range: str):
#     date_obj = datetime.strptime(date_str, "%d-%m-%Y")
#
#     if data_range == "W":
#         duration = int(str(datetime.strptime(date_str, "%w")))
#         start_date = date_obj - timedelta(days=duration)
#         return start_date
