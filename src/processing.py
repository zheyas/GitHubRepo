
from datetime import datetime
from typing import Any, Dict, List, Optional


def filter_by_state(data: Optional[List[Dict[str, Any]]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    if not data:
        print("Ошибка: данные отсутствуют или пусты. Проверьте источник данных.")
        return []
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    def parse_date(date_value: Any) -> datetime:
        if isinstance(date_value, str):
            for fmt in ('%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
                try:
                    return datetime.strptime(date_value, fmt)
                except ValueError:
                    continue
            if date_value.endswith('Z'):
                try:
                    return datetime.strptime(date_value[:-1], '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    pass
            # Выбросить ошибку, если все форматы провалились
            raise ValueError(f"Invalid date format: {date_value}")
        # Выбросить ошибку, если дата не строка
        raise ValueError(f"Date is not a string: {date_value}")

    sorted_data = sorted(
        data,
        key=lambda x: parse_date(x['date']),
        reverse=reverse
    )

    return sorted_data


def format_date(date_string: str) -> str:
    date_object = datetime.fromisoformat(date_string)
    return date_object.strftime("%d.%m.%Y")

# Example usage within the functions
# transactions = load_transactions_somehow()
# filtered_transactions = filter_by_state(transactions, 'EXECUTED')
# sorted_transactions = sort_by_date(filtered_transactions)
# for transaction in sorted_transactions:
#     print(format_date(transaction['date']))
