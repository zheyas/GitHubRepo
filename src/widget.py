from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(info: str) -> str:
    """
    Маскирует номер карты или счета в строке.

    Аргументы:
    info (str): строка формата Visa Platinum 7000792289606361, Maestro 7000792289606361, или Счет 73654108430135874305.

    Возвращает:
    str: строка с замаскированным номером карты или счета.
    """
    parts = info.split()
    if len(parts) < 2:
        return "Invalid input"
    number = parts[-1]


    # Проверяем корректность номера карты/счета
    if not number.isdigit():
        return "Invalid card/account number format"

    card_or_account_type = " ".join(parts[:-1]).lower()
    if ("visa" in card_or_account_type or "maestro" in card_or_account_type) and (len(number)!= 16):
        return 'Invalid input format'
    if "visa" in card_or_account_type or "maestro" in card_or_account_type:
        masked_number = get_mask_card_number(int(number))
        return f"{card_or_account_type} {masked_number}"
    elif "счет" in card_or_account_type:
        masked_number = get_mask_account(int(number))
        return f"{card_or_account_type} {masked_number}"
    else:
        return "Invalid input format"
def get_date(info: str) -> str:
    """
    Маскирует номер карты или счета в строке.

    Аргументы:
    info (str): строка формата Visa Platinum 7000792289606361, Maestro 7000792289606361, или Счет 73654108430135874305.

    Возвращает:
    str: строка с замаскированным номером карты или счета.
    """
    if (info.count("-") == 2 and "T" in info):
        date = info.split("-")
        return (f"{date[2][0:2]}.{date[1]}.{date[0]}")
    else:
        return 'Invalid date format'


