import json
from datetime import datetime
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from src.utils import (
    extract_last_four_digits,
    fetch_converted_amount,
    generate_date_range,
    get_expenses_and_income_from_file,
    get_stock_prices,
    load_transactions,
    parse_stock_data,
)


# Тест для функции generate_date_range
@pytest.mark.parametrize("target_date, interval, expected", [
    ("15.03.2023", "W", (datetime(2023, 3, 13), datetime(2023, 3, 19))),
    ("15.03.2023", "M", (datetime(2023, 3, 1), datetime(2023, 3, 31))),
    ("15.03.2023", "Y", (datetime(2023, 1, 1), datetime(2023, 12, 31))),
])
def test_generate_date_range(target_date, interval, expected):
    start_date, end_date = generate_date_range(target_date, interval)
    assert start_date == expected[0]
    assert end_date == expected[1]


# Тест для функции extract_last_four_digits
@pytest.mark.parametrize("card_number, expected", [
    ("1234567890123456", "3456"),
    ("0000111122223333", "3333"),
    ("abcd", None),
])
def test_extract_last_four_digits(card_number, expected):
    assert extract_last_four_digits(card_number) == expected


# Тест для функции get_expenses_and_income_from_file
@patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
    {"date": "2023-03-15T12:34:56.789", "operationAmount": {"amount": "-100.0"}, "description": "Coffee",
     "from": "1234567890123456"},
    {"date": "2023-03-16T12:34:56.789", "operationAmount": {"amount": "200.0"}, "description": "Salary",
     "from": "1234567890123456"},
]))
@patch("os.path.exists", return_value=True)  # Mock os.path.exists to always return True
def test_get_expenses_and_income_from_file(mock_exists, mock_file):
    start_date = datetime(2023, 3, 1)
    end_date = datetime(2023, 3, 31)
    expenses, income, operations = get_expenses_and_income_from_file('dummy_path.json', start_date, end_date)
    assert expenses == {"Coffee": 100.0}
    assert income == {"Salary": 200.0}
    assert len(operations) == 2
    assert operations[0]["Последние 4 цифры карты"] == "3456"


# Тест для функции fetch_converted_amount
@patch("requests.get")
def test_fetch_converted_amount(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 7500.0}
    assert fetch_converted_amount("dummy_api_key", 100.0, "USD") == 7500.0


# Тест для функции get_stock_prices
@patch("requests.get")
def test_get_stock_prices(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"symbol": "AAPL", "price": 150.0}]
    result = get_stock_prices("dummy_api_key", "AAPL")
    assert result == [{"stock": "AAPL", "price": 150.0}]


# Тест для функции load_transactions
@patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"date": "2023-03-15T12:34:56.789"}]))
def test_load_transactions(mock_file):
    file_path = Path(__file__).resolve().parent / 'dummy_path.json'
    transactions = load_transactions(file_path)
    print(load_transactions(file_path))
    assert isinstance(transactions, list)
    assert transactions[0]["date"] == "2023-03-15T12:34:56.789"


# Тест для функции parse_stock_data
def test_parse_stock_data():
    # Correct data with both 'symbol' and 'price' keys
    data = json.dumps([{"symbol": "AAPL", "price": 150.0}, {"symbol": "TSLA", "price": 650.0}])
    result = parse_stock_data(data)
    assert result == [{"stock": "AAPL", "price": 150.0}, {"stock": "TSLA", "price": 650.0}]

    # Invalid JSON
    with pytest.raises(ValueError):
        parse_stock_data("invalid json")

    # Missing 'price' key
    with pytest.raises(ValueError):
        parse_stock_data([{"symbol": "AAPL"}])  # Missing 'price'
