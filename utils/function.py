def assign(object, **kwargs):
    for key, value in kwargs.items():
        if hasattr(object, key):
            setattr(object, key, value)
