import os
from datetime import datetime

from config import ROOT_DIR
from src.read_xlsx import read_transactions_excel
from src.utils import get_events_information, get_information_home_page


def get_inform_for_veb_page(date_str: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            data_range: str = "M") -> tuple:
    """Возвращает JSON-строку для страницы 'Главная'"""
    filepath = os.path.join(ROOT_DIR, "data", "operations.xlsx")
    transactions = read_transactions_excel(filepath)

    inform_for_home_page = get_information_home_page(date_str, transactions)

    events_information = get_events_information(date_str, transactions, data_range)

    return inform_for_home_page, events_information
