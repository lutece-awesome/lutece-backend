from typing import Any


def assign(obj: Any, **kwargs: dict):
    for key, value in kwargs.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
