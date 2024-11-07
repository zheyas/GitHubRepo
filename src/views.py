import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import certifi
import pandas as pd
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение API-ключей из переменных окружения
currency_api_key = os.getenv("CURRENCY_API_KEY")
stock_api_key = os.getenv("STOCK_API_KEY")


# Утилита: Генерация временного диапазона
def generate_date_range(target_date: str, interval: str):
    target_date = datetime.strptime(target_date, "%d.%m.%Y")

    if interval == "W":
        start_date = target_date - timedelta(days=target_date.weekday())
        end_date = start_date + timedelta(days=6)
    elif interval == "M":
        start_date = datetime(target_date.year, target_date.month, 1)
        if target_date.month == 12:
            end_date = datetime(target_date.year, target_date.month, 31)
        else:
            end_date = datetime(target_date.year, target_date.month + 1, 1) - timedelta(days=1)
    elif interval == "Y":
        start_date = datetime(target_date.year, 1, 1)
        end_date = datetime(target_date.year, 12, 31)
    else:
        raise ValueError("Invalid interval type")

    return start_date, end_date


# Утилита: Получение данных о тратах и доходах из файла
def get_expenses_and_income_from_file(file_path, start_date, end_date):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    df = pd.read_excel(file_path)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format="%d.%m.%Y %H:%M:%S")
    df_filtered = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)]
    expenses = (
        df_filtered[df_filtered['Сумма операции'] < 0]
        .groupby('Категория')['Сумма операции']
        .sum()
        .to_dict()
    )
    income = (
        df_filtered[df_filtered['Сумма операции'] > 0]
        .groupby('Категория')['Сумма операции']
        .sum()
        .to_dict()
    )
    expenses = {k: abs(v) for k, v in expenses.items()}
    return expenses, income


# Основная функция: Генерация отчета
def generate_financial_report(target_date, interval='M'):
    # Получаем путь к текущему файлу и переходим на уровень выше, чтобы стать в корень проекта
    base_path = Path(__file__).resolve().parent.parent

    # Относительный путь к файлу в папке data
    file_path = base_path / 'data' / 'operations.xlsx'
    start_date, end_date = generate_date_range(target_date, interval)
    expenses, income = get_expenses_and_income_from_file(file_path, start_date, end_date)
    total_expenses = sum(expenses.values())
    total_income = sum(income.values())
    sorted_expenses = sorted(expenses.items(), key=lambda x: -x[1])
    main_expenses = sorted_expenses[:7]
    other_expenses_sum = sum([x[1] for x in sorted_expenses[7:]])
    main_expenses.append(("Остальное", other_expenses_sum))
    transfers_cash = {k: expenses[k] for k in ['Наличные', 'Переводы'] if k in expenses}
    sorted_transfers_cash = sorted(transfers_cash.items(), key=lambda x: -x[1])
    sorted_income = sorted(income.items(), key=lambda x: -x[1])

    report = {
        "Расходы": {
            "Общая сумма": total_expenses,
            "Основные": main_expenses,
            "Переводы и наличные": sorted_transfers_cash
        },
        "Поступления": {
            "Общая сумма": total_income,
            "Основные": sorted_income
        }
    }

    return json.dumps(report, ensure_ascii=False, indent=4)


# Утилита: Получение цены акции
def fetch_stock_price(api_key, ticker):
    url = f"https://financialmodelingprep.com/api/v3/quote-short/{ticker}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0].get('price', None)
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return None


# Основная функция: Получение цен акций
def fetch_sp500_stock_prices(api_key, tickers):
    stock_prices = {}
    for ticker in tickers:
        price = fetch_stock_price(api_key, ticker)
        if price is not None:
            stock_prices[ticker] = price
    return stock_prices


# Утилита: Конвертация валюты
def fetch_converted_amount(api_key, amount_value, from_currency, to_currency='RUB'):
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": api_key}
    params = {"to": to_currency, "from": from_currency, "amount": amount_value}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('result', None)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# Основная функция: Получение конвертированных сумм
def get_converted_amounts(api_key, amount_value):
    usd_to_rub = fetch_converted_amount(api_key, amount_value, 'USD')
    eur_to_rub = fetch_converted_amount(api_key, amount_value, 'EUR')
    return {"USD": usd_to_rub, "EUR": eur_to_rub}


# Пример использования
sp500_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]
