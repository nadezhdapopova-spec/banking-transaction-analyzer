from typing import Any
from unittest.mock import patch

import pandas as pd
from pandas._testing import assert_frame_equal

from src.read_xlsx import read_transactions_excel


@patch("src.read_xlsx.pd.read_excel")
def test_read_transactions_excel(mock_read_excel: Any) -> None:
    fake_df = pd.DataFrame({
        "Дата операции": ["01.01.2021 12:00:00", "02.01.2021 14:30:00"],
        "Сумма": [1000, 2000]
    })

    expected_df = fake_df.copy()
    expected_df["Дата операции"] = pd.to_datetime(expected_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    mock_read_excel.return_value = fake_df

    result = read_transactions_excel("fake/path.xlsx")

    assert_frame_equal(result, expected_df)
    mock_read_excel.assert_called_once_with("fake/path.xlsx")
