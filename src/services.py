import json
import os
import re

import pandas as pd

from config import ROOT_DIR
from src.read_xlsx import read_transactions_excel


def get_transactions_list() -> list[dict]:
    try:
        filepath = os.path.join(ROOT_DIR, "data", "operations.xlsx")
        transactions_df = read_transactions_excel(filepath)
        transactions_list = transactions_df.to_dict(orient="records")

        return transactions_list

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Ошибка чтения файла: {e}.")

    except StopIteration as e:
        raise StopIteration(f"Ошибка чтения файла: {e}.")


def get_profitable_cashback_categories(data: list[dict], month: int, year: int) -> str:
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
    try:
        transactions = get_transactions_list()

        pattern = re.compile(search_str, re.IGNORECASE)

        target_transactions = [transact for transact in transactions
                               if any(pattern.search(str(value)) for value in transact.values())]

        return json.dumps(target_transactions, ensure_ascii=False, indent=4, default=str)

    except Exception as e:
        print(f"Ошибка {e}. Введены не корректные данные")


def search_for_transfers_to_individuals(data: list[dict]) -> str:
    try:
        transactions_df = pd.DataFrame.from_records(data)

        pattern = re.compile(r"\b[А-Я][а-я]+ [А-Я]\.")

        filtered_transactions = transactions_df[(transactions_df["Категория"] == "Переводы") &
                                                (transactions_df["Описание"].str.contains(pattern))]

        transfers_to_individuals = filtered_transactions.to_dict(orient="records")

        return json.dumps(transfers_to_individuals, ensure_ascii=False, indent=4, default=str)

    except KeyError as e:
        raise KeyError(f"Ошибка: {e}")
