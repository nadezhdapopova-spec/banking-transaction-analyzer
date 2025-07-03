import json
import os
import re

import pandas as pd

from config import ROOT_DIR
from src.read_xlsx import read_transactions_excel


def get_transactions_list() -> list[dict]:
    """Считывает финансовые операции из XLSX-файла и возвращает в виде списка."""
    try:
        filepath = os.path.join(ROOT_DIR, "data", "operations.xlsx")
        transactions_df = read_transactions_excel(filepath)
        transactions_list = transactions_df.to_dict(orient="records")

        return transactions_list

    except AttributeError as e:
        raise AttributeError(f"Ошибка: {e}.")


def get_profitable_cashback_categories(data: list[dict], month: int, year: int) -> str:
    """Возвращает JSON-ответ с анализом категорий кэшбэка за указанный период."""
    try:
        transactions_df = pd.DataFrame.from_records(data)

        filtered_transactions = transactions_df[(transactions_df["Дата операции"].dt.month == month) &
                                                (transactions_df["Дата операции"].dt.year == year) &
                                                (transactions_df["Кэшбэк"].notna())]

        profit_cashback = filtered_transactions.groupby("Категория")["Кэшбэк"].sum().sort_values(ascending=False)
        profit_cashback_categories = profit_cashback.to_dict()
        for key, value in profit_cashback_categories.items():
            profit_cashback_categories[key] = int(value)

        profit_cashback_categories_json = json.dumps(profit_cashback_categories, ensure_ascii=False, indent=4)

        return profit_cashback_categories_json

    except KeyError as e:
        raise KeyError(f"Ошибка: {e}")


def make_simple_search(search_str: str) -> str:
    """Возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории."""
    transactions = get_transactions_list()

    pattern = re.compile(search_str, re.IGNORECASE)

    target_transactions = [transact for transact in transactions
                           if pattern.search(str(transact.get("Описание", "")))
                           or pattern.search(str(transact.get("Категория", "")))]

    for item in target_transactions:
        item["Кэшбэк"] = 0 if pd.isna(item.get("Кэшбэк")) else item["Кэшбэк"]
        item["MCC"] = None if pd.isna(item.get("MCC")) else item["MCC"]

    return json.dumps(target_transactions, ensure_ascii=False, indent=4, default=str)


def search_for_transfers_to_individuals(data: list[dict]) -> str:
    """Возвращает JSON-ответ со всеми транзакциями, которые относятся к переводам физлицам."""
    try:
        transactions_df = pd.DataFrame.from_records(data)

        pattern = re.compile(r"\b[А-Я][а-я]+ [А-Я]\.")

        filtered_transactions = transactions_df[(transactions_df["Категория"] == "Переводы") &
                                                (transactions_df["Описание"].str.contains(pattern))]

        transfers_to_individuals = filtered_transactions.to_dict(orient="records")
        for item in transfers_to_individuals:
            item["Кэшбэк"] = 0 if pd.isna(item.get("Кэшбэк")) else item["Кэшбэк"]
            item["MCC"] = None if pd.isna(item.get("MCC")) else item["MCC"]

        return json.dumps(transfers_to_individuals, ensure_ascii=False, indent=4, default=str)

    except KeyError as e:
        raise KeyError(f"Ошибка: {e}")
