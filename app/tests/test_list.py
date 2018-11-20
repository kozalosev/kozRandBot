from util import Items
from typing import List
from functools import partial


# UTILITIES

__lst = ['one', 'two', 'three', 'four']
__lst_ru = ['один', 'два', 'три', 'четыре']


def __generate_list(n: int, ru: bool = False) -> List[str]:
    assert 1 <= n <= 4
    if ru:
        return __lst_ru[:n]
    else:
        return __lst[:n]


def check(s: str, count: int, ru: bool = False):
    items = Items(s)
    lst = __generate_list(count, ru)
    assert items.acceptable
    assert items.list == lst


def gen_check(count: int, ru: bool = False):
    return partial(check, count=count, ru=ru)


# TESTS THEMSELVES

def test_commas():
    c = gen_check(3)
    c("one, two, three")
    c("one, two, three?")
    c("one, two, three???")


def test_semicolons():
    c = gen_check(3)
    c("one; two; three")
    c("one; two; three?")
    c("one; two; three???")


def test_two_items_separated_by_or():
    c = gen_check(2)
    c("one or two")
    c("one or two?")
    c("one or two???",)


def test_two_items_separated_by_or_ru():
    c = gen_check(2, ru=True)
    c("один или два")
    c("один или два?")
    c("один или два???")


def test_comma_separated_items_with_or_at_the_end():
    c = gen_check(4)
    c("one, two, three, or four")
    c("one, two, three or four")
    c("one, two, three, or four?")
    c("one, two, three or four?")


def test_comma_separated_items_with_or_at_the_end_ru():
    c = gen_check(4, ru=True)
    c("один, два, три или четыре")
    c("один, два, три, или четыре")
    c("один, два, три или четыре?")
    c("один, два, три, или четыре?")


def test_or_separated_items():
    c = gen_check(3)
    c("one, or two, or three")
    c("one, or two, or three?")


def test_or_separated_items_ru():
    c = gen_check(3, ru=True)
    c("один, или два, или три")
    c("один, или два, или три?")


def test_non_enumerations():
    assert not Items("just three words").acceptable
    assert not Items("просто три слова").acceptable
