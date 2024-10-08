
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

def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генерирует последовательность номеров карт в заданном диапазоне.

    Args:
        start (int): Начальное значение для генерации номера карты.
        end (int): Конечное значение для генерации номера карты.

    Yields:
        str: Форматированный номер карты в виде "XXXX XXXX XXXX XXXX".
    """
    current: int = start

    while current <= end:
        number_str: str = f"{current:016}"
        formatted_number: str = f"{number_str[:4]} {number_str[4:8]} {number_str[8:12]} {number_str[12:]}"
        yield formatted_number
        current += 1

# Пример использования

    #
    # transactions = [
    #     {'id': 1, 'description': 'Платеж за услуги'},
    #     {'id': 2, 'description': 'Возврат'},
    #     {'id': 3, 'description': 'Покупка товара'},
    # ]
    #
    # print("Описания транзакций:")
    # for description in transaction_descriptions(transactions):
    #     print(description)
    #
    # print("\nГенератор номеров карт:")
    # for number in card_number_generator(1, 10):
    #     print(number)
