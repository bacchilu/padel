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
                    log_console("Connecting...")
                    return func(*args, **kwargs)
                except KeyboardInterrupt:
                    return
                except:
                    log_console(f"Wait {delay_seconds} seconds to reconnect...")
                    time.sleep(delay_seconds)
                    retries += 1
            log_console(f"Max retries ({max_retries}) reached. Exiting...")

        return wrapper

    return decorator
