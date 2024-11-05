import json
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Настройка логирования
logger = logging.getLogger('utils')
file_handler = logging.FileHandler(Path(__file__).parent.parent / 'logs/utils.log', 'w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)  # Устанавливаем уровень логирования
load_dotenv()
API_KEY = os.getenv("API_KEY")


def amount(transaction):
    currency = transaction["operationAmount"]["currency"]["code"]
    amount_value = transaction["operationAmount"]["amount"]

    # Если валюта RUB, возвращаем исходную сумму
    if currency == "RUB":
        logger.info('Конвертация валюты не нужна')
        return amount_value

    # Если валюта не RUB, отправляем запрос к API для конвертации
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount_value}"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)

    # Проверяем успешность запроса и наличие нужного поля в ответе
    if response.status_code != 200 or "result" not in response.json():
        logger.error('Неудачный запрос к API')
        raise RuntimeError("API request failed")

    # Возвращаем сконвертированную сумму
    logger.info('Конвертация прошла успешно')
    return response.json()["result"]


# Используем относительный путь к файлу
file_path = Path(__file__).parent / 'data/operations.json'


def load_transactions(file_path):
    # Проверяем, существует ли файл
    if not file_path.exists():
        logger.error(f'Файл {file_path} не существует')
        return []

    try:
        # Открываем файл и пытаемся загрузить данные
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                logger.info('Данные являются списком')
                return data
            else:
                logger.error('Данные не являются списком')
                return []
    except (json.JSONDecodeError, OSError) as e:
        # Обработка ошибок чтения и декодирования JSON
        logger.error(f'Ошибка чтения данных: {e}')
        return []


# Устанавливаем рабочий каталог
os.chdir(r'D:\pyton\Курсы\pythonProjectN1')

# Пример использования функции с относительным путем
file_path = Path('data/operations.json')
