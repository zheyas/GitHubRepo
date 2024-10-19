import json
import os


def load_transactions(file_path):
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        return []

    try:
        # Открываем файл и пытаемся загрузить данные
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, OSError):
        # Обработка ошибок чтения и декодирования JSON
        return []


file_path = r"D:\pyton\Курсы\pythonProjectN1\data\operations.json"
