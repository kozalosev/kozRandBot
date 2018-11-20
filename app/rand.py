"""Implementations of some functions returning random values."""

import random
import string
from typing import *


def one_out_of_two(first, second) -> Any:
    """:return: either the first or second argument randomly."""
    return random.choice([first, second])


def between(min_val: int, max_val: int) -> int:
    """:return: a random number in range [min_val; max_val]"""
    if min_val > max_val:
        max_val, min_val = min_val, max_val
    return random.randint(min_val, max_val)


def maximum(num: int) -> Union[int, float]:
    """
    :return: a random integer number in range [1, num] if 'num' is positive;
        integer number in range [num; -1] if it's negative;
        float number in range [0.0; 1.0) if it equals to 0
    """
    if num == 0:
        return random.random()
    elif num < 0:
        return -random.randint(1, abs(num))
    else:
        return random.randint(1, num)


def password(length: int) -> str:
    """
    Generate a secure password of specified length.

    See: https://stackoverflow.com/a/23728630
    """
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(abs(length)))
