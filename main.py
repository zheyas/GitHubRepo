import src.loadformat
import src.processing  # Импортируем модуль processing
from pathlib import Path
import src.opros
import src.utils


print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.\nВыберите необходимый пункт меню:\n"
              "1. Получить информацию о транзакциях из JSON-файла\n"
              "2. Получить информацию о транзакциях из CSV-файла\n"
              "3. Получить информацию о транзакциях из XLSX-файла")
c = int(input())
if c not in [1, 2, 3]:
    print(f"Модификации {c} не существует")
    exit()

match c:
    case 1:
        while True:
            print("Для обработки выбран JSON-файл\n")
            print("Программа: Введите статус, по которому необходимо выполнить фильтрацию."
                  "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
            filter = input()
            filter = filter.upper()
            if filter not in ["EXECUTED", "CANCELED", "PENDING"]:
                print(f"Статус операции {filter} недоступен.")
            else:
                break
        trans = src.processing.filter_by_state(src.utils.load_transactions(src.utils.file_path))
        print(src.opros.opros(trans))

    case 2:
        while True:
            print("Для обработки выбран CSV-файл\n")
            print("Программа: Введите статус, по которому необходимо выполнить фильтрацию."
                  "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
            filter = input()
            filter = filter.upper()
            if filter not in ["EXECUTED", "CANCELED", "PENDING"]:
                print(f"Статус операции {filter} недоступен.")
            else:
                break
        trans = src.loadformat.read_csv_financial_operations(src.loadformat.file_path_csv)

        print(src.opros.opros(trans))

    case 3:
        while True:
            print("Для обработки выбран XLSX-файл\n")
            print("Программа: Введите статус, по которому необходимо выполнить фильтрацию."
                  "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
            filter = input()
            filter = filter.upper()
            if filter not in ["EXECUTED", "CANCELED", "PENDING"]:
                print(f"Статус операции {filter} недоступен.")
            else:
                break
        trans = src.loadformat.read_xlsx_financial_operations(src.loadformat.file_path_xlsx)
        print(trans)
        print(src.opros.opros(trans))
    case _:
        print("До свидания!")
def process_csv():
    while True:
        print("Для обработки выбран CSV-файл\n")
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию."
              "Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")
        filter_status = input().upper()
        if filter_status not in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f"Статус операции {filter_status} недоступен.")
        else:
            break

    csv_file_path = Path('data/file.csv')
    transactions = src.loadformat.read_csv_financial_operations(csv_file_path)

    if not transactions:
        print("Нет транзакций для отображения.")
        return

    filtered_trans = src.processing.filter_by_state(transactions, filter_status)

    if not filtered_trans:
        print("Нет транзакций, соответствующих критериям фильтрации.")
    else:
        print(filtered_trans)

def process_xlsx():
    xlsx_file_path = Path('data/transactions_excel.xlsx')
    transactions = src.loadformat.read_xlsx_financial_operations(xlsx_file_path)

    if not transactions:
        print("Нет транзакций для отображения.")
    else:
        print(transactions)

