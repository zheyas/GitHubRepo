import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тесты для функции get_mask_card_number
def test_get_mask_card_number_valid():
    """Тестирование корректной работы маскировки номера карты."""
    card_number = 1234567890123456
    masked_card = get_mask_card_number(card_number)
    assert masked_card == "XXXX XX78 **** 3456"


def test_get_mask_card_number_invalid_length():
    """Тестирование обработки некорректной длины номера карты."""
    card_number = 1234567890  # Меньше 16 цифр
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр."):
        get_mask_card_number(card_number)


# Тесты для функции get_mask_account
def test_get_mask_account_valid():
    """Тестирование корректной работы маскировки номера счета."""
    account_number = 12345678
    masked_account = get_mask_account(account_number)
    assert masked_account == "**5678"


def test_get_mask_account_invalid_length():
    """Тестирование обработки недостаточной длины номера счета."""
    account_number = 123  # Меньше 4 цифр
    with pytest.raises(ValueError, match="Номер счета должен содержать как минимум 4 цифры."):
        get_mask_account(account_number)
