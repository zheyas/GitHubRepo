import re


def search_transactions(transactions, search_string):
    # Скомпилируем регулярное выражение для строки поиска, игнорируя регистр
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Отфильтруем список словарей, у которых описание содержит искомую строку
    result = [transaction for transaction in transactions if pattern.search(transaction.get("description", ""))]

    return result


def count_operations_by_category(operations, categories):
    # Инициализируем словарь для подсчета операций по категориям
    category_count = {category: 0 for category in categories}

    # Проходим по всем операциям
    for operation in operations:
        # Получаем описание категории из операции
        description = operation.get('description', '')

        # Увеличиваем счетчик соответствующей категории
        if description in categories:
            category_count[description] += 1

    return category_count
