# -*- coding: utf-8 -*-
"""
"""


def normalize_number(
    number: str
) -> str:
    """
    """
    try:
        x, y = number.split(".")
        y = y.strip('0')
        if y == "":
            y = "0"
        return f"{int(x)}.{int(y)}"
    except ValueError as e:
        return f"{float(number)}"
