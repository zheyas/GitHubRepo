# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch, Mock
import json
import pandas as pd
from datetime import datetime
from src.views import generate_financial_report, fetch_sp500_stock_prices, fetch_converted_amount

# Тестирование функции generate_financial_report
@patch("src.views.pd.read_excel")
def test_generate_financial_report(mock_read_excel):
    # Мокируем данные
    mock_data = {
        'Дата операции': ["01.01.2023 12:00:00", "02.01.2023 15:00:00"],
        'Сумма операции': [-100.0, 200.0],
        'Категория': ["Еда", "Зарплата"]
    }
    mock_df = pd.DataFrame(mock_data)
    mock_read_excel.return_value = mock_df

    # Генерация отчета
    report = generate_financial_report("01.01.2023", "M")
    report_data = json.loads(report)

    # Печать для отладки
    print("Исходные данные:")
    print(mock_df)
    print("Отчет:")
    print(report_data)

    # Проверка структуры отчета
    assert "Расходы" in report_data
    assert "Поступления" in report_data
    assert report_data["Расходы"]["Общая сумма"] == 0  # Проверка на общую сумму расходов
    assert report_data["Поступления"]["Общая сумма"] == 0  # Проверка на общую сумму поступлений

# Тестирование функции fetch_sp500_stock_prices
@patch("src.views.urlopen")
def test_fetch_sp500_stock_prices(mock_urlopen):
    # Мокируем ответ API
    mock_response = Mock()
    mock_response.read.return_value = json.dumps([{"symbol": "AAPL", "price": 150.0}]).encode("utf-8")
    mock_urlopen.return_value = mock_response

    # Проверка вызова функции
    prices = fetch_sp500_stock_prices("fake_api_key", ["AAPL"])
    assert prices == {"AAPL": 150.0}

# Тестирование функции fetch_converted_amount
@patch("src.views.requests.get")
def test_fetch_converted_amount(mock_get):
    # Мокируем ответ API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 75.0}
    mock_get.return_value = mock_response

    # Проверка конверсии валют
    converted_amount = fetch_converted_amount("fake_api_key", 1, "USD", "RUB")
    assert converted_amount == 75.0
