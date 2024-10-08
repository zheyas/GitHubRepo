import functools
import sys
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор для логирования результата выполнения функции.

    Args:
        filename: Имя файла, в который записывать логи. Если не указано, используется stdout.

    Returns:
        Обернутая функция с логированием результата.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Обертка для функции с логированием.

        Args:
            func: Функция для декорирования.

        Returns:
            Результат выполнения оригинальной функции.
        """
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok\n"  # Используем __name__ для доступа к имени функции
                if filename:
                    with open(filename, 'a') as f:
                        f.write(message)
                else:
                    sys.stdout.write(message)
                return result
            except Exception as e:
                error_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(error_message)
                else:
                    sys.stderr.write(error_message)
                raise
        return wrapper
    return decorator
