from django.db import connections
from typing import Any, List


def assign(obj: Any, **kwargs: dict):
    for key, value in kwargs.items():
        if hasattr(obj, key):
            setattr(obj, key, value)


def pop_property(obj: dict, field: List[str]):
    for each in field:
        if each in obj:
            obj.pop(each)


def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


def recursive_merge_dicts(d1, d2) -> dict:
    if isinstance(d1, dict) and isinstance(d2, dict):
        return {
            **d1,
            **d2,
            **{k: recursive_merge_dicts(d1[k], d2[k]) for k in {*d1} & {*d2}}
        }
    else:
        return d2
