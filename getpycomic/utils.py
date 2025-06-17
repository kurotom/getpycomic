# -*- coding: utf-8 -*-
"""
"""

from fake_useragent import UserAgent
import re


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


def get_user_agent() -> str:
    """
    """
    ua = UserAgent(
        browsers=["Firefox", "Chrome"],
        os=["Windows", "Linux", "Ubuntu", "Mac OS X"],
        platforms="desktop"
    )
    return ua.random



def parser_volumes(
    string: str,
) -> dict:
    """
    As in a dictionary, the key is the volume number and its value is the
    chapters, which must have a comma or hyphen separator to determine the
    range of chapters.

    Examples:
        * `{1:[1,2],2:[3,4]}`
        * `{1:[1-2],2:[3-4]}`
    """
    matrix = {}
    if string is None:
        return {"matrix": matrix}

    string = ''.join(string).strip().replace(" ", "")

    for item in re.findall(r'(\d+:\[(\d+\.\d+|\d+)[,-](\d+\.\d+|\d+)\])', string):
        item = item[0]
        item = item.replace('[', "").replace("]", "")

        values = []
        k, v = item.split(":")

        try:
            for i in re.split(r',|-', v):
                if i.isdigit():
                    values.append(int(i))
                else:
                    values.append(float(i))
            matrix[int(k)] = values
        except Exception as e:
            pass
    return {"matrix": matrix}

def parser_chapter(
    string: str,
) -> dict:
    """
    `string` formats:
        * `5`, `1,5`, `2.5,3.1`  : from the given number of chapter/s.
        * `1-5`, `2.5-3.1`  : range of chapters.
        * `5+`, `2.1+`  : from this number up to the last available chapters.
        * `all`  : all available chapters.
    """
    def convert_nums(nums: list) -> list:
        r = []
        for i in nums:
            try:
                r.append(int(i))
            except:
                r.append(float(i))
        r.sort()
        return r

    string = string.strip()
    d_chaps = {
            "n_chapters": None,
            "range": None,
            "update": False,
        }
    nums_ = re.findall(r'(\d+\.\d+|\d+)', string)
    if string == "all":
        return d_chaps

    elif "+" in string:
        d_chaps["update"] = True
        d_chaps["n_chapters"] = [float(nums_[0])]

    elif "," in string:
        d_chaps["n_chapters"] = list(set(convert_nums(nums_)))

    elif "-" in string:
        d_chaps["range"] = convert_nums(nums_[:2])

    else:
        nums_ = [nums_[0]]
        d_chaps["n_chapters"] = convert_nums(nums_)

    return d_chaps
