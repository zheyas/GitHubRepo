import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def amount(transaction):
    currency = transaction["operationAmount"]["currency"]["code"]
    amount_value = transaction["operationAmount"]["amount"]

    # Если валюта RUB, возвращаем исходную сумму
    if currency == "RUB":
        return amount_value

    # Если валюта не RUB, отправляем запрос к API для конвертации
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount_value}"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)

    # Проверяем успешность запроса и наличие нужного поля в ответе
    if response.status_code != 200 or "result" not in response.json():
        raise RuntimeError("API request failed")

    # Возвращаем сконвертированную сумму
    return response.json()["result"]


def load_transactions(file_path):
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        return []

    try:
        # Открываем файл и пытаемся загрузить данные
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, OSError):
        # Обработка ошибок чтения и декодирования JSON
        return []


file_path = r"D:\pyton\Курсы\pythonProjectN1\data\operations.json"
