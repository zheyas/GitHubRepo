
# tests/test_widget.py

import pytest

from src.widget import get_date, mask_account_card


# Тесты для функции mask_account_card
@pytest.mark.parametrize("input_str, expected_output", [
    ("Visa Platinum 7000792289606361", "visa platinum XXXX XXXX XXXX 6361"),
    ("Maestro 7000792289606361", "maestro XXXX XXXX XXXX 6361"),
    ("Счет 73654108430135874305", "счет ****4305"),
    ("Visa 4000123456789010", "visa XXXX XXXX XXXX 9010"),
    ("Счет 1234", "счет ****1234"),
])
def test_mask_account_card_valid(input_str, expected_output):
    """Тестирование корректной работы маскировки карт и счетов."""
    assert mask_account_card(input_str) == expected_output


@pytest.mark.parametrize("input_str, expected_output", [
    ("InvalidFormat", "Invalid input"),
    ("Visa 1234ABCD5678", "Invalid card/account number format"),
    ("", "Invalid input"),
    ("Счет", "Invalid input"),
    ("Visa 700079228960636", "Invalid input format"),
])
def test_mask_account_card_invalid(input_str, expected_output):
    """Тестирование обработки некорректных входных данных."""
    assert mask_account_card(input_str) == expected_output


# Тесты для функции get_date
@pytest.mark.parametrize("input_date, expected_output", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2022-12-31T23:59:59", "31.12.2022"),
    ("1999-01-01T00:00:00", "01.01.1999"),
    ("2024-05-15T13:45:20.123456", "15.05.2024"),
])
def test_get_date_valid(input_date, expected_output):
    """Тестирование правильного преобразования дат."""
    assert get_date(input_date) == expected_output


@pytest.mark.parametrize("input_date, expected_output", [
    ("InvalidDateString", "Invalid date format"),  # Некорректный формат
    ("2024-03-11", "Invalid date format"),          # Отсутствует 'T' и время
    ("", "Invalid date format"),                     # Пустая строка
])
def test_get_date_invalid(input_date, expected_output):
    """Тестирование обработки некорректных входных данных для даты."""
    assert get_date(input_date) == expected_output
