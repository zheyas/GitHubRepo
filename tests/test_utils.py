import json
from unittest.mock import mock_open, patch

from src.utils import load_transactions


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
