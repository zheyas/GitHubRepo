
import pytest
from src.generators import transaction_descriptions, card_number_generator


def test_transaction_descriptions() -> None:
    transactions = [
        {'id': 1, 'amount': 100, 'currency': 'USD'},
        {'id': 2, 'amount': 200, 'currency': 'EUR'}
    ]
    descriptions = transaction_descriptions(transactions)
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации"
    ]

    for i in range(len(expected)):
        assert next(descriptions) == expected[i]


def test_card_number_generator() -> None:
    start: str = "0000 0000 0000 0001"
    end: str = "0000 0000 0000 0010"
    expected_results = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
        "0000 0000 0000 0006",
        "0000 0000 0000 0007",
        "0000 0000 0000 0008",
        "0000 0000 0000 0009",
        "0000 0000 0000 0010",
    ]

    cards = card_number_generator(start, end)

    for expected in expected_results:
        assert next(cards) == expected


def test_card_number_generator_single_number() -> None:
    start: str = "0000 0000 0000 0005"
    end: str = "0000 0000 0000 0005"
    expected: str = "0000 0000 0000 0005"

    cards = card_number_generator(start, end)
    assert next(cards) == expected

    with pytest.raises(StopIteration):
        next(cards)
