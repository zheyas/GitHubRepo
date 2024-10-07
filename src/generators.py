
from typing import Generator, List, Dict, Any


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    descriptions: List[str] = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту"
    ]
    index: int = 0
    while True:
        yield descriptions[index % len(descriptions)]
        index += 1


def card_number_generator(start: str, end: str) -> Generator[str, None, None]:
    current: int = int(start.replace(" ", ""))
    end_num: int = int(end.replace(" ", ""))

    while current <= end_num:
        number_str: str = f"{current:016}"
        formatted_number: str = f"{number_str[:4]} {number_str[4:8]} {number_str[8:12]} {number_str[12:]}"
        yield formatted_number
        current += 1
