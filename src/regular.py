import re
from collections import Counter


def search_transactions(transactions, search_string):
    # Скомпилируем регулярное выражение для строки поиска, игнорируя регистр
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Отфильтруем список словарей, у которых описание содержит искомую строку
    result = [transaction for transaction in transactions if pattern.search(transaction.get("description", ""))]

    return result


def count_operations_by_category(operations, categories):
    # Инициализируем Counter для подсчета операций по категориям
    category_counter = Counter(
        operation.get('description', '') for operation in operations if operation.get('description', '') in categories
    )

    # Создаем словарь с категориями и их количеством, включая категории с нулевым значением
    category_count = {category: category_counter.get(category, 0) for category in categories}

    return category_count
