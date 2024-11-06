import json
import os
from unittest.mock import Mock, mock_open, patch

import pytest
from dotenv import load_dotenv

from src.utils import amount, load_transactions


# Тесты для функции load_transactions
def test_load_transactions_file_not_exists():
    # Патчим os.path.exists, чтобы возвращать False (файл не существует)
    with patch('os.path.exists', return_value=False):
        result = load_transactions('fake_path.json')
        assert result == [], "Должен возвращаться пустой список, если файл не существует."


def test_load_transactions_empty_file():
    # Патчим os.path.exists, чтобы возвращать True, а также open, чтобы вернуть пустой файл
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data='')):
            result = load_transactions('fake_path.json')
            assert result == [], "Должен возвращаться пустой список для пустого файла."


def test_load_transactions_invalid_json():
    # Патчим os.path.exists и open, чтобы вернуть некорректные JSON данные
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data='invalid json')):
            result = load_transactions('fake_path.json')
            assert result == [], "Должен возвращаться пустой список при ошибке JSONDecodeError."


def test_load_transactions_valid_json():
    # Патчим os.path.exists и open, чтобы вернуть корректные JSON данные
    mock_data = json.dumps([{"transaction": 100, "currency": "USD"}])  # Пример корректного JSON
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = load_transactions('fake_path.json')
            assert result == [{"transaction": 100, "currency": "USD"}], "Функция должна возвращать данные из файла."


def test_load_transactions_non_list_json():
    # Патчим os.path.exists и open, чтобы вернуть корректные данные, но не список
    mock_data = json.dumps({"transaction": 100, "currency": "USD"})  # Некорректный формат (не список)
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = load_transactions('fake_path.json')
            assert result == [], "Функция должна возвращать пустой список, если данные не являются списком."


# Загрузка API_KEY из переменных окружения
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY is not set")


# Тесты для функции amount
@patch('src.utils.requests.get')  # Патчим requests.get в src.utils
def test_amount_in_rub(mock_get):
    # Тестируем случай, когда валюта RUB (запрос не отправляется)
    transaction = {
        "operationAmount": {
            "currency": {"code": "RUB"},
            "amount": 1000
        }
    }

    result = amount(transaction)

    # Убедимся, что запрос к API не делается, если валюта - RUB
    mock_get.assert_not_called()
    assert result == 1000


@patch('src.utils.requests.get')  # Патчим requests.get в src.utils
def test_amount_in_foreign_currency(mock_get):
    # Тестируем случай, когда валюта не RUB и происходит вызов API
    transaction = {
        "operationAmount": {
            "currency": {"code": "USD"},
            "amount": 100
        }
    }

    # Создаем мок для ответа API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 70.0}  # Допустим, курс конвертации 70 RUB за 1 USD
    mock_get.return_value = mock_response

    result = amount(transaction)

    # Проверим, какой был вызов mock_get
    print("Actual call:", mock_get.call_args)

    # Убедимся, что запрос к API был сделан с правильными параметрами
    expected_url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100"
    expected_headers = {"apikey": API_KEY}

    mock_get.assert_called_once_with(expected_url, headers=expected_headers)

    # Проверим, что функция вернула правильное значение
    assert result == 70.0


@patch('src.utils.requests.get')  # Патчим requests.get в src.utils
def test_amount_with_api_error(mock_get):
    # Тестируем случай, когда API возвращает ошибку
    transaction = {
        "operationAmount": {
            "currency": {"code": "EUR"},
            "amount": 100
        }
    }

    # Мок ответа с ошибкой
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="API request failed"):
        amount(transaction)
