import sys


def log_console(*data: object):
    print(*data, file=sys.stderr)
