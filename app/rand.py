"""Implementations of some functions returning random values."""

import re
import random
import string
import logging
import secrets
import uuid as std_uuid
from typing import *


__logger = logging.getLogger("rand")


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


def password(length: int, extra_chars: str = "") -> str:
    """
    Generate a secure password of specified length.

    See: https://stackoverflow.com/a/23728630

    :param length: the length of the generated password
    :param extra_chars: additional non-alphanumeric characters that will be used in the password
    """
    chars = string.ascii_letters + string.digits + extra_chars
    return ''.join(random.SystemRandom().choice(chars) for _ in range(abs(length)))


def strong_password(length: int, extra_chars: str = "", max_tries: int = 100) -> str:
    """
    Generate a secure password of specified length as the 'password' function do, but also
    ensures that password is strong enough.

    See: https://github.com/kozalosev/kozRandBot/issues/2

    :param length: the length of the generated password
    :param extra_chars: additional non-alphanumeric characters that will be used in the password
    :param max_tries: used as a threshold value to prevent the infinite loop to occur
    """
    generated_password = ""
    fuse = 0
    while not _is_password_strong(generated_password, extra_chars):
        if fuse >= max_tries:
            __logger.warning("Tried to generate proper password over {:d} times!".format(max_tries))
            break
        fuse += 1
        generated_password = password(length, extra_chars)
    __logger.info("A password was generated for {:d} times".format(fuse))
    return generated_password


def _is_password_strong(pwd: str, extra_chars: str) -> bool:
    if not re.search(r"\d", pwd):
        return False
    if not re.search(r"[a-z]", pwd) or not re.search(r"[A-Z]", pwd):
        return False
    if len(extra_chars) > 0 and not any(x in pwd for x in extra_chars):
        return False
    return True


def hex_password(nbytes: int) -> str:
    """
    Generate a string of `nbytes` bytes (i.e. 2*nbytes characters long) in
    a secure manner applicable for use as a password.

    :param nbytes: the count of bytes in the generated HEX password
    """
    return secrets.token_hex(abs(nbytes))


def uuid() -> str:
    """Generate a randomly generated Universal Unique Identifier"""
    return str(std_uuid.uuid4())
