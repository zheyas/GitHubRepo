from datetime import datetime


def sort_by_date(data, reverse=True):
    """
    Сортирует список словарей по ключу 'date', учитывая время в формате ISO.

    :param data: список словарей
    :param reverse: порядок сортировки. True для убывания, False для возрастания.
    :return: новый список, отсортированный по ключу 'date'
    """
    return sorted(data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=reverse)
