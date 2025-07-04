import json
import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import ROOT_DIR
from src.logging_config import reports_logger
from src.reports_decorator import report


# @report()
@report(filename=os.path.join(ROOT_DIR, "data", "reports.txt"))
def get_spending_by_category(transactions: pd.DataFrame,
                             category: str,
                             date_str: Optional[str] = None) -> str:
    """Возвращает JSON-ответ с тратами по категории за последние три месяца от заданной даты."""
    try:
        start_date, end_date = get_date_information(date_str)

        spending_by_date_category = get_spending_by_date_category(transactions, category, start_date, end_date)

        spending_by_category = json.dumps(spending_by_date_category, ensure_ascii=False, indent=4, default=str)
        reports_logger.info("Данные о тратах по категории преобразованы в JSON-строку")

        return spending_by_category

    except KeyError as e:
        reports_logger.error(f"Ошибка преобразования данных: {e}")
        raise KeyError(f"Ошибка: {e}")


def get_date_information(date_str: Optional[str] = None) -> tuple[datetime, datetime]:
    """Возвращает начальную и конечную даты для фильтрации транзакций."""
    try:
        if not date_str:
            date_obj = datetime.now()
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        reports_logger.info(f"Дата {date_str} преобразована в объект datetime")

        start_date = date_obj.replace(day=1) - relativedelta(months=2)
        end_date = date_obj + timedelta(days=1)

        return start_date, end_date

    except ValueError as e:
        reports_logger.error(f"Некорректный формат даты {date_str}")
        raise ValueError(f"Некорректный формат даты: {e}")


def get_spending_by_date_category(transactions_df: pd.DataFrame,
                                  category: str,
                                  start_date: datetime,
                                  end_date: datetime) -> dict:
    """Возвращает траты по заданной дате и категории."""
    try:
        filtered_transactions = transactions_df[(transactions_df["Категория"] == category) &
                                                (transactions_df["Дата операции"] >= start_date) &
                                                (transactions_df["Дата операции"] < end_date)]

        total_spends = filtered_transactions[filtered_transactions["Сумма операции"] < 0]["Сумма операции"].sum()
        reports_logger.info("Получены траты по заданной дате и категории")

        spending_by_date_category = {
            "category": category,
            "spending": abs(total_spends)
        }

        return spending_by_date_category

    except KeyError as e:
        reports_logger.error(f"Ошибка фильтрации транзакций: {e}")
        raise KeyError(f"Ошибка: {e}")
