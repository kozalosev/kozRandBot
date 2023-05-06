"""All implementations of inline handlers."""

import re
import random
from klocmod import LanguageDictionary
from typing import *

import rand
from handler.abc import HTML, Markdown, InlineHandler
from util import try_parse_int, Items
from .util import escape_html
from data import config


class FlipCoinHandler(InlineHandler):
    @classmethod
    def can_process(cls, query: str) -> bool:
        return query == ""

    def get_text(self, query: str, lang: LanguageDictionary) -> str:
        return rand.one_out_of_two(lang['heads'], lang['tails'])


class RandNumHandler(Markdown, InlineHandler):
    RANGE_REGEXP = r"^([-+]?[0-9]+)[,;]?\s+([-+]?[0-9]+)$"

    _range: Tuple[Optional[int], int] = None

    @classmethod
    def can_process(cls, query: str) -> bool:
        parsed = try_parse_int(query)
        return parsed is not None and parsed != 0 or re.match(cls.RANGE_REGEXP, query)

    def get_text(self, query: str, lang: LanguageDictionary) -> str:
        min_val, max_val = self._get_range(query)
        if min_val is None and max_val == 1:
            return lang['rand_num_from_zero_to_one_message'].format(rand.maximum(0))
        elif min_val is None:
            return lang['rand_num_from_zero_message'].format(max_val, rand.maximum(max_val))
        else:
            return lang['rand_num_message'].format(min_val, max_val, rand.between(min_val, max_val))

    def get_description(self, query: str, lang: LanguageDictionary) -> str:
        min_val, max_val = self._get_range(query)
        if min_val is None:
            return lang['rand_num_from_zero_description'].format(max_val)
        else:
            return lang['rand_num_description'].format(min_val, max_val)

    def _get_range(self, query: str) -> Tuple[Optional[int], int]:
        if not self._range:
            num_range = re.match(self.RANGE_REGEXP, query)
            if num_range:
                min_val, max_val = int(num_range.group(1)), int(num_range.group(2))
            else:
                min_val, max_val = None, int(query)
            self._range = (min_val, max_val)
        return self._range


class YesNoHandler(HTML, InlineHandler):
    @classmethod
    def can_process(cls, query: str) -> bool:
        return query.endswith("?")

    def get_text(self, query: str, lang: LanguageDictionary) -> str:
        yes_no_result = rand.one_out_of_two(lang['yes'], lang['no'])
        return lang['yes_no_message'].format(escape_html(query), escape_html(yes_no_result))


class RandItemHandler(HTML, InlineHandler):
    @classmethod
    def can_process(cls, query: str) -> bool:
        return Items(query).acceptable

    def get_text(self, query: str, lang: LanguageDictionary) -> str:
        items_list = [escape_html(s) for s in Items(query).list]
        return lang['rand_item_message'].format(query, random.choice(items_list))


class PasswordHandler(HTML, InlineHandler):
    _length: int = None

    @classmethod
    def can_process(cls, query: str) -> bool:
        length = try_parse_int(query)
        return query == "" or length and config.MIN_PASSWORD_LENGTH <= length <= config.MAX_PASSWORD_LENGTH

    def get_text(self, query: str, lang: LanguageDictionary) -> str:
        length = self._get_length(query)
        password = rand.strong_password(length, config.PASSWORD_EXTRA_CHARS, config.MAX_PASSWORD_GENERATION_TRIES)
        return lang['password_message'].format(length, escape_html(password))

    def get_description(self, query: str, lang: LanguageDictionary) -> str:
        template = super().get_description(query, lang)
        return template.format(self._get_length(query))

    def _get_length(self, query: str) -> int:
        if self._length is None:
            self._length = try_parse_int(query)
            if not (self._length and config.MIN_PASSWORD_LENGTH <= self._length <= config.MAX_PASSWORD_LENGTH):
                self._length = config.DEFAULT_PASSWORD_LENGTH
        return self._length
