
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.reports import average_spending_by_day_type, read_xlsx_financial_operations

EXAMPLE_DATA = [
    {'Дата операции': '01.01.2024 12:00:00', 'Категория': 'Shopping', 'Кэшбэк': '5',
     'Сумма операции': '100.0', 'Описание': 'Clothes'},
    {'Дата операции': '02.01.2024 14:30:00', 'Категория': 'Food', 'Кэшбэк': '2',
     'Сумма операции': '50.0', 'Описание': 'Groceries'},
    {'Дата операции': '03.01.2024 18:00:00', 'Категория': 'Transport', 'Кэшбэк': '0',
     'Сумма операции': '20.0', 'Описание': 'Bus Ticket'},
]


@pytest.fixture
def example_dataframe():
    return pd.DataFrame(EXAMPLE_DATA)


def test_read_xlsx_financial_operations():
    with patch('pandas.read_excel', return_value=pd.DataFrame(EXAMPLE_DATA)):
        result = read_xlsx_financial_operations(file_path='dummy_path.xlsx')
        assert len(result) == 3
        assert result[0]['Категория'] == 'Shopping'
        assert result[1]['Кэшбэк'] == '2'
        assert result[2]['Сумма операции'] == '20.0'


def test_average_spending_by_day_type(example_dataframe):
    result = average_spending_by_day_type(example_dataframe, datetime(2024, 1, 4))
    assert result["Средние траты за выходной день"] >= 0
    assert result["Средние траты за рабочий день"] >= 0
