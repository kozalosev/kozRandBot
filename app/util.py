import re
from typing import Optional, List


class Items:
    """A class to split the string of options, separated by commas and conjunctions, into a list."""

    conjunctions = ['or', 'или', 'vs']

    def __init__(self, string: str):
        if ';' in string:
            self._items = re.split(r";\s*", string)
            return
        if ',' in string:
            items = re.split(r",\s*", string)
            items = list(map(self._strip_conjunctions, items))
            last_items = self._try_search_for_items_separated_by_conjunctions(self.conjunctions, items[-1])
            if last_items:
                self._items = items[:-1] + last_items
            else:
                self._items = items
            return

        self._items = self._try_search_for_items_separated_by_conjunctions(self.conjunctions, string)

    @property
    def acceptable(self) -> bool:
        """:return: True if the string is a list of options and can be split"""
        return self._items and len(self._items) > 1

    @property
    def list(self) -> list:
        """:returns: a list of options"""
        if self._items:
            lst = self._items[:-1]
            lst.append(self._items[-1].rstrip('?'))
            return lst
        else:
            return []

    @classmethod
    def _strip_conjunctions(cls, string):
        for conjunction in cls.conjunctions:
            string_to_search = conjunction + ' '
            if string.startswith(string_to_search):
                return string[len(string_to_search):]
        return string

    def _try_search_for_items_separated_by_conjunctions(self, conjunctions, string) -> Optional[List[str]]:
        for conjunction in conjunctions:
            items = self.__search_conjunction(conjunction, string)
            if items:
                return items
        return None

    @staticmethod
    def __search_conjunction(conjunction, string) -> Optional[List[str]]:
        expr = re.compile(r",?\s+%s\s+" % conjunction, flags=re.IGNORECASE)
        if re.search(expr, string):
            return re.split(expr, string)
        else:
            return None


def try_parse_int(s: str) -> Optional[int]:
    try:
        return int(s)
    except ValueError:
        return None


def try_extract_numbers(text: str) -> Optional[List[int]]:
    """Try to extract numbers from a space-separated string of numbers."""
    if not text:
        return None
    numbers_str = re.split(r",?\s", text)
    numbers = list(map(lambda n: try_parse_int(n), numbers_str))
    if None in numbers:
        return None
    return numbers
