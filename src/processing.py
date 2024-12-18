
from datetime import datetime
from typing import Any, Dict, List, Optional


def filter_by_state(data: Optional[List[Dict[str, Any]]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    if not data:
        print("Ошибка: данные отсутствуют или пусты. Проверьте источник данных.")
        return []
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    def parse_date(date_value: Any) -> Optional[datetime]:
        if isinstance(date_value, str):
            for fmt in ('%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
                try:
                    return datetime.strptime(date_value, fmt)
                except ValueError:
                    continue
            if date_value.endswith('Z'):
                date_value = date_value[:-1]
                try:
                    return datetime.strptime(date_value, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    pass
            print(f"Неподдерживаемый формат даты: {date_value}")
            return None
        else:
            print(f"Предупреждение: дата не в строковом формате ({date_value}), пропущена.")
            return None

    filtered_data = [item for item in data if 'date' in item and item['date']]
    sorted_data = sorted(
        filtered_data,
        key=lambda x: parse_date(x['date']) or datetime.min,
        reverse=reverse
    )

    # Отладочная информация
    if not sorted_data:
        print("Отсортированные данные пусты или отсутствуют корректные даты.")

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
