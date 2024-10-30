import csv
import pandas as pd
from pathlib import Path
import os

def read_xlsx_financial_operations(file_path):
    """
    Считывает финансовые операции из XLSX-файла и возвращает их в виде списка словарей.

    :param file_path: Путь к файлу XLSX
    :return: Список словарей с финансовыми операциями
    """
    try:
        # Считываем файл в DataFrame
        data = pd.read_excel(file_path, engine='openpyxl')

        # Собираем данные в список словарей
        operations = []
        for _, row in data.iterrows():
            operation = {
                "transaction_id": row.get('id'),
                "state": row.get('state'),
                "date": row.get('date'),
                "amount": row.get('amount'),
                "currency_name": row.get('currency_name'),
                "currency_code": row.get('currency_code'),
                "from_account": row.get('from'),
                "to_account": row.get('to'),
                "description": row.get('description')
            }
            operations.append(operation)

        return operations

    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


def read_csv_financial_operations(file_path):
    """
    Считывает финансовые операции из CSV-файла и возвращает их в виде списка словарей.

    :param file_path: Путь к файлу CSV
    :return: Список словарей с финансовыми операциями
    """
    try:
        operations = []
        # Используем кодировку 'cp1251' для файлов с кириллицей
        with open(file_path, encoding='cp1251') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')

            # Перебираем строки и добавляем их в список
            for row in reader:
                operations.append(row)

        return operations

    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []

# Устанавливаем рабочий каталог
os.chdir(r'D:\pyton\Курсы\pythonProjectN1')

# Указываем относительные пути
file_path_xlsx = Path('data/transactions_excel.xlsx')
file_path_csv = Path('data/file.csv')

# Читаем операции из файлов
xlsx_operations = read_xlsx_financial_operations(file_path_xlsx)
csv_operations = read_csv_financial_operations(file_path_csv)
