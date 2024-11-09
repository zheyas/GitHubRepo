import os
from pathlib import Path

import pandas as pd

from src.reports import read_xlsx_financial_operations, spending_by_category, spending_by_workday


# Тестирование чтения данных из файла
def test_read_xlsx_financial_operations():
    # Создаем тестовый файл Excel
    test_file = Path(__file__).resolve().parent.parent / 'data' / 'test.xlsx'
    if test_file.exists():
        os.remove(test_file)

    test_data = [
        {'Дата операции': '01.10.2024 10:00:00', 'Категория': 'Продукты', 'Кэшбэк': '10', 'Сумма операции':
            '100', 'Описание': 'Тест1'},
        {'Дата операции': '05.10.2024 12:00:00', 'Категория': 'Транспорт', 'Кэшбэк': '5', 'Сумма операции':
            '50', 'Описание': 'Тест2'},
                ]
    df = pd.DataFrame(test_data)
    df.to_excel(test_file, index=False)

    # Проверка, что данные правильно считываются
    data = read_xlsx_financial_operations(test_file)
    assert len(data) == 2
    assert data[0]['Категория'] == 'Продукты'
    assert data[1]['Сумма операции'] == '50'

    # Удаление тестового файла
    os.remove(test_file)


# Тестирование функции `spending_by_workday`
def test_spending_by_workday():
    data = [
        {'Дата операции': '01.10.2024 10:00:00', 'Категория': 'Продукты', 'Кэшбэк': '10', 'Сумма операции':
            '100', 'Описание': 'Тест1'},
        {'Дата операции': '05.10.2024 12:00:00', 'Категория': 'Транспорт', 'Кэшбэк': '5', 'Сумма операции':
            '50', 'Описание': 'Тест2'},
        {'Дата операции': '07.10.2024 14:00:00', 'Категория': 'Продукты', 'Кэшбэк': '5', 'Сумма операции':
            '30', 'Описание': 'Тест3'},
    ]
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])

    result = spending_by_workday(df)

    assert 'Средние траты' in result.columns
    assert len(result) == 0  # Рабочие и выходные дни
    assert result['Средние траты'].sum() == 0.0


# Тестирование функции `spending_by_category`
def test_spending_by_category():
    data = [
        {'Дата операции': '01.10.2024 10:00:00', 'Категория': 'Продукты', 'Кэшбэк': '10', 'Сумма операции':
            '100', 'Описание': 'Тест1'},
        {'Дата операции': '05.10.2024 12:00:00', 'Категория': 'Транспорт', 'Кэшбэк': '5', 'Сумма операции':
            '50', 'Описание': 'Тест2'},
        {'Дата операции': '07.10.2024 14:00:00', 'Категория': 'Продукты', 'Кэшбэк': '5', 'Сумма операции':
            '30', 'Описание': 'Тест3'},
    ]
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])

    # Тест с категорией, которая существует
    result = spending_by_category(df, 'Продукты')
    assert 'Категория' not in result.columns

    # Тест с категорией, которой нет
    result_empty = spending_by_category(df, 'Электроника')
    assert result_empty.empty


# Тестирование неправильной даты в функции `spending_by_category`
def test_spending_by_category_invalid_date():
    data = [
        {'Дата операции': '01.10.2024 10:00:00', 'Категория': 'Продукты', 'Кэшбэк': '10', 'Сумма операции':
            '100', 'Описание': 'Тест1'},
        {'Дата операции': '05.10.2024 12:00:00', 'Категория': 'Транспорт', 'Кэшбэк': '5', 'Сумма операции':
            '50', 'Описание': 'Тест2'},
        {'Дата операции': '07.10.2024 14:00:00', 'Категория': 'Продукты', 'Кэшбэк': '5', 'Сумма операции':
            '30', 'Описание': 'Тест3'},
    ]
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])

    # Неверный формат даты
    result = spending_by_category(df, 'Продукты', date='2024-10-32')
    assert result.empty  # Должен вернуть пустой DataFrame
