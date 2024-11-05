from typing import Any, Dict, List

import pytest

from src.cervices import (
    analyze_cashback_profitability,
    investment_bank,
    search_personal_transfers,
    search_phone_transactions,
    search_transactions,
)


@pytest.fixture
def mock_data() -> List[Dict[str, Any]]:
    """Фикстура для предоставления тестовых данных."""
    return [
        {
            'Дата операции': '01.12.2021 15:30:00',
            'Категория': 'Фастфуд',
            'Кэшбэк': '10.5',
            'Сумма операции': '100',
            'Описание': 'Покупка еды'
        },
        {
            'Дата операции': '05.12.2021 12:00:00',
            'Категория': 'Мобильная связь',
            'Кэшбэк': '5',
            'Сумма операции': '200',
            'Описание': 'Оплата связи +79031234567'
        },
        {
            'Дата операции': '10.12.2021 18:00:00',
            'Категория': 'Переводы',
            'Кэшбэк': '0',
            'Сумма операции': '1500',
            'Описание': 'Иван И.'
        },
    ]


def test_analyze_cashback_profitability(mock_data):
    """Тестируем анализ кешбэка по категориям."""
    result = analyze_cashback_profitability(mock_data, 2021, 12)
    assert '"Фастфуд": 10.5' in result
    assert '"Мобильная связь": 5.0' in result


@pytest.fixture
def investment_mock_data() -> List[Dict[str, Any]]:
    """Фикстура для тестирования инвестиционного банка."""
    return [
        {'Дата операции': '01.12.2021 15:30:00', 'Сумма операции': '170.0'},
        {'Дата операции': '02.12.2021 10:00:00', 'Сумма операции': '220.0'},
        {'Дата операции': '03.12.2021 12:00:00', 'Сумма операции': '1505.0'},
        {'Дата операции': '01.12.2021 15:30:00', 'Сумма операции': '78.0'},
        {'Дата операции': '04.12.2021 08:00:00', 'Сумма операции': '265.0'},
        {'Дата операции': '10.12.2021 18:00:00', 'Сумма операции': '324.0'},
    ]


def test_investment_bank(investment_mock_data):
    """Тестируем расчет накоплений для инвесткопилки."""
    result = investment_bank("2021-12", investment_mock_data, 50)

    # Подсчитаем ожидаемую сумму вручную с учетом округлений до ближайшего предела 50
    expected_result = 30 + 30 + 45 + 22 + 35 + 26  # Итого 100

    assert result == pytest.approx(expected_result, 0.01)


def test_search_transactions(mock_data):
    """Тестируем поиск транзакций по запросу."""
    result = search_transactions(mock_data, "Фастфуд")
    assert "Фастфуд" in result
    assert "Покупка еды" in result

    result_empty = search_transactions(mock_data, "Такси")
    assert "Транзакции, соответствующие запросу, не найдены." in result_empty


def test_search_phone_transactions(mock_data):
    """Тестируем поиск транзакций с мобильными номерами."""
    result = search_phone_transactions(mock_data)
    assert "+79031234567" in result
    assert "Мобильная связь" in result


def test_search_personal_transfers(mock_data):
    """Тестируем поиск переводов физическим лицам."""
    result = search_personal_transfers(mock_data)
    assert "Переводы" in result
    assert "Иван И." in result
