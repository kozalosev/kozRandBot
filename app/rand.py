"""Implementations of some functions returning random values."""

import re
import random
import string
import logging
import secrets
import uuid as std_uuid
from typing import *


__logger = logging.getLogger("rand")
T = TypeVar('T')
K = TypeVar('K')

__base_rnd = random.Random()
__sys_rnd = random.SystemRandom()


def one_out_of_two(first: T, second: K, sys_rand: bool = False) -> Union[T, K]:
    """:return: either the first or second argument randomly."""
    return _get_rnd(sys_rand).choice([first, second])


def item_from_list(items: List[T], sys_rand: bool = False) -> T:
    """:return: a random item from the list"""
    return _get_rnd(sys_rand).choice(items)


def between(min_val: int, max_val: int, sys_rand: bool = False) -> int:
    """:return: a random number in range [min_val; max_val]"""
    if min_val > max_val:
        max_val, min_val = min_val, max_val
    return _get_rnd(sys_rand).randint(min_val, max_val)


def maximum(num: int, sys_rand: bool = False) -> Union[int, float]:
    """
    :return: a random integer number in range [1, num] if 'num' is positive;
        integer number in range [num; -1] if it's negative;
        float number in range [0.0; 1.0) if it equals to 0
    """
    rnd = _get_rnd(sys_rand)
    if num == 0:
        return rnd.random()
    elif num < 0:
        return -rnd.randint(1, abs(num))
    else:
        return rnd.randint(1, num)


def _get_rnd(sys_rand: bool) -> random.Random:
    if sys_rand:
        __logger.debug("SystemRandom is used")
        return __sys_rnd
    else:
        __logger.debug("Random is used")
        return __base_rnd


def password(length: int, extra_chars: str = "", sys_rand: bool = False) -> str:
    """
    Generate a secure password of specified length.

    See: https://stackoverflow.com/a/23728630

    :param length: the length of the generated password
    :param extra_chars: additional non-alphanumeric characters that will be used in the password
    :param sys_rand: use a system source of randomness
    """
    chars = string.ascii_letters + string.digits + extra_chars
    rnd = random.SystemRandom() if sys_rand else random.Random()
    return ''.join(rnd.choice(chars) for _ in range(abs(length)))


def strong_password(length: int, extra_chars: str = "", max_tries: int = 100, sys_rand: bool = False) -> str:
    """
    Generate a secure password of specified length as the 'password' function do, but also
    ensures that password is strong enough.

    See: https://github.com/kozalosev/kozRandBot/issues/2

    :param length: the length of the generated password
    :param extra_chars: additional non-alphanumeric characters that will be used in the password
    :param max_tries: used as a threshold value to prevent the infinite loop to occur
    :param sys_rand: use a system source of randomness
    """
    generated_password = ""
    fuse = 0
    while not _is_password_strong(generated_password, extra_chars):
        if fuse >= max_tries:
            __logger.warning("Tried to generate proper password over {:d} times!".format(max_tries))
            break
        fuse += 1
        generated_password = password(length, extra_chars, sys_rand)
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
