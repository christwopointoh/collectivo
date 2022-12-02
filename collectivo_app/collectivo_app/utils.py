"""Utility functions of the collectivo app."""


def string_to_list(string: str):
    """Convert a string with items seperated by comma to a list."""
    if string == '' or string is None:
        return []
    else:
        return string.replace(' ', '').split(',')
