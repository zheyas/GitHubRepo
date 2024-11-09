import json
import logging
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv


# Функция для генерации временного диапазона (неделя, месяц, год)
def generate_date_range(target_date: str, interval: str = "M"):
    target_date = datetime.strptime(target_date, "%d.%m.%Y")

    if interval == "W":
        start_date = target_date - timedelta(days=target_date.weekday())
        end_date = start_date + timedelta(days=6)
    elif interval == "M":
        start_date = datetime(target_date.year, target_date.month, 1)
        end_date = (datetime(target_date.year, target_date.month + 1, 1) - timedelta(days=1)) \
            if target_date.month != 12 else datetime(target_date.year, target_date.month, 31)
    elif interval == "Y":
        start_date = datetime(target_date.year, 1, 1)
        end_date = datetime(target_date.year, 12, 31)
    else:
        raise ValueError("Invalid interval type")

    return start_date, end_date


# Функция для извлечения последних 4 цифр карты из строки
def extract_last_four_digits(card_number):
    match = re.search(r'\d{4}$', card_number)
    return match.group(0) if match else None


# Функция для получения данных о тратах и доходах из файла JSON
def get_expenses_and_income_from_file(file_path, start_date, end_date):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    expenses = {}
    income = {}
    operations = []

    for operation in data:
        try:
            operation_date_str = operation.get('date')
            if operation_date_str is None:
                logger.warning(f"Пропущена операция без даты: {operation}")
                continue

            operation_date = datetime.strptime(operation_date_str, "%Y-%m-%dT%H:%M:%S.%f")

            if start_date <= operation_date <= end_date:
                amount = float(operation['operationAmount']['amount'])
                description = operation.get('description', "Без описания")

                if amount < 0:
                    expenses[description] = expenses.get(description, 0) + abs(amount)
                else:
                    income[description] = income.get(description, 0) + amount

                from_card = operation.get('from', None)
                last_four_digits = extract_last_four_digits(from_card)
                operations.append({
                    "Дата": operation_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "Описание": description,
                    "Сумма операции": amount,
                    "Последние 4 цифры карты": last_four_digits
                })
        except ValueError as e:
            logger.error(f"Неверный формат даты в операции: {operation}. Ошибка: {e}")

    return expenses, income, operations


# Функция для получения курсов валют
def fetch_converted_amount(api_key, amount_value, from_currency, to_currency='RUB'):
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": api_key}
    params = {"to": to_currency, "from": from_currency, "amount": amount_value}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('result', None)
    else:
        logger.error(f"Ошибка при получении курса валют: {response.status_code} - {response.text}")
        return None


# Функция для получения цен акций
def get_stock_prices(api_key, ticker):
    url = f"https://financialmodelingprep.com/api/v3/quote-short/{ticker}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return [{"stock": item["symbol"], "price": item["price"]} for item in data]


# Настройка логирования
logger = logging.getLogger('utils')
file_handler = logging.FileHandler(Path(__file__).parent.parent / 'logs/utils.log', 'w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
load_dotenv()
API_KEY = os.getenv("API_KEY")


# Функция для конвертации суммы в рубли
def convert_amount(transaction):
    currency = transaction["operationAmount"]["currency"]["code"]
    amount_value = transaction["operationAmount"]["amount"]

    # Если валюта RUB, возвращаем исходную сумму
    if currency == "RUB":
        logger.info('Конвертация валюты не нужна')
        return amount_value

    # Если валюта не RUB, отправляем запрос к API для конвертации
    converted_amount = fetch_converted_amount(API_KEY, amount_value, currency)

    if converted_amount is None:
        logger.error('Неудачный запрос к API для конвертации')
        raise RuntimeError("API request failed")

    logger.info('Конвертация прошла успешно')
    return converted_amount


# Получаем путь к текущему файлу и переходим на уровень выше, чтобы стать в корень проекта
base_path = Path(__file__).resolve().parent.parent

# Относительный путь к файлу в папке data
file_path = Path(__file__).resolve().parent.parent / 'data' / 'operations.json'


# Функция для загрузки транзакций из файла
def load_transactions(file_path):
    if not file_path.exists():
        logger.error(f'Файл {file_path} не существует')
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if isinstance(data, list):
                logger.info('Данные являются списком')
                return data
            else:
                logger.error('Данные не являются списком')
                return []
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f'Ошибка чтения данных: {e}')
        return []


def parse_stock_data(data):
    # Проверяем, является ли data строкой JSON и декодируем, если это так
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ValueError("Data is not valid JSON")

    # Проверяем, что data - это список словарей с нужными ключами
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        try:
            return [{"stock": item["symbol"], "price": item["price"]} for item in data]
        except KeyError:
            raise ValueError("Each item must contain 'symbol' and 'price' keys")
    else:
        raise TypeError("Expected data to be a list of dictionaries with 'symbol' and 'price' keys.")
