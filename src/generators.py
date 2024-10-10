from typing import Any, Dict, Generator, List


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генерирует описание каждой транзакции из списка.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций, каждая из которых представлена словарем.

    Yields:
        str: Описание транзакции или сообщение 'Описание отсутствует', если описание не найдено.
    """
    for transaction in transactions:
        description = transaction.get('description', 'Описание отсутствует')
        yield description


def card_number_generator(start: str, end: str) -> Generator[str, None, None]:
    """
    Генерирует последовательность номеров карт в заданном диапазоне.

    Args:
        start (str): Начальное значение для генерации номера карты в виде строки.
        end (str): Конечное значение для генерации номера карты в виде строки.

    Yields:
        str: Форматированный номер карты в виде "XXXX XXXX XXXX XXXX".
    """
    start_number = int(start.replace(" ", ""))
    end_number = int(end.replace(" ", ""))

    current_number = start_number
    while current_number <= end_number:
        number_str = f"{current_number:016}"
        formatted_number = f"{number_str[:4]} {number_str[4:8]} {number_str[8:12]} {number_str[12:]}"
        yield formatted_number
        current_number += 1


def filter_by_currency(transactions, currency_code):
    """Фильтрует транзакции по заданной валюте."""
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction
