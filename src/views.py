import json
import os
import ssl
from datetime import datetime, timedelta
from urllib.request import urlopen

import certifi
import pandas as pd
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение API-ключей из переменных окружения
currency_api_key = os.getenv("CURRENCY_API_KEY")
stock_api_key = os.getenv("STOCK_API_KEY")


# Генерация отчета с затратами и доходами
def generate_financial_report(target_date, interval='M'):
    # Генерация временного диапазона
    def generate_date_range(target_date, interval):
        target_date = datetime.strptime(target_date, "%d.%m.%Y")
        if interval == 'W':
            start_date = target_date - timedelta(days=target_date.weekday())  # начало недели
        elif interval == 'M':
            start_date = target_date.replace(day=1)  # начало месяца
        elif interval == 'Y':
            start_date = target_date.replace(month=1, day=1)  # начало года
        else:  # ALL
            start_date = datetime.min  # или фиксированная самая ранняя дата с реальными данными
        return start_date, target_date

    # Получение данных о тратах и поступлениях из файла
    def get_expenses_and_income_from_file(start_date, end_date):
        file_path = r"D:\pyton\Курсы\pythonProjectN1\data\operations.xlsx"
        df = pd.read_excel(file_path)
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format="%d.%m.%Y %H:%M:%S")
        df_filtered = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)]
        expenses = df_filtered[df_filtered['Сумма операции'] < 0].groupby('Категория')
        ['Сумма операции'].sum().to_dict()
        income = df_filtered[df_filtered['Сумма операции'] > 0].groupby('Категория')
        ['Сумма операции'].sum().to_dict()
        expenses = {k: abs(v) for k, v in expenses.items()}
        return expenses, income

    # Основная часть генерации отчета
    start_date, end_date = generate_date_range(target_date, interval)
    expenses, income = get_expenses_and_income_from_file(start_date, end_date)
    total_expenses = sum(expenses.values())
    total_income = sum(income.values())
    sorted_expenses = sorted(expenses.items(), key=lambda x: -x[1])
    main_expenses = sorted_expenses[:7]
    other_expenses_sum = sum([x[1] for x in sorted_expenses[7:]])
    main_expenses.append(("Остальное", other_expenses_sum))
    transfers_cash = {k: expenses[k] for k in ['Наличные', 'Переводы'] if k in expenses}
    sorted_transfers_cash = sorted(transfers_cash.items(), key=lambda x: -x[1])
    sorted_income = sorted(income.items(), key=lambda x: -x[1])

    # Формирование JSON ответа
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


# Функция для получения цен акций
def fetch_sp500_stock_prices(api_key, tickers):
    def fetch_stock_price(api_key, ticker):
        url = f"https://financialmodelingprep.com/api/v3/quote-short/{ticker}?apikey={api_key}"
        context = ssl.create_default_context(cafile=certifi.where())
        response = urlopen(url, context=context)
        data = json.loads(response.read().decode("utf-8"))
        if data:
            return data[0].get('price', None)
        return None

    stock_prices = {}
    for ticker in tickers:
        price = fetch_stock_price(api_key, ticker)
        if price is not None:
            stock_prices[ticker] = price
    return stock_prices


# Функция для конвертации валют
def fetch_converted_amount(api_key, amount_value, from_currency, to_currency='RUB'):
    url = (f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&"
           f"from={from_currency}&amount={amount_value}")
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        converted_amount = data.get('result', None)
        return converted_amount
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_converted_amounts(api_key, amount_value):
    usd_to_rub = fetch_converted_amount(api_key, amount_value, 'USD')
    eur_to_rub = fetch_converted_amount(api_key, amount_value, 'EUR')
    response = {"USD": usd_to_rub, "EUR": eur_to_rub}
    return response


sp500_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]
