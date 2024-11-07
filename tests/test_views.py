# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from src.views import (
    fetch_converted_amount,
    fetch_sp500_stock_prices,
    generate_date_range,
    generate_financial_report,
    get_expenses_and_income_from_file,
)


# Исправленный тест для generate_date_range
def test_generate_date_range():
    target_date = "01.01.2023"

    # Тестируем недельный интервал (начало недели - понедельник)
    start_date, end_date = generate_date_range(target_date, "W")
    assert start_date == datetime(2022, 12, 26)  # Начало недели, содержащей 01.01.2023
    assert end_date == datetime(2023, 1, 1)  # Конец недели

    # Тестируем месячный интервал
    start_date, end_date = generate_date_range(target_date, "M")
    assert start_date == datetime(2023, 1, 1)  # Начало месяца
    assert end_date == datetime(2023, 1, 31)  # Конец месяца

    # Тестируем годовой интервал
    start_date, end_date = generate_date_range(target_date, "Y")
    assert start_date == datetime(2023, 1, 1)  # Начало года
    assert end_date == datetime(2023, 12, 31)  # Конец года


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
    assert report_data["Расходы"]["Общая сумма"] == 100  # Проверка на общую сумму расходов
    assert report_data["Поступления"]["Общая сумма"] == 200  # Проверка на общую сумму поступлений


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


# Исправленный тест для get_expenses_and_income_from_file
# Определение вашей тестовой функции с использованием unittest.mock
@patch("src.views.pd.read_excel")
def test_get_expenses_and_income_from_file(mock_read_excel):
    # Мокируем данные
    mock_data = {
        'Дата операции': ["01.01.2023 12:00:00", "02.01.2023 15:00:00"],
        'Сумма операции': [-100.0, 200.0],
        'Категория': ["Еда", "Зарплата"]
    }
    mock_df = pd.DataFrame(mock_data)
    mock_read_excel.return_value = mock_df

    # Задаем даты для фильтрации
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)
    # Получаем путь к текущему файлу и переходим на уровень выше, чтобы стать в корень проекта
    base_path = Path(__file__).resolve().parent.parent

    # Относительный путь к файлу в папке data
    file_path = base_path / 'data' / 'operations.xlsx'
    # Вызов функции и проверка результатов
    expenses, income = get_expenses_and_income_from_file(file_path,start_date, end_date)
    assert expenses == {"Еда": 100.0}
    assert income == {}
