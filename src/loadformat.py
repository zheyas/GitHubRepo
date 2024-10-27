import csv
import pandas as pd


def read_xlsx_financial_operations(file_path):
    """
    Считывает и выводит финансовые операции из XLSX-файла.

    :param file_path: Путь к файлу XLSX
    """
    try:
        # Считываем файл в DataFrame
        data = pd.read_excel(file_path, engine='openpyxl')

        # Выводим первые несколько строк для проверки
        print("Первые строки данных:")
        print(data.head())

        # Перебираем строки, представляющие финансовые операции
        for index, row in data.iterrows():
            # Получаем данные из соответствующих столбцов
            transaction_id = row.get('id')
            state = row.get('state')
            date = row.get('date')
            amount = row.get('amount')
            currency_name = row.get('currency_name')
            currency_code = row.get('currency_code')
            from_account = row.get('from')
            to_account = row.get('to')
            description = row.get('description')

            # Выводим информацию о каждой операции
            print(f"ID: {transaction_id}, Статус: {state}, Дата: {date}, "
                  f"Сумма: {amount} {currency_name} ({currency_code}), "
                  f"От: {from_account}, До: {to_account}, Описание: {description}")

    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Пример использования
file_path_xlsl = r"D:\pyton\Курсы\pythonProjectN1\data\transactions_excel.xlsx"


def read_csv_financial_operations(file_path):
    """
    Считывает и выводит финансовые операции из CSV-файла.

    :param file_path: Путь к файлу CSV
    """
    try:
        # Открываем файл и читаем его содержимое
        with open(file_path) as csv_file:  # Добавляем encoding для поддержки кириллицы
            reader = csv.DictReader(csv_file, delimiter=';')  # Используем ';' как разделитель

            # Перебираем строки и выводим информацию
            for row in reader:
                print(row)  # Выводим каждую строку в формате словаря

    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Пример использования
file_path = r"D:\pyton\Курсы\pythonProjectN1\data\file.csv"

