[1mdiff --git a/src/decorators.py b/src/decorators.py[m
[1mindex cacb4b0..6292612 100644[m
[1m--- a/src/decorators.py[m
[1m+++ b/src/decorators.py[m
[36m@@ -1,14 +1,31 @@[m
 import functools[m
[31m-from typing import Callable, Any, Optional[m
 import sys[m
[32m+[m[32mfrom typing import Any, Callable, Optional[m
[32m+[m
 [m
 def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:[m
[32m+[m[32m    """Декоратор для логирования результата выполнения функции.[m
[32m+[m
[32m+[m[32m    Args:[m
[32m+[m[32m        filename: Имя файла, в который записывать логи. Если не указано, используется stdout.[m
[32m+[m
[32m+[m[32m    Returns:[m
[32m+[m[32m        Обернутая функция с логированием результата.[m
[32m+[m[32m    """[m
     def decorator(func: Callable[..., Any]) -> Callable[..., Any]:[m
[32m+[m[32m        """Обертка для функции с логированием.[m
[32m+[m
[32m+[m[32m        Args:[m
[32m+[m[32m            func: Функция для декорирования.[m
[32m+[m
[32m+[m[32m        Returns:[m
[32m+[m[32m            Результат выполнения оригинальной функции.[m
[32m+[m[32m        """[m
         @functools.wraps(func)[m
         def wrapper(*args: Any, **kwargs: Any) -> Any:[m
             try:[m
                 result = func(*args, **kwargs)[m
[31m-                message = f"{func.__name__} ok\n"  # Доступ к имени функции через name[m
[32m+[m[32m                message = f"{func.__name__} ok\n"  # Используем __name__ для доступа к имени функции[m
                 if filename:[m
                     with open(filename, 'a') as f:[m
                         f.write(message)[m
