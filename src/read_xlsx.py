import pandas as pd

from src.logging_config import read_xlsx_logger


def read_transactions_excel(filepath: str) -> pd.DataFrame:
    """Считывает финансовые операции из XLSX-файла"""
    try:
        read_xlsx_logger.info(f"Чтение XLSX-файла {filepath}.")
        transactions_df = pd.read_excel(filepath)

        transactions_df["Дата операции"] = pd.to_datetime(transactions_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

        read_xlsx_logger.info(f"XLSX-файл {filepath} преобразован в объект DataFrame.")
        return transactions_df

    except FileNotFoundError as e:
        read_xlsx_logger.error(f"XLSX-файл {filepath} не найден.")
        raise FileNotFoundError(f"Ошибка чтения файла: {e}.")

    except StopIteration as e:
        read_xlsx_logger.error(f"XLSX-файл {filepath} не содержит данные.")
        raise StopIteration(f"Ошибка чтения файла: {e}.")
