import src.processing
import src.regular
import src.utils
import src.decorators
import src.widget
import src.processing
import src.generators
import src.loadformat
import src.masks


def opros (trans):
    bool_choice = [True,True,True,True]
    itranor = 0
    while True:
        transactions = trans
        print("Отсортировать операции по дате? Да/Нет:")
        choice = input().lower()
        if choice not in ["да","нет"]:
            print("Некорректный ввод")
        else:
            if choice == "нет":
                bool_choice[itranor] = False
            itranor += 1
            break
    while bool_choice[0]:
        print('Отсортировать по возрастанию или по убыванию?')
        choice = input().lower()
        if choice not in ['по возрастанию','по убыванию']:
            print("Некорректный ввод")
        else:
            if choice == 'по возрастанию':
                bool_choice[itranor] = False
            itranor+=1
            transactions = src.processing.sort_by_date(transactions,bool_choice[1])
            break
    while True:
        print('Выводить только рублевые тразакции? Да/Нет')
        choice = input().lower()
        if choice not in ["да", "нет"]:
            print("Некорректный ввод")
        else:
            if choice == "нет":
                bool_choice[itranor] = False
                itranor += 1
            if bool_choice[2]:
                transactions = list (src.generators.filter_by_currency(transactions,"RUB"))
            break
    while True:
        print('Отфильтровать список транзакций по определенному слову в описании? Да/Нет')
        choice = input().lower()
        if choice not in ["да", "нет"]:
            print("Некорректный ввод")
        else:
            if choice == "нет":
                bool_choice[-1] = False
            itranor += 1
            break
    while bool_choice[-1]:
        print("Укажите слово:")
        choice = input()

        transactions = src.regular.search_transactions(transactions, choice)
        break
    return transactions

#trans = src.loadformat.read_csv_financial_operations(src.loadformat.file_path)
#print(opros(trans))






