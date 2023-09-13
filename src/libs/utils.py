import sys
import time


def log_console(*data: object):
    print(*data, file=sys.stderr)


def reconnection_decorator(max_retries=3, delay_seconds=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except KeyboardInterrupt:
                    return
                except:
                    print("Retrying connection...")
                    time.sleep(delay_seconds)
                    retries += 1
            print(f"Max retries ({max_retries}) reached. Exiting...")

        return wrapper

    return decorator
