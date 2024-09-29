def filter_by_state(data, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param data: список словарей
    :param state: значение ключа 'state', по умолчанию 'EXECUTED'
    :return: новый список, содержащий только те словари, где ключ 'state' соответствует переданному значению
    """
    return [item for item in data if item.get('state') == state]