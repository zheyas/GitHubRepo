import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from src.utils import fetch_converted_amount, generate_date_range, get_expenses_and_income_from_file, get_stock_prices

# Загрузка переменных окружения
load_dotenv()

currency_api_key = os.getenv("CURRENCY_API_KEY")
stock_api_key = os.getenv("STOCK_API_KEY")


# Функция для получения стоимости акций для нескольких тикеров
def get_stock_prices_for_multiple_tickers(api_key, tickers):
    stock_prices = {}
    for ticker in tickers:
        prices = get_stock_prices(api_key, ticker)
        for price_data in prices:
            stock_prices[price_data["stock"]] = price_data["price"]
    return stock_prices


# Функция для получения сводки по картам
def get_card_summary(operations):
    card_summary = []

    for operation in operations:
        # Извлекаем последние 4 цифры карты
        card = operation.get('Последние 4 цифры карты', '')  # Исправляем получение номера карты
        # Извлекаем сумму операции
        amount = operation.get('Сумма операции', 0)  # Исправляем получение суммы операции

        # Логирование для диагностики
        if not card:
            print(f"Отсутствует номер карты в операции: {operation}")
        if amount == 0:
            print(f"Отсутствует сумма операции или сумма равна 0: {operation}")

        # Вычисляем кешбэк
        cashback = abs(amount) // 100  # Абсолютное значение для кешбэка

        # Добавляем данные по карте
        card_summary.append({
            "last_four_digits": card[-4:] if card else '',  # Последние 4 цифры карты
            "total_expenses": abs(amount),  # Сумма расходов
            "cashback": cashback  # Кешбэк
        })

    return card_summary


# Функция для получения топ-5 транзакций
def get_top_transactions(operations, top_n=5):
    # Сортируем операции по сумме в убывающем порядке
    sorted_operations = sorted(operations, key=lambda x: x.get('Сумма операции', 0), reverse=True)

    # Берем топ-N операций
    top_transactions = sorted_operations[:top_n]

    # Логирование для диагностики
    if not top_transactions:
        print("Нет транзакций для отображения в топ-5.")

    return top_transactions


def get_greeting():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


# Получаем дату сегодня
today = datetime.today().strftime("%d.%m.%Y")

# Генерация даты
start_date, end_date = generate_date_range("10.10.2019", "M")

# Чтение файла операций
file_path = Path(__file__).resolve().parent.parent / "data" / "operations.json"

# Получение данных о тратах и доходах из файла
expenses, income, operations = get_expenses_and_income_from_file(file_path, start_date, end_date)

# Вывод на экран
ex_and_inc = (f"Траты: {expenses}" + f"Доходы: {income}")

# Получаем сводку по картам
card_summary = get_card_summary(operations)
summary = ("Сводка по картам:", card_summary)

# Получаем топ-5 транзакций
top_transactions = get_top_transactions(operations)
top5_transactions = ("Топ-5 транзакций:", top_transactions)

# Получаем стоимость акций для нескольких тикеров
tickers = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
stock_prices = get_stock_prices_for_multiple_tickers(stock_api_key, tickers)
share_price = ("Стоимость акций:", stock_prices)

# Получение текущих обменных курсов
exchange_rates = (f"Евро {fetch_converted_amount(currency_api_key, 1, 'EUR')} "
                  f"рублей\n") + (f"Доллар {fetch_converted_amount(currency_api_key, 1, 'USD')}"
                                  f" рублей\n")
