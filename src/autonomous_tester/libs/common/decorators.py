"""Decorators for the autonomous tester."""

from functools import wraps


def singleton(f):
    """singleton decorator to ensure a function only runs once
    this means if we call get_webclient in multiple places with the same credentials
    we won't create a new session / invalidate the previous session

    tbd whether it's useful enough for the other clients
    """
    result = None
    executed = False

    @wraps(f)
    def wrapper(*args, **kwargs):
        nonlocal result, executed

        if not executed:
            result = f(*args, **kwargs)
            executed = True

        return result

    return wrapper
