from django.db import connections
from typing import Any


def assign(obj: Any, **kwargs: dict):
    for key, value in kwargs.items():
        if hasattr(obj, key):
            setattr(obj, key, value)


def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()