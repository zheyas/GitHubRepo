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
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": API_KEY}
    params = {"to": "RUB", "from": currency, "amount": amount_value}

    response = requests.get(url, headers=headers, params=params)

    # Проверяем успешность запроса и наличие нужного поля в ответе
    if response.status_code != 200 or "result" not in response.json():
        logger.error('Неудачный запрос к API')
        raise RuntimeError("API request failed")

    # Возвращаем сконвертированную сумму
    logger.info('Конвертация прошла успешно')
    return response.json()["result"]



# Получаем путь к текущему файлу и переходим на уровень выше, чтобы стать в корень проекта
base_path = Path(__file__).resolve().parent.parent

# Относительный путь к файлу в папке data
file_path = base_path / 'data' / 'operations.json'

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
