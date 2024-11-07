import os
from datetime import datetime, timedelta
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


def average_spending_by_day_type(df: pd.DataFrame, date: datetime = None) -> dict:
    if date is None:
        date = datetime.now()

    # Определяем дату начала для фильтрации за последние три месяца
    three_months_ago = date - timedelta(days=90)

    # Преобразуем столбец 'Дата операции' в формат datetime с заданным форматом
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S', errors='coerce')

    # Фильтрация данных за последние три месяца
    recent_data = df[(df['Дата операции'] >= three_months_ago) & (df['Дата операции'] <= date)]
    recent_data = recent_data.dropna(subset=['Дата операции', 'Сумма операции'])
    recent_data['Сумма операции'] = recent_data['Сумма операции'].astype(float)
    recent_data['is_weekend'] = recent_data['Дата операции'].dt.dayofweek >= 5

    avg_weekend_spending = recent_data[recent_data['is_weekend']]['Сумма операции'].mean()
    avg_weekday_spending = recent_data[~recent_data['is_weekend']]['Сумма операции'].mean()

    return {
        "Средние траты за выходной день": float(avg_weekend_spending) if pd.notna(avg_weekend_spending) else 0,
        "Средние траты за рабочий день": float(avg_weekday_spending) if pd.notna(avg_weekday_spending) else 0
    }


# Основной блок кода
data = read_xlsx_financial_operations(file_path_xlsx)
df_transactions = pd.DataFrame(data)
