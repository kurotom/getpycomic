# -*- coding: utf-8 -*-
"""
"""


def normalize_number(
    number: str
) -> str:
    """
    """
    x, y = number.split(".")
    y = y.strip('0')
    if y == "":
        y = "0"
    return f"{int(x)}.{y}"
