import logging
from pathlib import Path

# Указываем относительные пути
logger = logging.getLogger('masks')
file_handler = logging.FileHandler(Path('logs/masks.log'), 'w')
file_formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляя только последние четыре цифры видимыми.

    Аргументы:
    card_number (str): Номер банковской карты в виде строки.

    Возвращает:
    str: Маскированный номер карты в формате 'XXXX XXXX XXXX XXXX'.
    """
    if len(card_number) != 16 or not card_number.isdigit():
        logger.error("Номер карты должен содержать 16 цифр и содержать только цифры.")
        raise ValueError("Номер карты должен содержать 16 цифр и содержать только цифры.")

    masked_number = f"XXXX XXXX XXXX {card_number[-4:]}"
    logger.info(f'Номер карты успешно замаскирован: {masked_number}')
    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта, оставляя только последние 4 цифры.

    Аргументы:
    account_number (str): Номер счёта в виде строки.

    Возвращает:
    str: Маскированный номер счёта в формате '****XXXX'.
    """
    if len(account_number) < 4 or not account_number.isdigit():
        logger.error("Номер счета должен содержать не менее 4 символов и содержать только цифры.")
        raise ValueError("Номер счета должен содержать не менее 4 символов и содержать только цифры.")

    masked_account = "****" + account_number[-4:]
    logger.info(f'Номер счета успешно замаскирован: {masked_account}')
    return masked_account


def mask_data_from_json(data: list) -> list:
    """
    Обрабатывает данные из JSON списка и маскирует номера карт и счетов.

    Аргументы:
    data (list): Список словарей с данными о картах и счетах.

    Возвращает:
    list: Список словарей с замаскированными данными.
    """
    masked_data = []

    for entry in data:
        masked_entry = {}
        if 'card_number' in entry:
            masked_entry['card_number'] = get_mask_card_number(entry['card_number'])
        if 'account_number' in entry:
            masked_entry['account_number'] = get_mask_account(entry['account_number'])
        masked_data.append(masked_entry)

    logger.info('Данные успешно замаскированы из списка JSON.')
    return masked_data


def mask_data_from_xlsx(data: list) -> list:
    """
    Обрабатывает данные из списка и маскирует номера карт и счетов.

    Аргументы:
    data (list): Список кортежей с данными о картах и счетах.

    Возвращает:
    list: Список словарей с замаскированными данными.
    """
    masked_data = []

    for row in data:
        masked_row = {}
        masked_row['card_number'] = get_mask_card_number(row[0]) if row[0] else None
        masked_row['account_number'] = get_mask_account(row[1]) if row[1] else None
        masked_data.append(masked_row)

    logger.info('Данные успешно замаскированы из списка для XLSX.')
    return masked_data

# Примеры использования:
# masked_json_data = mask_data_from_json([{'card_number': '1234567812345678', 'account_number': '1234567890123456'}])
# masked_xlsx_data = mask_data_from_xlsx([('1234567812345678', '1234567890123456')])
