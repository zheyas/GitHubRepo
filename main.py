import src.processing
import src.opros

while True:
    сhoice = 0
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.\nВыберите необходимый пункт меню:\n"
          "1. Получить информацию о транзакциях из JSON-файла\n"
          "2. Получить информацию о транзакциях из CSV-файла\n"
          "3. Получить информацию о транзакциях из XLSX-файла")
    сhoice = int(input())
    if сhoice not in [1, 2, 3]:
        print(f"Модификации {сhoice} не существует")
    else:
        break


match сhoice:
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
        trans = src.processing.filter_by_state(src.utils.load_transactions())
        print(src.opros.opros(trans))

    case 2:
        print("Зашли 2")
    case 3:
        print("Зашли 3")
    case _:
        print("До свидания!")
