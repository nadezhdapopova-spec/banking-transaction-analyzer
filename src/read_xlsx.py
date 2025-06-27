import pandas as pd


def read_transactions_excel(filepath: str, month: int, year: int) -> pd.DataFrame:
    """Функция для считывания финансовых операций из XLSX-файлов"""
    # reading_csv_excel_logger.info(f"Чтение XLSX-файла {filepath}.")
    transactions_df = pd.read_excel(filepath)

    transactions_df["Дата операции"] = pd.to_datetime(transactions_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    filtered_transactions = transactions_df[(transactions_df["Дата операции"].dt.month == month) &
                                            (transactions_df["Дата операции"].dt.year == year)]

    # reading_csv_excel_logger.info(f"XLSX-файл {filepath} преобразован в Python-объект.")
    return filtered_transactions
