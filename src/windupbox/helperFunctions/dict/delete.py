
def delete_none(_dict):
    """Delete None values recursively from all of the dictionaries"""
    if isinstance(_dict, dict):
        for key, value in list(_dict.items()):
            if isinstance(value, dict):
                _dict[key] = delete_none(value)
            elif value is None or key is None:
                del _dict[key]

    elif isinstance(_dict, (list, set, tuple)):
        _dict = type(_dict)(delete_none(item) for item in _dict if item is not None)

    return _dict
