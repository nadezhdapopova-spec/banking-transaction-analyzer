import pandas as pd


def read_transactions_excel(filepath: str) -> pd.DataFrame:
    """Считывает финансовые операции из XLSX-файла"""
    try:
        # reading_csv_excel_logger.info(f"Чтение XLSX-файла {filepath}.")
        transactions_df = pd.read_excel(filepath)

        transactions_df["Дата операции"] = pd.to_datetime(transactions_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

        # reading_csv_excel_logger.info(f"XLSX-файл {filepath} преобразован в Python-объект.")
        return transactions_df

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Ошибка чтения файла: {e}.")

    except StopIteration as e:
        raise StopIteration(f"Ошибка чтения файла: {e}.")
