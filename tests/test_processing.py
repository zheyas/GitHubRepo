import pytest

from src.processing import filter_by_state, sort_by_date  # Убедитесь, что путь к функции правильный


# Фикстура для тестовых данных
@pytest.fixture
def test_data():
    return [
        {'id': 1, 'state': 'EXECUTED'},
        {'id': 2, 'state': 'PENDING'},
        {'id': 3, 'state': 'EXECUTED'},
        {'id': 4, 'state': 'CANCELLED'},
        {'id': 5, 'state': 'EXECUTED'},
    ]


# Параметризованный тест для фильтрации по состоянию
@pytest.mark.parametrize("state, expected", [
    ('EXECUTED', [{'id': 1, 'state': 'EXECUTED'}, {'id': 3, 'state': 'EXECUTED'}, {'id': 5, 'state': 'EXECUTED'}]),
    ('PENDING', [{'id': 2, 'state': 'PENDING'}]),
    ('CANCELLED', [{'id': 4, 'state': 'CANCELLED'}]),
    ('INVALID_STATE', []),  # Нет записей с указанным статусом
])
def test_filter_by_state(test_data, state, expected):
    result = filter_by_state(test_data, state)
    assert result == expected


@pytest.fixture
def test_data1():
    return [
        {'id': 1, 'date': '2024-03-11T02:26:18.671407'},
        {'id': 2, 'date': '2023-01-15T15:45:00.000000'},
        {'id': 3, 'date': '2024-03-11T02:26:18.671407'},  # Дублирующая дата
        {'id': 4, 'date': '2022-11-20T12:00:00.000000'},
        {'id': 5, 'date': '2023-05-30T09:30:45.123456'},
    ]


# Тестирование сортировки по дате в порядке убывания
def test_sort_by_date_descending(test_data1):
    expected = [
        {'id': 1, 'date': '2024-03-11T02:26:18.671407'},
        {'id': 3, 'date': '2024-03-11T02:26:18.671407'},
        {'id': 5, 'date': '2023-05-30T09:30:45.123456'},
        {'id': 2, 'date': '2023-01-15T15:45:00.000000'},
        {'id': 4, 'date': '2022-11-20T12:00:00.000000'},
    ]
    result = sort_by_date(test_data1, reverse=True)
    assert result == expected


# Тестирование сортировки по дате в порядке возрастания
def test_sort_by_date_ascending(test_data1):
    expected = [
        {'id': 4, 'date': '2022-11-20T12:00:00.000000'},
        {'id': 2, 'date': '2023-01-15T15:45:00.000000'},
        {'id': 5, 'date': '2023-05-30T09:30:45.123456'},
        {'id': 1, 'date': '2024-03-11T02:26:18.671407'},
        {'id': 3, 'date': '2024-03-11T02:26:18.671407'},
    ]
    result = sort_by_date(test_data1, reverse=False)
    assert result == expected


# Тестирование некорректных форматов дат
@pytest.mark.parametrize("invalid_data", [
    [{'id': 1, 'date': 'invalid_date_format'}],
    [{'id': 1, 'date': '2024-03-11T02:26:18'}],  # Неполный формат
    [{'id': 1, 'date': '2024/03/11 02:26:18.671407'}],  # Неправильный разделитель
])
def test_sort_by_date_invalid(invalid_data):
    with pytest.raises(ValueError):
        sort_by_date(invalid_data)
