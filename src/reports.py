import json
import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import ROOT_DIR
from src.reports_decorator import report


# @report()
@report(filename=os.path.join(ROOT_DIR, "data", "reports.txt"))
def get_spending_by_category(transactions: pd.DataFrame,
                             category: str,
                             date_str: Optional[str] = None) -> str:
    """Возвращает JSON-ответ с тратами по заданной категории за последние три месяца от заданной даты."""
    try:
        start_date, end_date = get_date_information(date_str)

        filtered_transactions = get_filtered_transactions(transactions, category, start_date, end_date)

        filtered_transactions_dict = filtered_transactions.to_dict(orient="records")
        for item in filtered_transactions_dict:
            item["Кэшбэк"] = 0 if pd.isna(item.get("Кэшбэк")) else item["Кэшбэк"]
            item["MCC"] = None if pd.isna(item.get("MCC")) else item["MCC"]

        return json.dumps(filtered_transactions_dict, ensure_ascii=False, indent=4, default=str)

    except KeyError as e:
        raise KeyError(f"Ошибка: {e}")


def get_date_information(date_str: Optional[str] = None) -> tuple[datetime, datetime]:
    """Возвращает начальную и конечную даты для фильтрации транзакций."""
    try:
        if not date_str:
            date_obj = datetime.now()
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        start_date = date_obj.replace(day=1) - relativedelta(months=2)
        end_date = date_obj + timedelta(days=1)

        return start_date, end_date

    except ValueError as e:
        raise ValueError(f"Некорректный формат даты: {e}")


def get_filtered_transactions(transactions_df: pd.DataFrame,
                              category: str,
                              start_date: datetime,
                              end_date: datetime) -> pd.DataFrame:
    """Возвращает транзакции, отфильтрованные по заданной дате и категории."""
    try:
        filtered_transactions = transactions_df[(transactions_df["Категория"] == category) &
                                                (transactions_df["Дата операции"] >= start_date) &
                                                (transactions_df["Дата операции"] < end_date)]
        return filtered_transactions

    except KeyError as e:
        raise KeyError(f"Ошибка: {e}")
