import os
from unittest.mock import Mock, patch

from dotenv import load_dotenv

from src.external_api import amount

load_dotenv()
API_KEY = os.getenv("API_KEY")
print(f"Loaded API_KEY: {API_KEY}")  # Добавим вывод для проверки, что API_KEY загружен


@patch('src.external_api.requests.get')  # Патчим requests.get в src.external_api
def test_amount_in_rub(mock_get):
    # Тестируем случай, когда валюта RUB (запрос не отправляется)
    transaction = 1000
    currency = 'RUB'

    result = amount(transaction, currency)

    # Убедимся, что запрос к API не делается, если валюта - RUB
    mock_get.assert_not_called()
    assert result == 1000


@patch('src.external_api.requests.get')  # Патчим requests.get в src.external_api
def test_amount_in_foreign_currency(mock_get):
    # Тестируем случай, когда валюта не RUB и происходит вызов API
    transaction = 100
    currency = 'USD'

    # Создаем мок для ответа API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 70.0}  # Допустим, курс конвертации 70 RUB за 1 USD
    mock_get.return_value = mock_response

    result = amount(transaction, currency)

    # Проверим, какой был вызов mock_get
    print("Actual call:", mock_get.call_args)

    # Убедимся, что запрос к API был сделан с правильными параметрами
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100",
        headers={"apikey": API_KEY}  # Передаем реальный API_KEY
    )

    # Проверим, что функция вернула правильное значение
    assert result == 70.0


@patch('src.external_api.requests.get')  # Патчим requests.get в src.external_api
def test_amount_with_api_error(mock_get):
    # Тестируем случай, когда API возвращает ошибку
    transaction = 100
    currency = 'EUR'

    # Мок ответа с ошибкой
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    try:
        amount(transaction, currency)
    except KeyError:
        pass  # Ожидаем ошибку при отсутствии ключа "result"
    else:
        assert False, "Должна была быть ошибка KeyError"
