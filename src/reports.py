import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

# Настройка базового уровня логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Получаем путь к корню проекта
base_path = Path(__file__).resolve().parent.parent

# Относительный путь к файлу данных
file_path_xlsx = Path(__file__).resolve().parent.parent / 'data' / 'operations.xlsx'


def read_xlsx_financial_operations(file_path=file_path_xlsx) -> List[Dict[str, Any]]:
    """Читаем файл Excel и определяем нужные столбцы."""
    try:
        df = pd.read_excel(file_path, dtype=str)
    except FileNotFoundError:
        logging.error(f"Файл не найден по пути: {file_path}")
        return []
    except Exception as e:
        logging.error(f"Ошибка при чтении файла: {e}")
        return []

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


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Вычисляет средние траты за выходные и будние дни за последние три месяца."""
    date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    three_months_ago = date - timedelta(days=90)

    # Преобразование 'Дата операции' в формат datetime
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'],
                                                   format='%d.%m.%Y %H:%M:%S', errors='coerce')

    # Фильтрация транзакций за последние три месяца и обработка пустых значений
    recent_data = transactions[(transactions['Дата операции'] >= three_months_ago) &
                               (transactions['Дата операции'] <= date)]
    recent_data = recent_data.dropna(subset=['Дата операции', 'Сумма операции'])
    recent_data['Сумма операции'] = pd.to_numeric(recent_data['Сумма операции'], errors='coerce')

    # Определение типа дня и вычисление средних трат
    recent_data['Тип дня'] = (recent_data['Дата операции'].dt.dayofweek.
                              apply(lambda x: 'Выходной день' if x >= 5 else 'Рабочий день'))
    result = (recent_data.groupby('Тип дня')['Сумма операции'].mean().reset_index().
              rename(columns={'Сумма операции': 'Средние траты'}))

    return result


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца от переданной даты."""
    try:
        date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    except ValueError:
        logging.error("Некорректный формат даты. Ожидается 'YYYY-MM-DD'.")
        return pd.DataFrame()

    # Дата начала периода - три месяца назад
    three_months_ago = date - timedelta(days=90)
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S',
                                                   errors='coerce')

    # Фильтрация по дате и категории
    filtered_data = transactions[(transactions['Дата операции'] >= three_months_ago) &
                                 (transactions['Дата операции'] <= date) &
                                 (transactions['Категория'] == category)]

    if filtered_data.empty:
        logging.warning(f"Нет транзакций по категории '{category}' за указанный период.")
        return pd.DataFrame()

    # Подсчёт общей суммы трат по категории
    total_spending = filtered_data['Сумма операции'].astype(float).sum()
    result = pd.DataFrame({'Категория': [category], 'Общие траты': [total_spending]})
    logging.info(f"Общая сумма трат по категории '{category}' за последние три месяца: {total_spending}")

    return result


# Основной блок кода
data = read_xlsx_financial_operations()
df_transactions = pd.DataFrame(data)

# Пример вызова функций
# print(spending_by_workday(df_transactions))
# print(spending_by_category(df_transactions, 'Категория_Пример'))
