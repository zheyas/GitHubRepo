import functools
from typing import Callable, Any, Optional
import sys

def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok\n"  # Доступ к имени функции через name
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
