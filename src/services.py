import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

# Получаем путь к текущему файлу и переходим на уровень выше, чтобы стать в корень проекта
base_path = Path(__file__).resolve().parent.parent

# Относительный путь к файлу в папке data
file_path_xlsx = base_path / 'data' / 'operations.xlsx'


def read_xlsx_financial_operations(file_path=file_path_xlsx) -> List[Dict[str, Any]]:
    """Читаем файл Excel и определяем нужные столбцы"""
    df = pd.read_excel(file_path, dtype=str)
    transactions = []

    for _, row in df.iterrows():
        transaction = {
            'Дата операции': row['Дата операции'],
            'Категория': row['Категория'],
            'Кэшбэк': row['Кэшбэк'] if pd.notna(row['Кэшбэк']) else "0",
            'Сумма операции': row['Сумма операции'] if pd.notna(row['Сумма операции']) else "0",
            'Описание': row.get('Описание', '')  # Добавляем поле Описание
        }
        transactions.append(transaction)

    return transactions


data = read_xlsx_financial_operations(file_path_xlsx)


def analyze_cashback_profitability(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """Анализ категорий повышенного кешбэка"""
    cashback_summary = defaultdict(float)

    for transaction in data:
        if transaction['Дата операции'] is None or transaction['Категория'] is None:
            print("Некорректная структура данных или отсутствуют значения:", transaction)
            continue

        try:
            transaction_date = datetime.strptime(transaction['Дата операции'], "%d.%m.%Y %H:%M:%S")
        except ValueError:
            print("Ошибка формата даты:", transaction['Дата операции'])
            continue

        transaction_year = transaction_date.year
        transaction_month = transaction_date.month
        category = transaction['Категория']
        cashback_amount = float(transaction.get('Кэшбэк', "0").replace(",", "."))

        if transaction_year == year and transaction_month == month:
            cashback_summary[category] += cashback_amount

    cashback_summary = {category: amount for category, amount in cashback_summary.items()}

    if not cashback_summary:
        return json.dumps({"message": "Данных за указанный месяц и год не найдено."}, ensure_ascii=False, indent=4)

    return json.dumps(cashback_summary, ensure_ascii=False, indent=4)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Calculate the amount to set aside in the 'Investment Savings' fund, excluding cashback."""
    total_investment = 0.0

    for transaction in transactions:
        try:
            transaction_date = datetime.strptime(transaction['Дата операции'], "%d.%m.%Y %H:%M:%S")
            transaction_month = transaction_date.strftime("%Y-%m")
        except ValueError:
            print(f"Invalid date format in transaction: {transaction['Дата операции']}")
            continue

        if transaction_month == month:
            operation_amount = float(transaction.get('Сумма операции', "0").replace(",", "."))

            # Calculate the rounded operation amount to the nearest limit
            rounded_amount = ((operation_amount // limit) + 1) * limit
            difference = rounded_amount - operation_amount

            # Only add the difference, excluding cashback
            total_investment += difference

    return total_investment


def search_transactions(data: List[Dict[str, Any]], query: str) -> str:
    """Поиск транзакций, содержащих запрос в категории или описании"""
    query = query.lower()
    results = [
        transaction for transaction in data
        if (isinstance(transaction.get('Категория'), str) and query in transaction['Категория'].lower()) or
           (isinstance(transaction.get('Описание'), str) and query in transaction['Описание'].lower())
    ]

    if not results:
        return json.dumps({"message": "Транзакции, соответствующие запросу, не найдены."},
                          ensure_ascii=False, indent=4)

    return json.dumps(results, ensure_ascii=False, indent=4)


def search_phone_transactions(data: List[Dict[str, Any]]) -> str:
    """Поиск транзакций, содержащих мобильные номера в описании и категории 'мобильная связь'."""
    results = []
    phone_pattern = r'\+?\d{1}\s?\d{3}\s?\d{3}-?\d{2}-?\d{2}'  # Шаблон для поиска номеров телефонов

    for transaction in data:
        # Проверяем, что поле 'Категория' равно 'мобильная связь' и 'Описание' не пустое
        if (transaction.get('Категория') == 'Мобильная связь' and
                isinstance(transaction.get('Описание'), str) and transaction['Описание']):
            phones_found = re.findall(phone_pattern, transaction['Описание'])
            if phones_found:
                results.append(transaction)

    if not results:
        return json.dumps({"message": "Транзакции с мобильными номерами не найдены."},
                          ensure_ascii=False, indent=4)

    return json.dumps(results, ensure_ascii=False, indent=4)


def search_personal_transfers(data: List[Dict[str, Any]]) -> str:
    """Поиск транзакций, относящихся к переводам физическим лицам."""
    results = []

    for transaction in data:
        # Проверяем, что поле 'Категория' равно 'Переводы' и 'Описание' не пустое
        if (transaction.get('Категория') == 'Переводы' and
                isinstance(transaction.get('Описание'), str) and transaction['Описание']):
            # Используем регулярное выражение для проверки формата "Имя Фамилия."
            if re.match(r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.$', transaction['Описание'].strip()):
                results.append(transaction)

    if not results:
        return json.dumps({"message": "Транзакции по переводам физическим лицам не найдены."},
                          ensure_ascii=False, indent=4)

    return json.dumps(results, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    # Анализ кешбэка за ноябрь 2021 года
    year, month = 2021, 12
    cashback_result = analyze_cashback_profitability(data, year, month)
    print("Анализ кешбэка по категориям:\n", cashback_result)

    # Рассчет накоплений для «Инвесткопилки» за ноябрь 2021 года
    investment_result = investment_bank("2021-12", data, 50)
    print(f"Сумма накоплений в «Инвесткопилке» за {year}-{month}: {investment_result} ₽")

    # Поиск транзакций с запросом
    search_query = "Фастфуд"
    search_result = search_transactions(data, search_query)
    print(f"Результаты поиска по запросу '{search_query}':\n", search_result)

    # Поиск мобильных номеров в транзакциях
    mobile_search_result = search_phone_transactions(data)
    print("Результаты поиска мобильных номеров:\n", mobile_search_result)

    # Поиск переводов физическим лицам
    personal_transfers_result = search_personal_transfers(data)
    print("Результаты поиска переводов физическим лицам:\n", personal_transfers_result)
