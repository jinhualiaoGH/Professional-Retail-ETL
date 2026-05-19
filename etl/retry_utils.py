import time
from functools import wraps


def retry(max_attempts=3, delay_seconds=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")

                    if attempt < max_attempts:
                        time.sleep(delay_seconds)

            raise last_exception

        return wrapper

    return decorator