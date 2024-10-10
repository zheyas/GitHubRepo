from datetime import datetime


def filter_by_state(data, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param data: список словарей
    :param state: значение ключа 'state', по умолчанию 'EXECUTED'
    :return: новый список, содержащий только те словари, где ключ 'state' соответствует переданному значению
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(data, reverse=True):
    """
    Сортирует список словарей по ключу 'date', учитывая время в формате ISO.

    :param data: список словарей
    :param reverse: порядок сортировки. True для убывания, False для возрастания.
    :return: новый список, отсортированный по ключу 'date'
    """
    return sorted(data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=reverse)
