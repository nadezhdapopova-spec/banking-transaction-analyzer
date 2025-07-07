import json
from datetime import datetime, timedelta

import pandas as pd

from src.logging_config import src_utils_logger


def get_information_home_page(date_str: str,
                              transactions: pd.DataFrame,
                              currency_rates: list[dict],
                              stock_prices: list[dict]) -> str:
    """Создает json-строку для страницы 'Главная'."""
    date_obj, start_date, end_date = get_date_obj_information(date_str)
    greeting = get_greeting(date_obj)

    transactions_df = filter_transactions(transactions, start_date, end_date, date_obj)
    cards_information = get_card_spent_cashback(transactions_df)
    top_five_transactions = get_top_five_transactions(transactions_df)

    result_dict = {
        "greeting": greeting,
        "cards": cards_information,
        "top_transactions": top_five_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    parsed_result = json.dumps(result_dict, indent=4, ensure_ascii=False)
    src_utils_logger.info("Python-объект преобразован в JSON-строку для страницы 'Главная'")

    return parsed_result


def get_events_information(date_str: str,
                           transactions: pd.DataFrame,
                           currency_rates: list[dict],
                           stock_prices: list[dict],
                           data_range: str = "M") -> str:
    """Создает json-строку для страницы 'События'."""
    date_obj, start_date, end_date = get_date_obj_information(date_str, data_range)

    transactions_df = filter_transactions(transactions, start_date, end_date, date_obj)

    total_amount_expenses = get_total_expenses(transactions_df)
    top_categories_expenses = get_top_categories_expenses(transactions_df)
    transfers_and_cash_expenses = get_transfers_and_cash_expenses(transactions_df)
    expenses = dict()
    expenses.update(total_amount_expenses)
    expenses["main"] = top_categories_expenses
    expenses["transfers_and_cash"] = transfers_and_cash_expenses

    total_amount_income = get_total_income(transactions_df)
    top_categories_income = get_top_categories_income(transactions_df)
    income = dict()
    income.update(total_amount_income)
    income["main"] = top_categories_income

    result = {
        "expenses": expenses,
        "income": income,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    parsed_result = json.dumps(result, indent=4, ensure_ascii=False)
    src_utils_logger.info("Python-объект преобразован в JSON-строку для страницы 'События'")

    return parsed_result


def get_date_obj_information(date_str: str, data_range: str = "M") -> tuple[datetime, datetime, datetime]:
    """Возвращает начальную и конечную даты для фильтрации транзакций."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        src_utils_logger.info(f"Дата {date_str} преобразована в объект datetime")
        end_date = date_obj + timedelta(days=1)

        if data_range == "W":
            duration = int(datetime.strftime(date_obj, "%w"))
            start_date = date_obj - timedelta(days=duration-1)
        elif data_range == "M":
            start_date = date_obj.replace(day=1)
        elif data_range == "Y":
            start_date = date_obj.replace(day=1, month=1)
        else:
            start_date = date_obj

        return date_obj, start_date, end_date

    except ValueError as e:
        src_utils_logger.error(f"Некорректный формат даты {date_str}")
        raise ValueError(f"Некорректный формат даты: {e}")


def get_greeting(date_obj: datetime) -> str:
    """Возвращает приветствие в зависимости от текущего времени."""
    if 6 <= date_obj.hour < 12:
        return "Доброе утро"
    elif 12 <= date_obj.hour < 18:
        return "Добрый день"
    elif 18 <= date_obj.hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def filter_transactions(transactions_df: pd.DataFrame,
                        start_date: datetime,
                        end_date: datetime,
                        date_obj: datetime) -> pd.DataFrame:
    """Возвращает транзакции, отфильтрованные по дате."""
    try:
        if start_date == date_obj:
            filtered_transactions = transactions_df[(transactions_df["Дата операции"] <= end_date)]
        else:
            filtered_transactions = transactions_df[(transactions_df["Дата операции"] >= start_date) &
                                                    (transactions_df["Дата операции"] < end_date)]

        src_utils_logger.info("Транзакции отфильтрованы по дате")
        return filtered_transactions

    except KeyError as e:
        src_utils_logger.error(f"Ошибка фильтрации транзакций по дате: {e}")
        raise KeyError(f"Ошибка: {e}")


def get_card_spent_cashback(transactions_df: pd.DataFrame) -> list[dict]:
    """Возвращает общую сумму расходов, кешбэк по каждой карте."""
    try:
        result = transactions_df.groupby("Номер карты").agg({"Сумма операции": "sum", "Кэшбэк": "sum"})
        src_utils_logger.info("Получены сумма расходов, кешбэк по каждой карте")

        result_dict = result.to_dict(orient="index")

        cards_info = []
        for key, value in result_dict.items():
            card_info = dict()
            card_info["last_digits"] = str(key)[-4:]
            card_info["total_spent"] = abs(round(value["Сумма операции"], 2))
            card_info["cashback"] = value["Кэшбэк"]
            cards_info.append(card_info)

        return cards_info

    except KeyError as e:
        src_utils_logger.error(f"Ошибка при получении данных по каждой карте: {e}")
        raise KeyError(f"Ошибка: {e}")


def get_top_five_transactions(transactions_df: pd.DataFrame) -> list[dict]:
    """Возвращает топ-5 транзакций по сумме платежа."""
    try:
        top_transactions = transactions_df.sort_values("Сумма операции с округлением", ascending=False).head(5)
        src_utils_logger.info("Транзакции отсортированы по сумме платежа")

        top_transactions_dict = top_transactions.to_dict(orient="index")

        top_five_transactions = []
        for key, value in top_transactions_dict.items():
            top_transact = dict()
            top_transact["date"] = value["Дата операции"].strftime("%d.%m.%Y")
            top_transact["amount"] = abs(value["Сумма операции"])
            top_transact["category"] = value["Категория"]
            top_transact["description"] = value["Описание"]
            top_five_transactions.append(top_transact)

        return top_five_transactions

    except KeyError as e:
        src_utils_logger.error(f"Ошибка при сортировке транзакций по сумме платежа: {e}")
        raise KeyError(f"Ошибка: {e}")


def get_total_expenses(transactions_df: pd.DataFrame) -> dict:
    """Возвращает общую сумму расходов."""
    try:
        total_amount = transactions_df[transactions_df["Сумма операции"] < 0]["Сумма операции"].sum()
        src_utils_logger.info("Получена сумма расходов")

        total_expenses = {"total_amount": abs(int(round(float(total_amount), 0)))}

        return total_expenses

    except KeyError as e:
        src_utils_logger.error(f"Ошибка при получении суммы расходов: {e}")
        raise KeyError(f"Ошибка: {e}")


def get_total_income(transactions_df: pd.DataFrame) -> dict:
    """Возвращает общую сумму поступлений."""
    try:
        total_amount = transactions_df[transactions_df["Сумма операции"] > 0]["Сумма операции"].sum()
        src_utils_logger.info("Получена сумма поступлений")

        total_income = {"total_amount": int(round(float(total_amount), 0))}

        return total_income

    except KeyError as e:
        src_utils_logger.error(f"Ошибка при получении суммы поступлений: {e}")
        raise KeyError(f"Ошибка: {e}")


def get_top_categories_expenses(transactions_df: pd.DataFrame) -> list[dict]:
    """Возвращает сумму расходов по 8 категориям."""
    try:
        result = transactions_df.groupby("Категория")["Сумма операции"].sum().loc[lambda x: x < 0].sort_values()
        other_category = result.iloc[7:].sum()
        src_utils_logger.info("Получена сумма расходов по категориям")

        result_list = result.reset_index().to_dict(orient="records")
        categories = [item for item in result_list[:7]]
        categories.append({
            "Категория": "Остальное",
            "Сумма операции": float(other_category)})

        for item in categories:
            item["category"] = item.pop("Категория")
            item["amount"] = item.pop("Сумма операции")
            item["amount"] = abs(int(round(float(item["amount"]), 0)))

        return categories

    except KeyError as e:
        src_utils_logger.error(f"Ошибка при получении суммы расходов по категориям: {e}")
        raise KeyError(f"Ошибка: {e}")


def get_top_categories_income(transactions_df: pd.DataFrame) -> list[dict]:
    """Возвращает сумму поступлений по категориям."""
    try:
        result = (transactions_df[transactions_df["Сумма операции"] > 0].
                  groupby("Категория")["Сумма операции"].sum().sort_values(ascending=False))
        src_utils_logger.info("Получена сумма поступлений по категориям")

        categories = result.reset_index().to_dict(orient="records")

        for item in categories:
            item["category"] = item.pop("Категория")
            item["amount"] = item.pop("Сумма операции")
            item["amount"] = int(round(float(item["amount"]), 0))

        return categories

    except KeyError as e:
        src_utils_logger.error(f"Ошибка при получении суммы поступлений по категориям: {e}")
        raise KeyError(f"Ошибка: {e}")


def get_transfers_and_cash_expenses(transactions_df: pd.DataFrame) -> list[dict]:
    """Возвращает сумму расходов по категориям 'Наличные' и 'Переводы'."""
    try:
        transfers_and_cash = (transactions_df[transactions_df["Категория"].isin(["Переводы", "Наличные"]) &
                                              (transactions_df["Сумма операции"] < 0)].
                              groupby("Категория")["Сумма операции"].sum().sort_values())
        src_utils_logger.info("Получена сумма расходов по категориям 'Наличные' и 'Переводы'")

        if "Переводы" not in transfers_and_cash:
            transfers_and_cash.loc["Переводы"] = 0
        if "Наличные" not in transfers_and_cash:
            transfers_and_cash.loc["Наличные"] = 0

        transfers_and_cash_list = transfers_and_cash.reset_index().to_dict(orient="records")

        for item in transfers_and_cash_list:
            item["category"] = item.pop("Категория")
            item["amount"] = item.pop("Сумма операции")
            item["amount"] = abs(int(round(float(item["amount"]), 0)))

        return transfers_and_cash_list

    except KeyError as e:
        src_utils_logger.error(f"Ошибка при получении данных по категориям 'Наличные' и 'Переводы': {e}")
        raise KeyError(f"Ошибка: {e}")
