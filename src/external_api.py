import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def amount(transaction: float, currency: str):
    """Принимает транзавкцию и возвращает сумму в рублях"""
    if (currency == "RUB"):
        return transaction
    else:
        headers = {
            "apikey": API_KEY
        }
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={transaction}"
        response = requests.get(url, headers=headers)

        result = response.json()["result"]
        return float(result)
