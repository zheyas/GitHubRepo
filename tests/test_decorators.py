
from typing import Any

import pytest

from src.decorators import log  # Замените 'your_module_name' на фактическое имя вашего модуля


@log()
def successful_function(x: int, y: int) -> int:
    return x + y


@log()
def failing_function(x: int, y: int) -> float:
    return x / y


def test_successful_function(capsys: Any) -> None:
    assert successful_function(3, 2) == 5
    captured = capsys.readouterr()
    assert "successful_function ok" in captured.out


def test_failing_function(capsys: Any) -> None:
    with pytest.raises(ZeroDivisionError):
        failing_function(1, 0)
    captured = capsys.readouterr()
    assert "failing_function error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.err


def test_log_to_file(tmp_path: Any) -> None:
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def add(x: int, y: int) -> int:
        return x + y

    @log(filename=str(log_file))
    def divide(x: int, y: int) -> float:
        return x / y

    add(2, 3)
    try:
        divide(1, 0)
    except ZeroDivisionError:
        pass

    with open(log_file, 'r') as f:
        logs = f.read()
        assert "add ok" in logs
        assert "divide error: ZeroDivisionError. Inputs: (1, 0), {}" in logs
