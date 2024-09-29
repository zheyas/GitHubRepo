def get_mask_card_number(card_number: int) -> str:
    """
    Маскирует номер банковской карты, оставляя только последние четыре цифры видимыми.

    Аргументы:
    card_number (int): Номер банковской карты в виде числа.

    Возвращает:
    str: Маскированный номер карты в формате 'XXXX XX** **** XXXX'.
    """
    card_number_str = str(card_number)
    if len(card_number_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр.")
    return f"XXXX XX{card_number_str[6:8]} **** {card_number_str[12:]}"


def get_mask_account(account_number: int) -> str:
    """
    Маскирует номер банковского счета, оставляя только последние четыре цифры видимыми.

    Аргументы:
    account_number (int): Номер банковского счета в виде числа.git statusgit status

    Возвращает:
    str: Маскированный номер счета в формате '**XXXX'.
    """
    account_number_str = str(account_number)
    if len(account_number_str) < 4:
        raise ValueError("Номер счета должен содержать как минимум 4 цифры.")
    return f"**{account_number_str[-4:]}"
