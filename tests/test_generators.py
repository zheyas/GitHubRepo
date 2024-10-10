import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_transaction_descriptions() -> None:
    transactions = [
        {'id': 1, 'amount': 100, 'currency': 'USD'},
        {'id': 2, 'amount': 200, 'currency': 'EUR'}
    ]
    descriptions = transaction_descriptions(transactions)
    expected = [
        "Описание отсутствует",
        "Описание отсутствует"
    ]

    for i in range(len(expected)):
        assert next(descriptions) == expected[i]


def test_card_number_generator() -> None:
    start = "0000 0000 0000 0001"
    end = "0000 0000 0000 0010"
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


def test_filter_by_currency_usd():
    transactions = [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "200.00",
                "currency": {
                    "name": "EUR",
                    "code": "EUR"
                }
            }
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "150.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        }
    ]

    # Применяем фильтр для USD
    usd_transactions = list(filter_by_currency(transactions, "USD"))

    # Проверяем количество отфильтрованных транзакций
    assert len(usd_transactions) == 2

    # Проверяем, что отфильтрованы правильные транзакции
    assert usd_transactions[0]["id"] == 1
    assert usd_transactions[1]["id"] == 3


def test_filter_by_currency_eur():
    transactions = [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "200.00",
                "currency": {
                    "name": "EUR",
                    "code": "EUR"
                }
            }
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "150.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        }
    ]

    # Применяем фильтр для EUR
    eur_transactions = list(filter_by_currency(transactions, "EUR"))

    # Проверяем количество отфильтрованных транзакций
    assert len(eur_transactions) == 1

    # Проверяем, что отфильтрована правильная транзакция
    assert eur_transactions[0]["id"] == 2


def test_filter_by_currency_none():
    transactions = [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        }
    ]

    # Применяем фильтр для GBP, которая отсутствует
    gbp_transactions = list(filter_by_currency(transactions, "GBP"))

    # Проверяем, что нет транзакций с данной валютой
    assert len(gbp_transactions) == 0
