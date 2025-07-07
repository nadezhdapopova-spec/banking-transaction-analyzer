import json
import os
import re

import pandas as pd

from config import ROOT_DIR
from src.logging_config import services_logger
from src.read_xlsx import read_transactions_excel


def get_transactions_list() -> list[dict]:
    """Считывает финансовые операции из XLSX-файла и возвращает в виде списка."""
    filepath = os.path.join(ROOT_DIR, "data", "operations.xlsx")
    try:
        services_logger.info(f"Чтение XLSX-файла {filepath}.")
        transactions_df = read_transactions_excel(filepath)
        transactions_list = transactions_df.to_dict(orient="records")
        services_logger.info(f"XLSX-файл {filepath} преобразован в Python объект.")

        return transactions_list

    except AttributeError as e:
        services_logger.error(f"Ошибка преобразования XLSX-файла {filepath} в Python объект: {e}.")
        raise AttributeError(f"Ошибка: {e}.")


def get_profitable_cashback_categories(data: list[dict], month: int, year: int) -> str:
    """Возвращает JSON-ответ с анализом категорий кэшбэка за указанный период."""
    try:
        transactions_df = pd.DataFrame.from_records(data)

        filtered_transactions = transactions_df[(transactions_df["Дата операции"].dt.month == month) &
                                                (transactions_df["Дата операции"].dt.year == year) &
                                                (transactions_df["Кэшбэк"].notna())]
        services_logger.info("Транзакции отфильтрованы по дате")

        profit_cashback = filtered_transactions.groupby("Категория")["Кэшбэк"].sum().sort_values(ascending=False)
        services_logger.info("Получены данные о кэшбэке")
        profit_cashback_categories = profit_cashback.to_dict()
        for key, value in profit_cashback_categories.items():
            profit_cashback_categories[key] = int(value)

        profit_cashback_categories_json = json.dumps(profit_cashback_categories, ensure_ascii=False, indent=4)
        services_logger.info("Данные о кэшбэке преобразованы в JSON-строку")

        return profit_cashback_categories_json

    except KeyError as e:
        services_logger.error(f"Ошибка фильтрации транзакций: {e}")
        raise KeyError(f"Ошибка: {e}")


def make_simple_search(search_str: str) -> str:
    """Возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории."""
    transactions = get_transactions_list()

    pattern = re.compile(search_str, re.IGNORECASE)

    target_transactions = [transact for transact in transactions
                           if pattern.search(str(transact.get("Описание", "")))
                           or pattern.search(str(transact.get("Категория", "")))]
    services_logger.info(f"Транзакции отфильтрованы по запросу {search_str}")

    for item in target_transactions:
        item["Номер карты"] = None if pd.isna(item.get("Номер карты")) else item["Номер карты"]
        item["Кэшбэк"] = 0 if pd.isna(item.get("Кэшбэк")) else item["Кэшбэк"]
        item["MCC"] = None if pd.isna(item.get("MCC")) else item["MCC"]

    simple_search = json.dumps(target_transactions, ensure_ascii=False, indent=4, default=str)
    services_logger.info("Данные о транзакциях преобразованы в JSON-строку")

    return simple_search


def search_for_transfers_to_individuals(data: list[dict]) -> str:
    """Возвращает JSON-ответ со всеми транзакциями, которые относятся к переводам физлицам."""
    try:
        transactions_df = pd.DataFrame.from_records(data)

        pattern = re.compile(r"\b[А-Я][а-я]+ [А-Я]\.")

        filtered_transactions = transactions_df[(transactions_df["Категория"] == "Переводы") &
                                                (transactions_df["Описание"].str.contains(pattern))]
        services_logger.info("Получены транзакции - переводы физлицам")

        transfers_to_individuals = filtered_transactions.to_dict(orient="records")
        for item in transfers_to_individuals:
            item["Номер карты"] = None if pd.isna(item.get("Номер карты")) else item["Номер карты"]
            item["Кэшбэк"] = 0 if pd.isna(item.get("Кэшбэк")) else item["Кэшбэк"]
            item["MCC"] = None if pd.isna(item.get("MCC")) else item["MCC"]

        transfers_to_individuals_json = json.dumps(transfers_to_individuals, ensure_ascii=False, indent=4, default=str)
        services_logger.info("Данные о переводах физлицам преобразованы в JSON-строку")

        return transfers_to_individuals_json

    except KeyError as e:
        services_logger.error(f"Ошибка фильтрации транзакций: {e}")
        raise KeyError(f"Ошибка: {e}")
