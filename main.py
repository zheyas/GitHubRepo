from datetime import datetime
from pathlib import Path

import src.services
import src.loadformat
import src.masks
import src.opros
import src.processing  # Импортируем модуль processing
import src.utils


def format_date(date_string: str) -> str:
    # Attempt parsing with datetime.fromisoformat which covers most standard cases
    if date_string.endswith('Z'):
        # Remove 'Z' and consider it as UTC
        date_string = date_string[:-1]

    try:
        date_object = datetime.fromisoformat(date_string)
    except ValueError:
        # Fallback to strptime to handle other ISO variants or non-supported formats
        try:
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            try:
                date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                # Log or handle unsupported formats
                print(f"Unable to parse date: {date_string}")
                return "Invalid Date Format"

    # Format the date to the desired format
    return date_object.strftime("%d.%m.%Y")

print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.\nВыберите необходимый пункт меню:\n"
              "1. Получить информацию о транзакциях из JSON-файла\n"
              "2. Получить информацию о транзакциях из CSV-файла\n"
              "3. Получить информацию о транзакциях из XLSX-файла\n"
            "4. Раздел Сервисы")
c = int(input())
if c not in [1, 2, 3, 4]:
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

        trans = src.opros.opros(trans)
        print(f'Всего операций было: {len(trans)}')
        for i in trans:
            if i["description"] != 'Открытие вклада':
                f = i["from"].split(" ")
                if f[0] != "Счет":
                    f[-1] = src.masks.get_mask_card_number(f[-1])
                else:
                    f[-1] = src.masks.get_mask_account(f[-1])

            t = i["to"].split(" ")
            if t[0] != "Счет":
                t[-1] = src.masks.get_mask_card_number(t[-1])
            else:
                t[-1] = src.masks.get_mask_account(t[-1])

            if i["description"] != 'Открытие вклада':
                print(f"{format_date(i['date'])} {i['description']}")
                print(f"{' '.join(f)} -> {' '.join(t)}")
                print(f" {i['operationAmount']['amount']} {i['operationAmount']['currency']['name']} ")
        else:
                print(f"{format_date(i['date'])} {i['description']}")
                print(' '.join(t))
                print(f" {i['operationAmount']['amount']} {i['operationAmount']['currency']['name']} ")

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
        trans = src.opros.opros(trans)
        print(f'Всего операций было: {len(trans)}')
        for i in trans:
            if i["description"] != 'Открытие вклада':
                f = i["from"].split(" ")
                if f[0] != "Счет":
                    f[-1] = src.masks.get_mask_card_number(f[-1])
                else:
                    f[-1] = src.masks.get_mask_account(f[-1])

            t = i["to"].split(" ")
            if t[0] != "Счет":
                t[-1] = src.masks.get_mask_card_number(t[-1])
            else:
                t[-1] = src.masks.get_mask_account(t[-1])

            if i["description"] != 'Открытие вклада':
                print(f"{format_date(i['date'])} {i['description']}")
                print(f"{' '.join(f)} -> {' '.join(t)}")
                print(f" {i['amount']} {i['currency_name']} ")
        else:
            print(f"{format_date(i['date'])} {i['description']}")
            print(' '.join(t))
            print(f" {i['amount']} {i['currency_name']} ")
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

        print(src.opros.opros(trans))
        print(f'Всего операций было: {len(trans)}')
        for i in trans:
            if i["description"] != 'Открытие вклада':
                f = i["from_account"].split(" ")
                if f[0] != "Счет":
                    f[-1] = src.masks.get_mask_card_number(f[-1])
                else:
                    f[-1] = src.masks.get_mask_account(f[-1])

            t = i["to_account"].split(" ")
            if t[0] != "Счет":
                t[-1] = src.masks.get_mask_card_number(t[-1])
            else:
                t[-1] = src.masks.get_mask_account(t[-1])

            if i["description"] != 'Открытие вклада':
                print(f"{format_date(i['date'])} {i['description']}")
                print(f"{' '.join(f)} -> {' '.join(t)}")
                print(f" {i['amount']} {i['currency_name']} ")
        else:
            print(f"{format_date(i['date'])} {i['description']}")
            print(' '.join(t))
            print(f" {i['amount']} {i['currency_name']} ")
    case 4:
        print("Вы попали в раздел сервисы")
        year = 0
        month = 0
        while True:
            print("Введите год числом:")
            year = int(input())
            print("Введите месяц числом:")
            month = int(input())
            if (year<0) or (month not in range (1,12+1)):
                print("Некорректный ввод")
            else:
                break
        data = src.cervices.data
        s = str(year)+'-'+str(month)
        print(src.cervices.analyze_cashback_profitability(data,year,month))
        limit = 0
        while True:
            print("Введите способ округления: 10, 50, 100:")
            limit = int(input())
            if limit in [10, 50, 100]:
                break
        print(src.cervices.investment_bank(s,data,limit))
        print("Что изволите найти?")
        q = input()
        print(src.cervices.search_transactions(data,q))
        print("Наёдем телефоны")
        print(src.cervices.search_phone_transactions(data))
        print("Наёдем переводы человекам")
        print(src.cervices.search_personal_transfers(data))

    case _:
        print("До свидания!")
