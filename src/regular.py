import re


def search_transactions(transactions, search_string):
    # Скомпилируем регулярное выражение для строки поиска, игнорируя регистр
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Отфильтруем список словарей, у которых описание содержит искомую строку
    result = [transaction for transaction in transactions if pattern.search(transaction.get("description", ""))]

    return result
