from datetime import datetime
from unittest.mock import patch

import src.views
from src.views import get_card_summary, get_greeting, get_stock_prices_for_multiple_tickers, get_top_transactions


# Тест для get_stock_prices_for_multiple_tickers
@patch('src.views.get_stock_prices')
def test_get_stock_prices_for_multiple_tickers(mock_get_stock_prices):
    fake_api_key = src.views.stock_api_key
    # Мокаем результат вызова функции get_stock_prices
    mock_get_stock_prices.return_value = [{"stock": "AAPL", "price": 150}, {"stock": "AMZN", "price": 3200}]

    tickers = ["AAPL", "AMZN"]
    result = get_stock_prices_for_multiple_tickers(fake_api_key, tickers)

    assert result == {
        "AAPL": 150,
        "AMZN": 3200
    }
    mock_get_stock_prices.assert_any_call(fake_api_key, "AAPL")
    mock_get_stock_prices.assert_any_call(fake_api_key, "AMZN")


# Тест для get_card_summary
def test_get_card_summary():
    operations = [
        {"Последние 4 цифры карты": "1234", "Сумма операции": 1000},
        {"Последние 4 цифры карты": "5678", "Сумма операции": -500},
        {"Последние 4 цифры карты": "9876", "Сумма операции": 2000}
    ]

    result = get_card_summary(operations)

    expected_result = [
        {"last_four_digits": "1234", "total_expenses": 1000, "cashback": 10},
        {"last_four_digits": "5678", "total_expenses": 500, "cashback": 5},
        {"last_four_digits": "9876", "total_expenses": 2000, "cashback": 20}
    ]

    assert result == expected_result


# Тест для get_top_transactions
def test_get_top_transactions():
    operations = [
        {"Сумма операции": 1000, "Описание": "Транзакция 1"},
        {"Сумма операции": 500, "Описание": "Транзакция 2"},
        {"Сумма операции": 1500, "Описание": "Транзакция 3"}
    ]

    result = get_top_transactions(operations, top_n=2)

    expected_result = [
        {"Сумма операции": 1500, "Описание": "Транзакция 3"},
        {"Сумма операции": 1000, "Описание": "Транзакция 1"}
    ]

    assert result == expected_result


# Тест для get_greeting
def test_get_greeting():
    with patch('src.views.datetime') as mock_datetime:
        # Мокаем время
        mock_datetime.now.return_value = datetime(2024, 11, 9, 10, 0)
        result = get_greeting()
        assert result == "Доброе утро"

        mock_datetime.now.return_value = datetime(2024, 11, 9, 15, 0)
        result = get_greeting()
        assert result == "Добрый день"

        mock_datetime.now.return_value = datetime(2024, 11, 9, 19, 0)
        result = get_greeting()
        assert result == "Добрый вечер"

        mock_datetime.now.return_value = datetime(2024, 11, 9, 3, 0)
        result = get_greeting()
        assert result == "Доброй ночи"
